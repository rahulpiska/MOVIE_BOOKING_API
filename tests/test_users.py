import pytest

@pytest.mark.users
def test_create_user(client):

    response = client.post("/users",
                           json={
                               "name":"User",
                               "email":"user@gmail.com",
                               "password":"user123"
                           }
                        )

    assert response.status_code == 200
    assert response.json()["name"] == "User"
    assert response.json()["email"] == "user@gmail.com"


@pytest.mark.users
def test_create_duplicate_user(client):

    response1 = client.post("/users",
                           json={
                               "name":"User",
                               "email":"user@gmail.com",
                               "password":"user123"
                           }
                        )

    assert response1.status_code == 200
    assert response1.json()["name"] == "User"
    assert response1.json()["email"] == "user@gmail.com"


    response2 = client.post("/users",
                           json={
                               "name":"User",
                               "email":"user@gmail.com",
                               "password":"user123"
                           }
                        )

    assert response2.status_code == 400
    assert response2.json()["detail"] == "User with this email already exists"



@pytest.mark.users
def test_create_user_with_invalid_email(client):

    response = client.post("/users",
                           json={
                               "name":"User",
                               "email": "admingmail",
                               "password": "user123"
                           }
                        )

    assert response.status_code == 422


@pytest.mark.users
def test_create_user_with_missing_fields(client):

    response = client.post("/users",
                           json={
                               "email":"user@gmail",
                               "password":"user123"
                           }
                        )

    assert response.status_code == 422




