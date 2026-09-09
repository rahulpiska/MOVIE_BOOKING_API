import pytest
from models import Seat


@pytest.mark.screens
def test_create_screen(client, create_theater, admin_auth_headers):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 200
    assert response.json()["name"] == "Screen_1"
    assert response.json()["theater_id"] == theater_id



@pytest.mark.screens
def test_create_duplicate_screen(client, create_theater, admin_auth_headers):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    screen = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert screen.status_code == 200
    assert screen.json()["name"] == "Screen_1"
    assert screen.json()["theater_id"] == theater_id

    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"screen_1",
                               "theater_id": theater_id,
                               "rows":4,
                               "seats_per_row":4
                            }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Screen with this name already exists"


@pytest.mark.screens
def test_create_screen_using_invalid_theater_id(client, admin_auth_headers):

    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":999999,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid theater id"


@pytest.mark.screens
def test_create_screen_without_login(client, create_theater):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.post("/screens",
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 401


@pytest.mark.screens
def test_create_screen_with_missing_fields(client, create_theater, admin_auth_headers):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 422


@pytest.mark.screens
def test_create_screen_using_normal_user(client, create_theater, normal_auth_headers):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.post("/screens",
                           headers=normal_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.screens
def test_create_screen_with_invalid_theater_id_type(client, create_theater, admin_auth_headers):

    theater = create_theater("AMB_cinemas")

    assert theater.status_code == 200
    assert theater.json()["name"] == "AMB_cinemas"

    theater_id = theater.json()["id"]

    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id": "acrev",
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert response.status_code == 422


@pytest.mark.screens
def test_create_same_screen_with_different_theater_ids(client, create_theater, admin_auth_headers):

    theater_1 = create_theater("AMB_cinemas")

    assert theater_1.status_code == 200
    assert theater_1.json()["name"] == "AMB_cinemas"

    theater_1_id = theater_1.json()["id"]

    screen_1 = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_1_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert screen_1.status_code == 200
    assert screen_1.json()["name"] == "Screen_1"
    assert screen_1.json()["theater_id"] == theater_1_id


    theater_2 = create_theater("PVR_cinemas")

    assert theater_2.status_code == 200
    assert theater_2.json()["name"] == "PVR_cinemas"

    theater_2_id = theater_2.json()["id"]

    screen_2 = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_2_id,
                               "rows":3,
                               "seats_per_row":4
                           }
                        )

    assert screen_2.status_code == 200
    assert screen_2.json()["name"] == "Screen_1"
    assert screen_2.json()["theater_id"] == theater_2_id



@pytest.mark.parametrize("field,value", [
    ("rows", 0),
    ("rows", -1),
    ("seats_per_row", 0),
    ("seats_per_row", -1)
])

@pytest.mark.screens
def test_create_screen_with_invalid_seat_dimensions(client, create_theater, admin_auth_headers, field, value):

    theater = create_theater("PVR_cinemas")
    theate_id = theater.json()["id"]

    data = {
        "name":"Screen_1",
        "theater_id":theate_id,
        "rows":3,
        "seats_per_row":4
    }

    data[field] = value


    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json=data)

    assert response.status_code == 422


@pytest.mark.screens
def test_create_screen_creates_seats(client, create_theater, admin_auth_headers, db_session):

    theater = create_theater("AAA_cinemas")
    theater_id = theater.json()["id"]


    response = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_1",
                               "theater_id":theater_id,
                               "rows":2,
                               "seats_per_row":2
                           }
                        )

    assert response.status_code == 200

    screen_id = response.json()["id"]

    seats = db_session.query(Seat).filter(
        Seat.screen_id == screen_id
    ).all()

    assert len(seats) == 4

    seats_numbers = {seat.seat_number for seat in seats}

    assert seats_numbers == {
        "A1","A2",
        "B1","B2"
    }


@pytest.mark.screens
def test_get_screens(client, create_screen):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)

    response = client.get("/screens")

    assert response.status_code == 200
    data = response.json()

    assert any(
        item["id"] == screen.json()["id"]
        and item["name"] == screen.json()["name"]
        for item in data
    )

@pytest.mark.screens
def test_get_screens_in_empty_db(client):

    response = client.get("/screens")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.screens
def test_get_screen_by_id(client, create_screen):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.get(f"/screens/{screen_id}")

    assert response.status_code == 200
    assert response.json()["name"] == screen.json()["name"]

@pytest.mark.screens
def test_get_non_exist_screen(client):


    response = client.get("/screens/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Screen not found"


@pytest.mark.screens
def test_get_screen_by_Invalid_id_type(client):

    response = client.get("/screens/abcd")

    assert response.status_code == 422



@pytest.mark.screens
def test_update_screen(client, admin_auth_headers, create_screen):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":"Screen_2"
                          }
                        )

    assert response.status_code == 200
    assert response.json()["name"] == "Screen_2"



@pytest.mark.screens
def test_update_screen_using_invalid_id(client, admin_auth_headers):

    response = client.put("/screens/99999",
                          headers=admin_auth_headers,
                          json={
                              "name":"Screen_1"
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Screen not found"


@pytest.mark.screens
def test_update_screen_without_login(client, create_screen):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          json={
                              "name":"Screen_2"
                          }
                        )

    assert response.status_code == 401

@pytest.mark.screens
def test_update_screen_using_normal_user(client, create_screen, normal_auth_headers):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          headers=normal_auth_headers,
                          json={
                              "name":"Screen_2"
                          }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"



@pytest.mark.screens
def test_update_screen_with_invalid_screen_id_type(client, admin_auth_headers, create_screen):

    response = client.put("/screens/acbd",
                          headers=admin_auth_headers,
                          json={
                              "name":"Screen_1"
                          }
                        )

    assert response.status_code == 422


@pytest.mark.screens
def test_update_screen_with_non_exist_theater_id(client, create_screen, admin_auth_headers):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          headers=admin_auth_headers,
                          json={
                              "theater_id":5
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Theater not found"


@pytest.mark.screens
def test_update_screen_to_duplicate(client, admin_auth_headers, create_screen):

    screen_A = create_screen("AAA_cinemas","Screen_1",2,2)
    theater_id = screen_A.json()["theater_id"]

    screen_B = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_2",
                               "theater_id":theater_id,
                               "rows":2,
                               "seats_per_row":2
                           }
                        )
    
    screen_id = screen_B.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":"Screen_1"
                          }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Theater already exists with this screen name"


@pytest.mark.parametrize("field, value",[
    ("name", 432),
    ("theater_id", "abcd")
]
)

@pytest.mark.screens
def test_update_screen_with_invalid_data(client, admin_auth_headers, create_screen, field, value):

    screen = create_screen("AAA_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    data= {
        "name":"Screen_1",
        "theater_id": screen.json()["theater_id"]
    }

    data[field] = value

    response = client.put(f"/screens/{screen_id}",
               headers=admin_auth_headers,
               json=data)

    assert response.status_code == 422


@pytest.mark.screens
def test_update_screen_to_duplicate_name_in_different_theater(client, create_screen, admin_auth_headers):

    screen_A = create_screen("AAA_cinemas","Screen_1",2,2)

    screen_B = create_screen("PVR_cinemas","Screen_2",2,2)
    screen_id = screen_B.json()["id"]

    response = client.put(f"/screens/{screen_id}",
                          headers=admin_auth_headers,
                          json={
                              "name":"Screen_1"
                          }
                        )

    assert response.status_code == 200
    assert response.json()["name"] == "Screen_1"

#--------------------

@pytest.mark.screens
def test_delete_screens(client, create_screen, admin_auth_headers):

    screen = create_screen("PVR_cinemas","Screen_1",2,2)
    screen_id = screen.json()["id"]

    response = client.delete(f"/screens/{screen_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Screen deleted successfully"

    get_response = client.get(f"/screens/{screen_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Screen not found"


@pytest.mark.screens
def test_delete_non_exist_screen(client, admin_auth_headers):

    response = client.delete("/screens/99999",
                             headers=admin_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Screen not found"


@pytest.mark.screens
def test_delete_screen_using_normal_user(client, create_screen, normal_auth_headers):

    screen = create_screen("AMB_cinemas","Screen_1",2,3)
    screen_id = screen.json()["id"]

    response = client.delete(f"/screens/{screen_id}",
                             headers=normal_auth_headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.screens
def test_delete_screen_without_login(client,create_screen):

    screen = create_screen("AAA_cinemas","Screen_1",2,3)
    screen_id = screen.json()["id"]

    response = client.delete(f"/screens/{screen_id}")

    assert response.status_code == 401



@pytest.mark.screens
def test_delete_screen_using_invalid_id_type(client, create_screen, admin_auth_headers):

    screen = create_screen("AAA_cinemas","Screen_1",2,3)
    screen_id = screen.json()["id"]

    response = client.delete("/screens/abg",
                             headers=admin_auth_headers)

    assert response.status_code == 422


@pytest.mark.screens
def test_delete_screen_having_shows(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    screen = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    screen_id = screen.json()["id"]

    client.post("/shows",
                    headers=admin_auth_headers,
                    json={
                        "movie_id":movie.json()["id"],
                        "screen_id":screen.json()["id"],
                        "start_time":"2027-03-15T09:30:00",
                        "ticket_price":300
                    }
                )


    response = client.delete(f"/screens/{screen_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Screen has shows"

