import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.crud import recipeBewertung
from db.crud import restBewertung
from db.crud.allergies import create_allergie
from db.crud.cuisine import create_cuisine
from db.crud.filter import create_filterRest
from db.crud.filter import update_filterRest
from db.crud.restaurant import create_restaurant
from db.crud.restaurant import delete_restaurant
from db.crud.restaurant import get_all_restaurants
from db.crud.restaurant import get_restaurant_by_id
from db.crud.user import create_user
from db.crud.user import delete_user
from db.crud.user import get_user_by_mail
from db.crud.user import update_user
from schemes import Allergies
from schemes import Cuisine
from schemes import scheme_allergie
from schemes import scheme_cuisine
from schemes import scheme_filter
from schemes import scheme_recipe
from schemes import scheme_rest
from schemes import scheme_user
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import RestaurantNotFound
from schemes.exceptions import UserNotFound
from schemes.scheme_user import UserBase
from schemes.scheme_user import UserCreate
from tools.hashing import Hasher

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.mark.filterwarnings("ignore")
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def add_allergies(db_session: SessionTesting) -> None:
    for allergie in Allergies:
        create_allergie(db_session, allergie)


@pytest.fixture(scope="function")
def add_cuisines(db_session: SessionTesting) -> None:
    for cuisine in Cuisine:
        create_cuisine(db_session, cuisine)


def test_restaurant(db_session: SessionTesting):

    # Add two Restaurants
    # add the first restaurant
    rest_add = scheme_rest.RestaurantBase(place_id="1234", name="Rest 1 nice")
    rest_return = create_restaurant(db_session, rest_add)
    assert rest_add == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # add the second restaurant
    rest_add_2 = scheme_rest.RestaurantBase(place_id="567", name="Rest 2 nice")
    rest_return = create_restaurant(db_session, rest_add_2)
    assert rest_add_2 == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # Get one Restaurant
    rest_return = get_restaurant_by_id(db_session, rest_add.place_id)
    assert rest_add == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # Get all Restaurants
    rests_return = get_all_restaurants(db_session)
    rests_return_schemes = [scheme_rest.RestaurantBase(**rest.__dict__) for rest in rests_return]
    assert rests_return_schemes == [rest_add, rest_add_2]

    # Delete that Restaurant
    affected_rows = delete_restaurant(db_session, rest_add)
    assert affected_rows == 1
    assert get_restaurant_by_id(db_session, rest_add.place_id) is None

    # Check if you cant add the same restaurant twice
    with pytest.raises(DuplicateEntry):
        create_restaurant(db_session, rest_add_2)


def test_user(db_session: SessionTesting):
    # Add two users
    # ...first user
    user_add = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_ret = create_user(db_session, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # ..second user
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    user_ret = create_user(db_session, user_add_2)
    assert user_add_2.email == user_ret.email
    assert Hasher.verify_password(user_add_2.password, user_ret.hashed_password)

    # Update User password
    user_add.password = "new_password"
    user_ret = update_user(db_session, user_add, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Update User email
    tmp_user = user_add.copy()
    user_add.email = "new@mail.test"
    user_ret = update_user(db_session, tmp_user, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Get one User
    user_ret = get_user_by_mail(db_session, user_add.email)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Delete one User
    assert 1 == delete_user(db_session, user_add_2)

    # Chek if only one user with the same email can be added
    with pytest.raises(DuplicateEntry):
        create_user(db_session, user_add)


def test_restaurant_bewertung(db_session: SessionTesting):
    fake_user = scheme_user.UserBase(email="fake@nope.ok")
    fake_rest = scheme_rest.RestaurantBase(place_id="000000", name="Fake Rest")
    user_add_1 = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    rest_add_1 = scheme_rest.RestaurantBase(place_id="1234", name="Rest 1")
    rest_add_2 = scheme_rest.RestaurantBase(place_id="5678", name="Rest 2")

    # Add user
    create_user(db_session, user_add_1)
    create_user(db_session, user_add_2)

    # Add restaurant
    create_restaurant(db_session, rest_add_1)
    create_restaurant(db_session, rest_add_2)

    # Add assessment to user1 and rest1
    assessment_add_1_1 = scheme_rest.RestBewertungCreate(
        name="Rest 1 1", comment="This is a comment", rating=1.5, person=user_add_1, restaurant=rest_add_1
    )
    assessment_ret = restBewertung.create_bewertung(db_session, assessment_add_1_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user1 and rest2
    assessment_add_1_2 = scheme_rest.RestBewertungCreate(
        name="Rest 1 2", comment="This is a comment for rest 2", rating=2.5, person=user_add_1, restaurant=rest_add_2
    )
    assessment_ret = restBewertung.create_bewertung(db_session, assessment_add_1_2)
    assert assessment_ret.kommentar == assessment_add_1_2.comment
    assert assessment_ret.rating == assessment_add_1_2.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user2 and rest2
    assessment_add_2_2 = scheme_rest.RestBewertungCreate(
        name="Rest 2 2", comment="This is a comment 2", rating=3.5, person=user_add_2, restaurant=rest_add_2
    )
    assessment_ret = restBewertung.create_bewertung(db_session, assessment_add_2_2)
    assert assessment_ret.kommentar == assessment_add_2_2.comment
    assert assessment_ret.rating == assessment_add_2_2.rating
    assert assessment_ret.zeitstempel is not None

    # Get all assessments
    assessments_ret = restBewertung.get_all_user_bewertungen(db_session, user_add_1)
    assert len(assessments_ret) == 2

    assessments_ret = restBewertung.get_all_user_bewertungen(db_session, user_add_2)
    assert len(assessments_ret) == 1

    # Get one assessment from one user to one rest
    assessment_ret = restBewertung.get_bewertung_from_user_to_rest(db_session, user_add_1, rest_add_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Update assessment
    updated_1_1 = assessment_add_1_1.copy()
    updated_1_1.comment = "UPDATED"
    updated_1_1.rating = 0
    assessment_ret = restBewertung.update_bewertung(db_session, assessment_add_1_1, updated_1_1)
    assert assessment_ret.kommentar == updated_1_1.comment
    assert assessment_ret.rating == updated_1_1.rating
    assert assessment_ret.person_email == updated_1_1.person.email
    assert assessment_ret.place_id == updated_1_1.restaurant.place_id

    # Try to get assessments that does not exist
    assessment_ret = restBewertung.get_all_user_bewertungen(db_session, fake_user)
    assert assessment_ret is None

    assessment_ret = restBewertung.get_bewertung_from_user_to_rest(db_session, fake_user, rest_add_1)
    assert assessment_ret is None

    assessment_ret = restBewertung.get_bewertung_from_user_to_rest(db_session, user_add_1, fake_rest)
    assert assessment_ret is None

    # Try to add assessments with invalid user and restaurant
    with pytest.raises(UserNotFound):
        assessment_ret = restBewertung.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(
                name="Troll", comment="none", rating=0, person=fake_user, restaurant=rest_add_1
            ),
        )

    with pytest.raises(RestaurantNotFound):
        assessment_ret = restBewertung.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(
                name="Nice",
                comment="none",
                rating=0,
                person=scheme_user.UserBase(email=user_add_1.email),
                restaurant=fake_rest,
            ),
        )

    # Delete Assessments
    assert 1 == restBewertung.delete_bewertung(db_session, user_add_1, rest_add_1)
    assert restBewertung.get_bewertung_from_user_to_rest(db_session, user_add_1, rest_add_1) is None
    assert 0 == restBewertung.delete_bewertung(db_session, user_add_1, rest_add_1)
    assert 0 == restBewertung.delete_bewertung(db_session, fake_user, rest_add_2)
    assert 0 == restBewertung.delete_bewertung(db_session, user_add_1, fake_rest)

    # Test if only one comment for the same restaurant an user are possible
    with pytest.raises(DuplicateEntry):
        restBewertung.create_bewertung(db_session, assessment_add_2_2)


def test_recipe_bewertung(db_session: SessionTesting):
    fake_user = scheme_user.UserBase(email="fake@nope.ok")
    fake_rest = scheme_recipe.RecipeBase(id="884488")
    user_add_1 = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    recipe_1 = scheme_recipe.RecipeBase(id="1234")
    recipe_2 = scheme_recipe.RecipeBase(id="6789")

    # Add user
    create_user(db_session, user_add_1)
    create_user(db_session, user_add_2)

    # Add assessment to user1 and recipe1
    assessment_add_1_1 = scheme_recipe.RecipeBewertungCreate(
        name="Rest 1 1", comment="This is a comment", rating=1.5, person=user_add_1, recipe=recipe_1
    )
    assessment_ret = recipeBewertung.create_bewertung(db_session, assessment_add_1_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user1 and rest2
    assessment_add_1_2 = scheme_recipe.RecipeBewertungCreate(
        name="Rest 1 2", comment="This is a comment for rest 2", rating=2.5, person=user_add_1, recipe=recipe_2
    )
    assessment_ret = recipeBewertung.create_bewertung(db_session, assessment_add_1_2)
    assert assessment_ret.kommentar == assessment_add_1_2.comment
    assert assessment_ret.rating == assessment_add_1_2.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user2 and rest2
    assessment_add_2_2 = scheme_recipe.RecipeBewertungCreate(
        name="Rest 2 2", comment="This is a comment 2", rating=3.5, person=user_add_2, recipe=recipe_2
    )
    assessment_ret = recipeBewertung.create_bewertung(db_session, assessment_add_2_2)
    assert assessment_ret.kommentar == assessment_add_2_2.comment
    assert assessment_ret.rating == assessment_add_2_2.rating
    assert assessment_ret.zeitstempel is not None

    # Get all assessments
    assessments_ret = recipeBewertung.get_all_user_bewertungen(db_session, user_add_1)
    assert len(assessments_ret) == 2

    assessments_ret = recipeBewertung.get_all_user_bewertungen(db_session, user_add_2)
    assert len(assessments_ret) == 1

    # Get one assessment from one user to one rest
    assessment_ret = recipeBewertung.get_bewertung_from_user_to_recipe(db_session, user_add_1, recipe_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Update assessment
    updated_1_1 = assessment_add_1_1.copy()
    updated_1_1.comment = "UPDATED"
    updated_1_1.rating = 0
    assessment_ret = recipeBewertung.update_assessment(db_session, assessment_add_1_1, updated_1_1)
    assert assessment_ret.kommentar == updated_1_1.comment
    assert assessment_ret.rating == updated_1_1.rating
    assert assessment_ret.person_email == updated_1_1.person.email
    assert assessment_ret.rezept_id == updated_1_1.recipe.id

    # Try to get assessments that does not exist
    assessment_ret = recipeBewertung.get_all_user_bewertungen(db_session, fake_user)
    assert assessment_ret is None

    assessment_ret = recipeBewertung.get_bewertung_from_user_to_recipe(db_session, fake_user, recipe_1)
    assert assessment_ret is None

    assessment_ret = recipeBewertung.get_bewertung_from_user_to_recipe(db_session, user_add_1, fake_rest)
    assert assessment_ret is None

    # Try to add assessments with invalid user
    with pytest.raises(UserNotFound):
        assessment_ret = recipeBewertung.create_bewertung(
            db_session,
            scheme_recipe.RecipeBewertungCreate(
                name="Rest 1 1", comment="This is a comment", rating=1.5, person=fake_user, recipe=recipe_1
            ),
        )

    # Delete Assessments
    assert 1 == recipeBewertung.delete_bewertung(db_session, user_add_1, recipe_1)
    assert recipeBewertung.get_bewertung_from_user_to_recipe(db_session, user_add_1, recipe_1) is None
    assert 0 == recipeBewertung.delete_bewertung(db_session, user_add_1, recipe_1)
    assert 0 == recipeBewertung.delete_bewertung(db_session, fake_user, recipe_2)
    assert 0 == recipeBewertung.delete_bewertung(db_session, user_add_1, fake_rest)

    # Test if only one comment for the same restaurant an user are possible
    with pytest.raises(DuplicateEntry):
        recipeBewertung.create_bewertung(db_session, assessment_add_2_2)


def test_filterRest(db_session: SessionTesting, add_allergies, add_cuisines):
    # set data
    person1 = UserCreate(email="bla@ka.de", password="password")
    create_user(db_session, person1)

    allergies = [scheme_allergie.PydanticAllergies(name=Allergies.LACTOSE.value)]
    cuisines = [
        scheme_cuisine.PydanticCuisine(name=Cuisine.GERMAN.value),
        scheme_cuisine.PydanticCuisine(name=Cuisine.DOENER.value),
    ]
    filterRest_person1 = scheme_filter.FilterRestDatabase(
        cuisines=cuisines, allergies=allergies, rating=3, costs=3, radius=5000, zipcode=88069
    )

    # Try with Allergies
    filterRest_return = create_filterRest(db_session, filterRest_person1, person1)
    assert person1.email == filterRest_return.person.email
    assert person1.email == filterRest_return.email
    assert filterRest_person1.zipcode == filterRest_return.zipcode
    assert filterRest_person1.radius == filterRest_return.radius
    assert filterRest_person1.rating == filterRest_return.rating
    # assert filterRest_person1.cuisines.value == filterRest_return.cuisine

    # Try without Allergies
    person2 = UserCreate(email="blab2@ka.de", password="geheim")
    filterRest_person2 = filterRest_person1.copy()
    create_user(db_session, person2)
    try:
        filterRest_person2.allergies = None
        create_filterRest(db_session, filterRest_person2, person2)
    except Exception as error:
        assert False, f"'create_filter raised exception {error}"

    # Try with none existing user
    person_fail = UserBase(email="nope@ok.de")
    filterRest_fail = filterRest_person1.copy()
    with pytest.raises(UserNotFound):
        create_filterRest(db_session, filterRest_fail, person_fail)

    # Update Filter from person1
    filterRest_update = scheme_filter.FilterRestDatabase(
        cuisines=[scheme_cuisine.PydanticCuisine(name=Cuisine.GERMAN.value)],
        allergies=allergies,
        rating=1,
        costs=1,
        radius=1444,
        zipcode=88069,
    )
    filterRest_return = update_filterRest(db_session, updated_filter=filterRest_update, user=person1)
    assert person1.email == filterRest_return.person.email
    assert person1.email == filterRest_return.email
    assert filterRest_update.zipcode == filterRest_return.zipcode
    assert filterRest_update.radius == filterRest_return.radius
    assert filterRest_update.rating == filterRest_return.rating
    # assert filterRest_update.cuisines.value == filterRest_return.cuisine

    # Try updated with non existing User
    with pytest.raises(UserNotFound):
        update_filterRest(db_session, updated_filter=filterRest_person1, user=person_fail)

    # Only one filterRest for one Person
    with pytest.raises(DuplicateEntry):
        create_filterRest(db_session, filterRest_person1, person1)


def test_allergie_add(db_session: SessionTesting):
    for allergie in Allergies:
        added_allergie = create_allergie(db_session, allergie)
        assert allergie.value == added_allergie.name


def test_cuisine_add(db_session: SessionTesting):
    for cuisine in Cuisine:
        added_allergie = create_cuisine(db_session, cuisine)
        assert cuisine.value == added_allergie.name
