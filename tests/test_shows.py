import pytest
from decimal import Decimal


@pytest.mark.shows
def test_create_show(client,create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    response = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 200
    assert response.json()["start_time"] == "2026-09-24T09:30:00"
    assert response.json()["end_time"] == "2026-09-24T12:30:00"
    assert response.json()["ticket_price"] == "300.00"



@pytest.mark.shows
def test_create_show_using_normal_user(client,create_movie, create_screen, normal_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    response = client.post("/shows",
                           headers=normal_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"



@pytest.mark.shows
def test_create_show_without_login(client,create_movie, create_screen):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    response = client.post("/shows",
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 401



@pytest.mark.shows
def test_create_show_with_non_exist_movie(client, create_screen, admin_auth_headers):


    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    response = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":999999,
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"



@pytest.mark.shows
def test_create_show_with_non_exist_screen(client,create_movie, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )


    response = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":999999,
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Screen not found"


@pytest.mark.shows
def test_create_shows_with_missing_fields(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Spirit",
        "Staring_Prabhas, directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    response = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    assert response.status_code == 422



@pytest.mark.shows
def test_create_show_to_overlap_another_show_timings(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T10:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_2.status_code == 400
    assert show_2.json()["detail"] == "This show overlaps with an existing show on this screen"



@pytest.mark.shows
def test_create_show_to_not_overlap_another_show_timings(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T12:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_2.status_code == 200
    assert show_2.json()["start_time"] == "2027-08-15T12:30:00"
    assert show_2.json()["end_time"] == "2027-08-15T15:30:00"


@pytest.mark.shows
def test_create_show_with_different_screens_with_same_timings(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen_1 = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen_1.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"


    screen_2 = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_2",
                               "theater_id":screen_1.json()["theater_id"],
                               "rows":2,
                               "seats_per_row":2
                           }
                        )

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen_2.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_2.status_code == 200
    assert show_2.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_2.json()["end_time"] == "2027-08-15T12:30:00"



@pytest.mark.parametrize("field, value",[
    ("movie_id", "abcd"),
    ("screen_id", "acd"),
    ("start_time","22-02-2027"),
    ("ticket_price","efe"),
    ("ticket_price", 0),
    ("ticket_price", -100)
])

@pytest.mark.shows
def test_create_shows_with_invalid_data(client, admin_auth_headers,create_movie, create_screen, field, value):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    data ={
        "movie_id":movie.json()["id"],
        "screen_id":screen.json()["id"],
        "start_time":"2026-09-24T09:30:00",
        "ticket_price":300
    }

    data[field] = value

    response = client.post("/shows",
                           headers=admin_auth_headers,
                           json=data)

    assert response.status_code == 422


@pytest.mark.shows
def test_get_shows(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Avengers",
        "Endgame encore",
        "Telugu",
        "Sci-fi",
        180,
        "2026-09-25"
    )

    screen = create_screen("INOX_kothapet","Screen_1",2,3)

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2026-09-25T09:30:00",
                           "ticket_price":450
                       }
                    )

    response = client.get("/shows")

    assert response.status_code == 200
    data = response.json()

    assert any(
    item["start_time"] == "2026-09-25T09:30:00"
    and item["end_time"] == "2026-09-25T12:30:00"
    for item in data
    )



@pytest.mark.shows
def test_get_shows_with_empty_db(client):

    response = client.get("/shows")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.shows
def test_get_show_by_id(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Avengers",
        "Endgame encore",
        "Telugu",
        "Sci-fi",
        180,
        "2026-09-25"
    )

    screen = create_screen("INOX_kothapet","Screen_1",2,3)

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2026-09-25T09:30:00",
                           "ticket_price":450
                       }
                    )

    show_id = show.json()["id"]

    response = client.get(f"/shows/{show_id}")

    assert response.status_code == 200
    assert response.json()["start_time"] == "2026-09-25T09:30:00"
    assert response.json()["end_time"] == "2026-09-25T12:30:00"



@pytest.mark.shows
def test_get_non_exist_show(client):

    response = client.get("/shows/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Show not found"



@pytest.mark.shows
def test_get_show_using_invalid_id_type(client):

    response = client.get("/shows/abcd")

    assert response.status_code == 422



@pytest.mark.shows
def test_get_seats_of_show(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Avengers",
        "Endgame encore",
        "Telugu",
        "Sci-fi",
        180,
        "2026-09-25"
    )

    screen = create_screen("INOX_kothapet","Screen_1",2,3)

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2026-09-25T09:30:00",
                           "ticket_price":450
                       }
                    )

    response = client.get("/shows")

    assert response.status_code == 200

    show_id = show.json()["id"]

    get_response = client.get(f"/shows/{show_id}/seats")

    assert get_response.status_code == 200

    data = get_response.json()

    seat_numbers = {item["Seat_number"] for item in data}

    assert seat_numbers == {
        "A1","A2","A3",
        "B1","B2","B3"
    }

    assert len(data) == 6

    assert all(item["available"] is True for item in data)   

@pytest.mark.shows
def test_get_seats_of_non_exists_show(client):

    get_response = client.get("/shows/99999/seats")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Show not found"

@pytest.mark.shows
def test_get_seats_of_show_by_invalid_id_type(client):

    get_response = client.get("/shows/abgc/seats")

    assert get_response.status_code == 422


@pytest.mark.shows
def test_update_show(client, create_screen, create_movie, admin_auth_headers):

    movie_1 = create_movie(
        "Spiderman",
        "Brand new_day",
        "telugu",
        "Adventure",
        180,
        "2027-02-03"
    )


    screen_1 = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie_1.json()["id"],
                           "screen_id":screen_1.json()["id"],
                           "start_time":"2027-02-03T09:30:00",
                           "ticket_price":300
                       }
                    )

    show_id = show.json()["id"]

    movie_2 = create_movie(
        "Captain_America",
        "Brand new_world",
        "telugu",
        "Adventure",
        135,
        "2027-02-03"
    )
    screen_2 = create_screen(
        "PCX_cinemas",
        "Screen_1",
        2,
        2
    )

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                              "movie_id":movie_2.json()["id"],
                              "screen_id":screen_2.json()["id"],
                              "start_time":"2027-02-03T09:45:00",
                              "ticket_price":450
                          }
                        )

    assert response.status_code == 200
    assert response.json()["movie_id"] == movie_2.json()["id"]
    assert response.json()["screen_id"] == screen_2.json()["id"]
    assert response.json()["start_time"] == "2027-02-03T09:45:00"
    assert response.json()["end_time"] == "2027-02-03T12:00:00"
    assert response.json()["ticket_price"] == "450.00"

@pytest.mark.shows
def test_update_show_with_normal_user(client, create_screen, create_movie, admin_auth_headers, normal_auth_headers):

    movie = create_movie(
        "Spiderman",
        "Brand new_day",
        "telugu",
        "Adventure",
        180,
        "2027-02-03"
    )

    screen = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2027-02-03T09:30:00",
                           "ticket_price":300
                       }
                    )

    show_id = show.json()["id"]

    response = client.put(f"/shows/{show_id}",
                          headers=normal_auth_headers,
                          json={
                              "start_time":"2027-02-03T09:45:00"
                          }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.shows
def test_update_show_without_login(client, create_screen, create_movie, admin_auth_headers):

    movie = create_movie(
        "Spiderman",
        "Brand new_day",
        "telugu",
        "Adventure",
        180,
        "2027-02-03"
    )

    screen = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2027-02-03T09:30:00",
                           "ticket_price":300
                       }
                    )

    show_id = show.json()["id"]

    response = client.put(f"/shows/{show_id}",
                          json={
                              "start_time":"2027-02-03T09:45:00"
                          }
                        )

    assert response.status_code == 401


@pytest.mark.shows
def test_update_show_using_invalid_show_id(client, admin_auth_headers):

    response = client.put(f"/shows/99999",
                          headers=admin_auth_headers,
                          json={
                              "start_time":"2027-02-03T09:45:00"
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Show not found"

@pytest.mark.shows
def test_update_show_using_invalid_id_type(client, admin_auth_headers):

    response = client.put(f"/shows/abd",
                          headers=admin_auth_headers,
                          json={
                              "start_time":"2027-02-03T09:45:00"
                          }
                        )

    assert response.status_code == 422


@pytest.mark.parametrize("field, value",[
    ("movie_id", "abcd"),
    ("screen_id", "acd"),
    ("start_time","22-02-2027"),
    ("ticket_price","efe"),
    ("ticket_price", 0),
    ("ticket_price", -100)
])

@pytest.mark.shows
def test_update_show_with_invalid_data(client, admin_auth_headers,create_movie, create_screen, field, value):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2027-08-15T09:45:00",
                           "ticket_price":350
                       }
                    )

    show_id = show.json()["id"]

    data={
        "movie_id":movie.json()["id"],
        "screen_id":screen.json()["id"],
        "start_time":"2027-08-15T09:45:00",
        "ticket_price":350
    }

    data[field] = value

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json=data)

    assert response.status_code == 422


@pytest.mark.shows
def test_update_show_with_non_exists_movie_id(client, create_screen, create_movie, admin_auth_headers):

    movie = create_movie(
        "Spiderman",
        "Brand new_day",
        "telugu",
        "Adventure",
        180,
        "2027-02-03"
    )

    screen = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2027-02-03T09:30:00",
                           "ticket_price":300
                       }
                    )

    show_id = show.json()["id"]

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                            "movie_id":99999
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


@pytest.mark.shows
def test_update_show_with_non_exists_screen_id(client, create_screen, create_movie, admin_auth_headers):

    movie = create_movie(
        "Spiderman",
        "Brand new_day",
        "telugu",
        "Adventure",
        180,
        "2027-02-03"
    )

    screen = create_screen(
        "PVR_cinemas",
        "Screen_1",
        2,
        2
    )

    show = client.post("/shows",
                       headers=admin_auth_headers,
                       json={
                           "movie_id":movie.json()["id"],
                           "screen_id":screen.json()["id"],
                           "start_time":"2027-02-03T09:30:00",
                           "ticket_price":300
                       }
                    )

    show_id = show.json()["id"]

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                            "screen_id":99999
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Screen not found"



@pytest.mark.shows
def test_update_show_to_overlap_another_show_timings_of_same_screen(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T12:30:00",
                             "ticket_price":300,
                         }
                        )

    show_id = show_2.json()["id"]

    assert show_2.status_code == 200

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                              "start_time":"2027-08-15T11:30:30"
                          }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "This show overlaps with an existing show on this screen"


@pytest.mark.shows
def test_update_show_with_overlap_another_show_timings_different_screen(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen_1 = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen_1.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"


    screen_2 = client.post("/screens",
                           headers=admin_auth_headers,
                           json={
                               "name":"Screen_2",
                               "theater_id":screen_1.json()["theater_id"],
                               "rows":2,
                               "seats_per_row":3
                           }
                        )

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen_2.json()["id"],
                             "start_time":"2027-08-15T12:30:00",
                             "ticket_price":300,
                         }
                        )

    show_id = show_2.json()["id"]

    assert show_2.status_code == 200

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                              "start_time":"2027-08-15T11:30:00"
                          }
                        )

    assert response.status_code == 200
    assert response.json()["start_time"] == "2027-08-15T11:30:00"



@pytest.mark.shows
def test_update_show_at_boundary_of_another_show(client, admin_auth_headers, create_movie, create_screen):

    movie = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashant neel",
        "Telugu",
        "Action_drama",
        180,
        "2027-08-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2, 2)

    show_1 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T09:30:00",
                             "ticket_price":300,
                         }
                        )

    assert show_1.status_code == 200
    assert show_1.json()["start_time"] == "2027-08-15T09:30:00"
    assert show_1.json()["end_time"] == "2027-08-15T12:30:00"

    show_2 = client.post("/shows",
                         headers=admin_auth_headers,
                         json={
                             "movie_id":movie.json()["id"],
                             "screen_id":screen.json()["id"],
                             "start_time":"2027-08-15T13:30:00",
                             "ticket_price":300,
                         }
                        )

    show_id = show_2.json()["id"]

    assert show_2.status_code == 200

    response = client.put(f"/shows/{show_id}",
                          headers=admin_auth_headers,
                          json={
                              "start_time":"2027-08-15T12:30:00"
                          }
                        )

    assert response.status_code == 200
    assert response.json()["start_time"] == "2027-08-15T12:30:00"
    assert response.json()["end_time"] == "2027-08-15T15:30:00"


@pytest.mark.shows
def test_delete_show(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    show = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    show_id = show.json()["id"]

    response = client.delete(f"/shows/{show_id}",
                             headers=admin_auth_headers
                            )

    assert response.status_code == 200
    assert response.json()["message"] == "Show deleted successfully"

    get_response = client.get(f"/shows/{show_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Show not found"



@pytest.mark.shows
def test_delete_show_with_normal_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    show = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    show_id = show.json()["id"]

    response = client.delete(f"/shows/{show_id}",
                             headers=normal_auth_headers
                            )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"



@pytest.mark.shows
def test_delete_show_without_login(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    screen = create_screen("PVR_cinemas","Screen_id", 2, 2)

    show = client.post("/shows",
                           headers=admin_auth_headers,
                           json={
                               "movie_id":movie.json()["id"],
                               "screen_id":screen.json()["id"],
                               "start_time":"2026-09-24T09:30:00",
                               "ticket_price":300
                           }
                        )

    show_id = show.json()["id"]

    response = client.delete(f"/shows/{show_id}")

    assert response.status_code == 401


@pytest.mark.shows
def test_delete_non_exists_show(client, admin_auth_headers):

    response = client.delete("/shows/99999",
                             headers=admin_auth_headers
                            )

    assert response.status_code == 404
    assert response.json()["detail"] == "Show not found"


@pytest.mark.shows
def test_delete_show_using_invalid_id_type(client, create_movie, create_screen, admin_auth_headers):

    response = client.delete("/shows/abdh",
                             headers=admin_auth_headers
                            )

    assert response.status_code == 422

@pytest.mark.shows
def test_delete_show_having_bookings(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-04-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2,2)

    show = client.post("/shows",
                headers=admin_auth_headers,
                json={
                    "movie_id":movie.json()["id"],
                    "screen_id":screen.json()["id"],
                    "start_time":"2027-04-15T09:30:00",
                    "ticket_price":300
                }
            )

    assert show.status_code == 200

    show_id = show.json()["id"]

    seats_response  = client.get(f"/shows/{show_id}/seats")

    assert seats_response.status_code == 200

    seats = seats_response.json()

    seat_ids = [seats[0]["seat_id"],seats[1]["seat_id"]]

    booking_seats = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200

    response = client.delete(f"/shows/{show_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Show has bookings"


@pytest.mark.shows
def test_get_show_seats_after_booking(client, create_movie, create_screen, admin_auth_headers):
    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-04-15"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2,2)

    show = client.post("/shows",
                headers=admin_auth_headers,
                json={
                    "movie_id":movie.json()["id"],
                    "screen_id":screen.json()["id"],
                    "start_time":"2027-04-15T09:30:00",
                    "ticket_price":300
                }
            )

    assert show.status_code == 200

    show_id = show.json()["id"]

    seats_response  = client.get(f"/shows/{show_id}/seats")

    assert seats_response.status_code == 200

    seats = seats_response.json()

    seat_ids = [seats[0]["seat_id"],seats[1]["seat_id"]]

    response = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 200

    booked_seat_numbers = [
        seats[0]["Seat_number"],
        seats[1]["Seat_number"]
    ]

    get_response = client.get(f"/shows/{show_id}/seats")

    assert get_response.status_code == 200

    data = get_response.json()

    for seat in data:
        if seat["Seat_number"] in booked_seat_numbers:
            assert seat["available"] == False
        else:
            assert seat["available"] == True
