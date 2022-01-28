import pytest
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from db import crud
from db import db_models
from schemes import scheme_rest
from schemes import scheme_user
from tools.hashing import Hasher

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_models.Base.metadata.create_all(bind=engine)


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


def test_restaurant(db_session: SessionTesting):

    # Add two Restaurants
    # add the first restaurant
    rest_add = scheme_rest.RestaurantBase(place_id="1234")
    rest_return = crud.create_restaurant(db_session, rest_add)
    assert rest_add == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # add the second restaurant
    rest_add_2 = scheme_rest.RestaurantBase(place_id="567")
    rest_return = crud.create_restaurant(db_session, rest_add_2)
    assert rest_add_2 == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # Get one Restaurant
    rest_return = crud.get_restaurant_by_id(db_session, rest_add.place_id)
    assert rest_add == scheme_rest.RestaurantBase(**rest_return.__dict__)

    # Get all Restaurants
    rests_return = crud.get_all_restaurants(db_session)
    rests_return_schemes = [scheme_rest.RestaurantBase(**rest.__dict__) for rest in rests_return]
    assert rests_return_schemes == [rest_add, rest_add_2]

    # Delete that Restaurant
    affected_rows = crud.delete_restaurant(db_session, rest_add)
    assert affected_rows == 1
    assert crud.get_restaurant_by_id(db_session, rest_add.place_id) is None

    # Check if you cant add the same restaurant twice
    with pytest.raises(exc.SQLAlchemyError):
        crud.create_restaurant(db_session, rest_add_2)


def test_user(db_session: SessionTesting):
    # Add two users
    # ...first user
    user_add = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_ret = crud.create_user(db_session, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # ..second user
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    user_ret = crud.create_user(db_session, user_add_2)
    assert user_add_2.email == user_ret.email
    assert Hasher.verify_password(user_add_2.password, user_ret.hashed_password)

    # Update User password
    user_add.password = "new_password"
    user_ret = crud.update_user(db_session, user_add, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Update User email
    tmp_user = user_add.copy()
    user_add.email = "new@mail.test"
    user_ret = crud.update_user(db_session, tmp_user, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Get one User
    user_ret = crud.get_user_by_mail(db_session, user_add.email)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Delete one User
    assert 1 == crud.delete_user(db_session, user_add_2)

    # Chek if only one user with the same email can be added
    with pytest.raises(exc.SQLAlchemyError):
        crud.create_user(db_session, user_add)


def test_bewertung(db_session: SessionTesting):
    fake_user = scheme_user.UserBase(email="fake@nope.ok")
    fake_rest = scheme_rest.RestaurantBase(place_id="000000")
    user_add_1 = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    rest_add_1 = scheme_rest.RestaurantBase(place_id="1234")
    rest_add_2 = scheme_rest.RestaurantBase(place_id="5678")

    # Add user
    crud.create_user(db_session, user_add_1)
    crud.create_user(db_session, user_add_2)

    # Add restaurant
    crud.create_restaurant(db_session, rest_add_1)
    crud.create_restaurant(db_session, rest_add_2)

    # Add assessment to user1 and rest1
    assessment_add_1_1 = scheme_rest.RestBewertungCreate(
        comment="This is a comment", rating=1.5, person=user_add_1, restaurant=rest_add_1
    )
    assessment_ret = crud.create_bewertung(db_session, assessment_add_1_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user1 and rest2
    assessment_add_1_2 = scheme_rest.RestBewertungCreate(
        comment="This is a comment for rest 2", rating=2.5, person=user_add_1, restaurant=rest_add_2
    )
    assessment_ret = crud.create_bewertung(db_session, assessment_add_1_2)
    assert assessment_ret.kommentar == assessment_add_1_2.comment
    assert assessment_ret.rating == assessment_add_1_2.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user2 and rest2
    assessment_add_2_2 = scheme_rest.RestBewertungCreate(
        comment="This is a comment 2", rating=3.5, person=user_add_2, restaurant=rest_add_2
    )
    assessment_ret = crud.create_bewertung(db_session, assessment_add_2_2)
    assert assessment_ret.kommentar == assessment_add_2_2.comment
    assert assessment_ret.rating == assessment_add_2_2.rating
    assert assessment_ret.zeitstempel is not None

    # Get all assessments
    assessments_ret = crud.get_all_user_bewertungen(db_session, user_add_1)
    assert len(assessments_ret) == 2

    assessments_ret = crud.get_all_user_bewertungen(db_session, user_add_2)
    assert len(assessments_ret) == 1

    # Get one assessment from one user to one rest
    assessment_ret = crud.get_bewertung_from_user_to_rest(db_session, user_add_1, rest_add_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Update assessment
    updated_1_1 = assessment_add_1_1.copy()
    updated_1_1.comment = "UPDATED"
    updated_1_1.rating = 0
    assessment_ret = crud.update_bewertung(db_session, assessment_add_1_1, updated_1_1)
    assert assessment_ret.kommentar == updated_1_1.comment
    assert assessment_ret.rating == updated_1_1.rating
    assert assessment_ret.person_email == updated_1_1.person.email
    assert assessment_ret.place_id == updated_1_1.restaurant.place_id

    # Try to get assessments that does not exist
    assessment_ret = crud.get_all_user_bewertungen(db_session, fake_user)
    assert assessment_ret is None

    assessment_ret = crud.get_bewertung_from_user_to_rest(db_session, fake_user, rest_add_1)
    assert assessment_ret is None

    assessment_ret = crud.get_bewertung_from_user_to_rest(db_session, user_add_1, fake_rest)
    assert assessment_ret is None

    # Try to add assessments with invalid user and restaurant
    with pytest.raises(exc.SQLAlchemyError):
        assessment_ret = crud.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(comment="none", rating=0, person=fake_user, restaurant=rest_add_1),
        )

    with pytest.raises(exc.SQLAlchemyError):
        assessment_ret = crud.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(
                comment="none", rating=0, person=scheme_user.UserBase(email=user_add_1.email), restaurant=fake_rest
            ),
        )

    # Delete Assessments
    assert 1 == crud.delete_bewertung(db_session, user_add_1, rest_add_1)
    assert crud.get_bewertung_from_user_to_rest(db_session, user_add_1, rest_add_1) is None
    assert 0 == crud.delete_bewertung(db_session, user_add_1, rest_add_1)
    assert 0 == crud.delete_bewertung(db_session, fake_user, rest_add_2)
    assert 0 == crud.delete_bewertung(db_session, user_add_1, fake_rest)

    # Test if only one comment for the same restaurant an user are possible
    with pytest.raises(exc.IntegrityError):
        crud.create_bewertung(db_session, assessment_add_2_2)
