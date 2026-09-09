import pytest

@pytest.mark.theaters
def test_create_theater(create_theater):

    theater = create_theater("AMB cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB cinemas"


@pytest.mark.theaters
def test_create_duplicate_theater(create_theater):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    response = create_theater("amb_cinemas")

    assert response.status_code == 400
    assert response.json()["detail"] == "Theater already exists with this name"


@pytest.mark.theaters
def test_create_theater_using_normal_user_login(client, normal_auth_headers):

    response = client.post("/theaters",
                           headers=normal_auth_headers,
                           json={
                               "name":"AMB cinemas"
                           }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.theaters
def test_create_theater_with_missing_fields(client, admin_auth_headers):

    response = client.post("/theaters",
                           headers=admin_auth_headers)

    assert response.status_code == 422


@pytest.mark.theaters
def test_create_theater_without_login(client):

    response = client.post("/theaters",
                           json={
                               "name":"AAA_cinemas"
                           }
                        )

    assert response.status_code == 401



@pytest.mark.theaters
def test_get_theaters(client, create_theater):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    response = client.get("/theaters")

    assert response.status_code == 200
    data = response.json()

    assert data[0]["name"] == "AMB_cinemas"


@pytest.mark.theaters
def test_get_theaters_with_empty_db(client):

    response = client.get("/theaters")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.theaters
def test_get_theater_by_id(client, create_theater):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.get(f"/theaters/{theater_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "AMB_cinemas"


@pytest.mark.theaters
def test_get_non_exist_theater_by_id(client):

    response = client.get("/theaters/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Theater not found"


@pytest.mark.theaters
def test_get_theater_using_invalid_theater_id(client):

    response = client.get("/theaters/abc")

    assert response.status_code == 422

#---------------------

@pytest.mark.theaters
def test_update_theater(client, create_theater, admin_auth_headers):

    theater = create_theater("PVR_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_cinemas"

    theater_id = theater.json()["id"]

    response = client.put(f"/theaters/{theater_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":"PVR_malakpet"
                          })


    assert response.status_code == 200
    assert response.json()["name"] == "PVR_malakpet"

    get_response = client.get(f"/theaters/{theater_id}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "PVR_malakpet"


@pytest.mark.theaters
def test_update_theater_with_normal_user(client, create_theater, normal_auth_headers):

    theater = create_theater("INOX_kukatpally")

    assert theater.status_code == 200
    assert theater.json()["name"] == "INOX_kukatpally"

    theater_id = theater.json()["id"]

    response = client.put(f"/theaters/{theater_id}",
                          headers=normal_auth_headers,
                          json={
                              "name":"INOX_Kukatpally"
                          }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"



@pytest.mark.theaters
def test_update_theater_to_duplicate(client, create_theater, admin_auth_headers):

    theater_1 = create_theater("PVR_cinemas")

    assert theater_1.status_code == 200
    assert theater_1.json()["name"] == "PVR_cinemas"

    theater_2 = create_theater("PVR_khairatabad")

    assert theater_2.status_code == 200
    assert theater_2.json()["name"] == "PVR_khairatabad"

    theater_id = theater_2.json()["id"]

    response = client.put(f"/theaters/{theater_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":"pvr_cinemas"
                          }
                        )


    assert response.status_code == 400
    assert response.json()["detail"] == "Theater with this name already exists"


@pytest.mark.theaters
def test_update_non_exist_theater(client, admin_auth_headers):

    response = client.put("/theaters/99999",
                          headers=admin_auth_headers,
                          json={
                              "name":"INOX_kukatpally"
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Theater not found"


@pytest.mark.theaters
def test_update_theater_by_invalid_id(client, admin_auth_headers):

    response = client.put("/theaters/abvc",
                          headers=admin_auth_headers,
                          json={
                              "name":"INOX_kukatpally"
                          }
                        )

    assert response.status_code == 422


@pytest.mark.theaters
def test_update_theater_without_login(client, create_theater):

    theater = create_theater("PVR_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_cinemas"

    theater_id = theater.json()["id"]

    response = client.put(f"/theaters/{theater_id}",
                          json={
                              "name":"PVR_malakpet"
                          }
                        )


    assert response.status_code == 401



@pytest.mark.theaters
def test_update_theater_with_invalid_data(client, create_theater, admin_auth_headers):

    theater = create_theater("PVR_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_cinemas"

    theater_id = theater.json()["id"]

    response = client.put(f"/theaters/{theater_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":23212
                          }
                        )


    assert response.status_code == 422


#---------------------

@pytest.mark.theaters
def test_delete_theater(client, create_theater, admin_auth_headers):

    theater = create_theater("PVR_kukatpally")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_kukatpally"

    theater_id = theater.json()["id"]

    response = client.delete(f"/theaters/{theater_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Theater deleted successfully"

    get_response = client.get(f"/theaters/{theater_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Theater not found"



@pytest.mark.theaters
def test_delete_non_exist_theater(client,admin_auth_headers):

    response = client.delete("/theaters/99999",
                             headers=admin_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Theater not found"


@pytest.mark.theaters
def test_delete_theater_with_normal_user(client, normal_auth_headers, create_theater):

    theater = create_theater("PVR_kukatpally")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_kukatpally"

    theater_id = theater.json()["id"]

    response = client.delete(f"/theaters/{theater_id}",
                             headers=normal_auth_headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"



@pytest.mark.theaters
def test_delete_theater_without_login(client, create_theater):

    theater = create_theater("PVR_kukatpally")

    assert theater.status_code == 200
    assert theater.json()["name"] == "PVR_kukatpally"

    theater_id = theater.json()["id"]

    response = client.delete(f"/theaters/{theater_id}")

    assert response.status_code == 401


@pytest.mark.theaters
def test_delete_theater_using_invalid_id(client, admin_auth_headers):

    response = client.delete("/theaters/abdc",
                             headers=admin_auth_headers)

    assert response.status_code == 422


@pytest.mark.theaters
def test_delete_theater_having_screen(client, create_theater, create_screen, admin_auth_headers):

    screen = create_screen("PVR_cinemas","Screen_id",2,2)

    theater_id = screen.json()["theater_id"]

    assert screen.status_code == 200

    response = client.delete(f"/theaters/{theater_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "theater has screens"

