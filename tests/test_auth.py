import pytest

from conftest import NORMAL_EMAIL

@pytest.mark.auth
def test_login(client):

    create_user = client.post("/users",
                              json={
                                  "name":"User",
                                  "email":"user@gmail.com",
                                  "password":"user123"
                              }
                            )

    assert create_user.status_code == 200
    assert create_user.json()["email"] == "user@gmail.com"


    user_login = client.post("/auth/login",
                             data={
                                 "username":"user@gmail.com",
                                 "password":"user123"
                             }
                            )


    assert user_login.status_code == 200

    data = user_login.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.auth
def test_login_non_existing_user(client):

    user_login = client.post("/auth/login",
                             data={
                                 "username":"tony@gmail.com",
                                 "password":"tony123"
                             }
                            )

    assert user_login.status_code == 401
    assert user_login.json()["detail"] == "Invalid credintials"



@pytest.mark.auth
def test_login_using_wrong_password(client):

    create_user = client.post("/users",
                              json={
                                  "name":"User",
                                  "email":"user@gmail.com",
                                  "password":"user123"
                              }
                            )

    assert create_user.status_code == 200
    assert create_user.json()["email"] == "user@gmail.com"


    user_login = client.post("/auth/login",
                             data={
                                 "username":"user@gmail.com",
                                 "password":"no_password"
                             }
                            )

    assert user_login.status_code == 401
    assert user_login.json()["detail"] == "Invalid credintials"


@pytest.mark.auth
def test_login_without_email(client):

    response = client.post("/auth/login",
                             data={
                                 "password":"user123"
                             }
                            )

    assert response.status_code == 422


@pytest.mark.auth
def test_login_without_password(client):

    response = client.post("/auth/login",
                             data={
                                 "username":"user@gmail.com"
                             }
                            )

    assert response.status_code == 422
    



@pytest.mark.auth
def test_get_user_using_token(client, normal_auth_headers):

    response = client.get("/auth/me",
                          headers=normal_auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == NORMAL_EMAIL
    assert response.json()["is_admin"] == False



@pytest.mark.auth
def test_get_user_without_token(client):

    response = client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.auth
def test_get_user_with_invalid_token(client):

    fake_token = "fsjforoerjerorjnrfognr"

    response = client.get("/auth/me",
                          headers={
                              "Authorization": f"Bearer {fake_token}"
                            }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid token"

