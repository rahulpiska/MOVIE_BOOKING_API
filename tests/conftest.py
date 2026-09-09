import pytest
from testing_database import test_engine, TestSessionLocal

from fastapi.testclient import TestClient

from main import app
from database import get_db

from utils import hash_password
from models import User


#-----------------------------------------------------------------------

@pytest.fixture
def db_session():

    connection = test_engine.connect()
    transaction = connection.begin()

    db = TestSessionLocal(bind=connection)

    try:
        yield db

    finally:
        db.close()
        transaction.rollback()
        connection.close()



@pytest.fixture
def client(db_session):

    def get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


#-----------------------------------------------------------------------
#ADMIN USER 

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123" 

@pytest.fixture
def admin_user(db_session):

    db = db_session  

    new_admin = User(
        name = "Admin",
        email = ADMIN_EMAIL,
        password = hash_password(ADMIN_PASSWORD),
        is_admin = True
    )

    db.add(new_admin)

    db.commit()
    db.refresh(new_admin)

    return new_admin



@pytest.fixture
def admin_login(client, admin_user):

    response = client.post("/auth/login",
                           data={
                               "username":ADMIN_EMAIL,
                               "password":ADMIN_PASSWORD
                           }
                        )

    assert response.status_code == 200

    return response

    
@pytest.fixture
def admin_auth_headers(admin_login):

    login_data = admin_login.json()

    token = login_data["access_token"]

    return{
        "Authorization": f"Bearer {token}"
    }



#----------------------------------------------------------------------
#normal user

NORMAL_EMAIL = "tony@gmail.com"
NORMAL_PASSWORD = "tony@123" 

@pytest.fixture
def normal_user(db_session):

    db = db_session

    new_user = User(
        name= "tony",
        email = NORMAL_EMAIL,
        password = hash_password(NORMAL_PASSWORD)  
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user


@pytest.fixture
def normal_login(client, normal_user):

    response = client.post("/auth/login",
                           data={
                               "username":NORMAL_EMAIL,
                               "password":NORMAL_PASSWORD
                           }
                        )

    assert response.status_code == 200

    return response


@pytest.fixture
def normal_auth_headers(normal_login):

    login_data = normal_login.json()

    token = login_data["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }



#============================================================================

@pytest.fixture
def create_movie(client,admin_auth_headers):
    def _create_category(title, description, language, genre, duration_minutes, release_date):

        response = client.post("/movies",
                               headers=admin_auth_headers,
                               json={
                                   "title":title,
                                   "description":description,
                                   "language":language,
                                   "genre": genre,
                                   "duration_minutes":duration_minutes,
                                   "release_date":release_date

                               }
                            )

        return response
    return _create_category


@pytest.fixture
def create_theater(client, admin_auth_headers):

    def _create_theater(name):

        response = client.post("/theaters",
                               headers=admin_auth_headers,
                               json={
                                   "name":name
                               }
                            )

        return response
    return _create_theater


@pytest.fixture
def create_screen(client, create_theater, admin_auth_headers):

    def _create_screen(theater_name, screen_name, rows, seats_per_row):

        theater = create_theater(theater_name)
        theater_id = theater.json()["id"]

        response = client.post("/screens",
                               headers=admin_auth_headers,
                               json={
                                   "name":screen_name,
                                   "theater_id":theater_id,
                                   "rows":rows,
                                   "seats_per_row":seats_per_row
                               }
                            )

        return response
    return _create_screen