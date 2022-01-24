import pytest
from db import crud, db_models
from schemes import scheme_rest, scheme_user
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
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
    rest_add = scheme_rest.BaseRestaurant(place_id="1234")
    rest_return = crud.create_restaurant(db_session, rest_add)
    assert rest_add == scheme_rest.BaseRestaurant(**rest_return.__dict__)

    # add the second restaurant
    rest_add_2 = scheme_rest.BaseRestaurant(place_id="567")
    rest_return = crud.create_restaurant(db_session, rest_add_2)
    assert rest_add_2 == scheme_rest.BaseRestaurant(**rest_return.__dict__)

    # Get one Restaurant
    rest_return = crud.get_restaurant_by_id(db_session, rest_add.place_id)
    assert rest_add == scheme_rest.BaseRestaurant(**rest_return.__dict__)

    # Get all Restaurants
    rests_return = crud.get_all_restaurants(db_session)
    rests_return_schemes = [scheme_rest.BaseRestaurant(**rest.__dict__) for rest in rests_return]
    assert rests_return_schemes == [rest_add, rest_add_2]

    # Delete that Restaurant
    affected_rows = crud.delete_restaurant(db_session, rest_add.place_id)
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
    user_ret = crud.update_user(db_session, user_add.email, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Update User email
    tmp_user = user_add.copy()
    user_add.email = "new@mail.test"
    user_ret = crud.update_user(db_session, tmp_user.email, user_add)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Get one User
    user_ret = crud.get_user_by_mail(db_session, user_add.email)
    assert user_add.email == user_ret.email
    assert Hasher.verify_password(user_add.password, user_ret.hashed_password)

    # Delete one User
    assert 1 == crud.delete_user_by_mail(db_session, user_add_2.email)

    # Chek if only one user with the same email can be added
    with pytest.raises(exc.SQLAlchemyError):
        crud.create_user(db_session, user_add)


def test_bewertung(db_session: SessionTesting):
    # Add user
    user_add = scheme_user.UserCreate(email="test1@demo.lol", password="password1")
    user_add_2 = scheme_user.UserCreate(email="test2@demo.lol", password="password2")
    crud.create_user(db_session, user_add)
    crud.create_user(db_session, user_add_2)

    # Add restaurant
    rest_add = scheme_rest.BaseRestaurant(place_id="1234")
    rest_add_2 = scheme_rest.BaseRestaurant(place_id="5678")
    crud.create_restaurant(db_session, rest_add)
    crud.create_restaurant(db_session, rest_add_2)

    # Add assessment to user1 and rest1
    assessment_add_1_1 = scheme_rest.RestBewertungCreate(
        comment="This is a comment", rating=1.5, person=user_add, restaurant=rest_add
    )
    assessment_ret = crud.create_bewertung(db_session, assessment_add_1_1)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Add assessment to user1 and rest2
    assessment_add_1_2 = scheme_rest.RestBewertungCreate(
        comment="This is a comment for rest 2", rating=2.5, person=user_add, restaurant=rest_add_2
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
    assessments_ret = crud.get_all_user_bewertungen(db_session, user_add)
    assert len(assessments_ret) == 2

    assessments_ret = crud.get_all_user_bewertungen(db_session, user_add_2)
    assert len(assessments_ret) == 1

    # Get one assessment from one user to one rest
    assessment_ret = crud.get_bewertung_from_user_to_rest(db_session, user_add, rest_add)
    assert assessment_ret.kommentar == assessment_add_1_1.comment
    assert assessment_ret.rating == assessment_add_1_1.rating
    assert assessment_ret.zeitstempel is not None

    # Try to get assessments that does not exist
    assessment_ret = crud.get_all_user_bewertungen(db_session, scheme_user.UserBase(email="nope@nice.de"))
    assert len(assessment_ret) == 0

    assessment_ret = crud.get_bewertung_from_user_to_rest(
        db_session, scheme_user.UserBase(email="nope@nice.de"), rest_add
    )
    assert assessment_ret is None

    assessment_ret = crud.get_bewertung_from_user_to_rest(
        db_session, user_add, scheme_rest.BaseRestaurant(place_id="0000000")
    )
    assert assessment_ret is None

    # Try to add assessments with invalid user and restaurant
    fake_user = scheme_user.UserBase(email="fake@nope.ok")
    fake_rest = scheme_rest.BaseRestaurant(place_id="000000")

    with pytest.raises(exc.SQLAlchemyError):
        assessment_ret = crud.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(comment="none", rating=0, person=fake_user, restaurant=rest_add),
        )

    with pytest.raises(exc.SQLAlchemyError):
        assessment_ret = crud.create_bewertung(
            db_session,
            scheme_rest.RestBewertungCreate(
                comment="none",
                rating=0,
                person=scheme_user.UserBase(email=user_add.email),
                restaurant=fake_rest,
            ),
        )

    # Test if only one comment for the same restaurant an user are possible
    with pytest.raises(exc.SQLAlchemyError):
        crud.create_bewertung(db_session, assessment_add_1_1)
        pass
