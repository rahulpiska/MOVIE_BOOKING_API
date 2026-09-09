import pytest

@pytest.mark.bookings
def test_create_booking_using_admin_user(client, create_movie, create_screen, admin_auth_headers):

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
    assert response.json()["total_amount"] == "600.00"
    assert response.json()["status"] == "Confirmed"


@pytest.mark.bookings
def test_create_booking_using_normal_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 200
    assert response.json()["total_amount"] == "600.00"
    assert response.json()["status"] == "Confirmed"


@pytest.mark.bookings
def test_create_booking_without_login(client, create_movie, create_screen, admin_auth_headers):

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
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 401


@pytest.mark.bookings
def test_create_booking_with_invalid_show_id(client, create_movie, create_screen, admin_auth_headers):

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
                               "show_id": 999999,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Show not available"


@pytest.mark.bookings
def test_create_booking_with_invalid_seat_ids(client, create_movie, create_screen, admin_auth_headers):

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
                               "show_id": show_id,
                               "seat_ids": [1,2,44]
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid seats"



@pytest.mark.bookings
def test_create_booking_using_unavailable_seats(client, create_movie, create_screen, admin_auth_headers):

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

    book_seats = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert book_seats.status_code == 200
    assert book_seats.json()["total_amount"] == "600.00"
    assert book_seats.json()["status"] == "Confirmed"

    response = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Seats unavailable"


@pytest.mark.parametrize("field, value",[
    ("show_id", 0),
    ("show_id", -10),
    ("show_id", "acd"),
    ("seat_ids","derf"),
    ("seat_ids",["1,2"])
]
)

@pytest.mark.bookings
def test_create_booking_with_invalid_data_values(client,
                                                create_movie,
                                                create_screen,
                                                admin_auth_headers,
                                                field,value):

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


    data={
        "show_id":show_id,
        "seat_ids":seat_ids
    }

    data[field] = value

    response = client.post("/bookings",
                           headers=admin_auth_headers,
                           json=data
                        )

    assert response.status_code == 422


@pytest.mark.bookings
def test_create_booking_with_empty_seat_ids(client, create_movie, create_screen, admin_auth_headers):

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

    seat_ids = []

    response = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 422


@pytest.mark.bookings
def test_create_booking_with_duplicate_seat_ids(client, create_movie, create_screen, admin_auth_headers):

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

    seat_ids = [seats[0]["seat_id"],seats[0]["seat_id"]]

    response = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid seats"


@pytest.mark.bookings
def test_get_bookings_using_admin_user(client, create_movie, create_screen, admin_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    response = client.get("/bookings",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert any(
        item["show_id"] == show_id
        and item["total_amount"] == "600.00"
        and item["status"] == "Confirmed"
        for item in data
    )


@pytest.mark.bookings
def test_get_bookings_using_normal_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    response = client.get("/bookings",
                          headers=normal_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert any(
        item["show_id"] == show_id
        and item["total_amount"] == "600.00"
        and item["status"] == "Confirmed"
        for item in data
    )



@pytest.mark.bookings
def test_get_bookings_of_another_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    response = client.get("/bookings",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json() == []



@pytest.mark.bookings
def test_get_bookings_without_login(client, create_movie, create_screen, admin_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    response = client.get("/bookings")

    assert response.status_code == 401


@pytest.mark.bookings
def test_get_bookings_with_empty_bookings(client, create_movie, create_screen, admin_auth_headers):

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


    response = client.get("/bookings",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json() == []



@pytest.mark.bookings
def test_get_booking_details_by_id_using_admin_user(client, create_movie, create_screen, admin_auth_headers):

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

    expected_seat_numbers = [
        seats[0]["Seat_number"],
        seats[1]["Seat_number"]
    ]

    booking_seats = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.get(f"/bookings/{booking_id}",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()


    assert data["movie"] == "Spirit"
    assert data["theater"] == "PVR_cinemas"
    assert data["screen"] == "Screen_1"
    assert data["start_time"] == "2027-04-15T09:30:00"
    assert data["status"] == "Confirmed"
    assert data["total_amount"] == "600.00"
    assert data["seats"] == expected_seat_numbers



@pytest.mark.bookings
def test_get_booking_details_by_id_using_normal_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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

    expected_seat_numbers = [
        seats[0]["Seat_number"],
        seats[1]["Seat_number"]
    ]

    booking_seats = client.post("/bookings",
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.get(f"/bookings/{booking_id}",
                          headers=normal_auth_headers)

    assert response.status_code == 200
    data = response.json()


    assert data["movie"] == "Spirit"
    assert data["theater"] == "PVR_cinemas"
    assert data["screen"] == "Screen_1"
    assert data["start_time"] == "2027-04-15T09:30:00"
    assert data["status"] == "Confirmed"
    assert data["total_amount"] == "600.00"
    assert data["seats"] == expected_seat_numbers


@pytest.mark.bookings
def test_get_booking_details_of_non_exists_booking_id(client, normal_auth_headers):
    response = client.get("/bookings/999999",
                          headers=normal_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking Details not found"


@pytest.mark.bookings
def test_get_booking_details_of_another_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.get(f"/bookings/{booking_id}",
                          headers=normal_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking Details not found" 


@pytest.mark.bookings
def test_get_booking_details_without_login(client,create_movie, create_screen, admin_auth_headers):

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

    expected_seat_numbers = [
        seats[0]["Seat_number"],
        seats[1]["Seat_number"]
    ]

    booking_seats = client.post("/bookings",
                           headers=admin_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.get(f"/bookings/{booking_id}")

    assert response.status_code == 401


@pytest.mark.bookings
def test_cancel_booking_using_admin_user(client, create_movie, create_screen, admin_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["show_id"] == show_id
    assert data["status"] == "Cancelled"


@pytest.mark.bookings
def test_cancel_booking_using_normal_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert booking_seats.status_code == 200
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=normal_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["show_id"] == show_id
    assert data["status"] == "Cancelled"


@pytest.mark.bookings
def test_cancel_booking_using_invalid_id(client, admin_auth_headers):

    response = client.patch("/bookings/999999/cancel",
                          headers=admin_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"

@pytest.mark.bookings
def test_cancel_booking_using_invalid_id_type(client, admin_auth_headers):

    response = client.patch("/bookings/acvs/cancel",
                          headers=admin_auth_headers)

    assert response.status_code == 422


@pytest.mark.bookings
def test_cancel_booking_without_login(client, create_movie, create_screen, admin_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel")

    assert response.status_code == 401


@pytest.mark.bookings
def test_cancel_the_already_cancelled_booking(client, create_movie, create_screen, admin_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["show_id"] == show_id
    assert data["status"] == "Cancelled"

    get_response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=admin_auth_headers)

    assert get_response.status_code == 400
    assert get_response.json()["detail"] == "Booking already Cancelled"


@pytest.mark.bookings
def test_cancel_booking_after_show_started(client, create_movie, create_screen, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-08"
    )

    screen = create_screen("PVR_cinemas","Screen_1",2,2)

    show = client.post("/shows",
                headers=admin_auth_headers,
                json={
                    "movie_id":movie.json()["id"],
                    "screen_id":screen.json()["id"],
                    "start_time":"2026-09-09T11:30:00",
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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=admin_auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot cancel after the show has started"


@pytest.mark.bookings
def test_cancel_booking_of_another_user(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    response = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=normal_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


@pytest.mark.bookings
def test_cancel_booking_to_check_seats_will_available(client, create_movie, create_screen, admin_auth_headers, normal_auth_headers):

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
    assert booking_seats.json()["total_amount"] == "600.00"
    assert booking_seats.json()["status"] == "Confirmed"

    booking_id = booking_seats.json()["id"]

    cancel_booking = client.patch(f"/bookings/{booking_id}/cancel",
                          headers=admin_auth_headers)

    assert cancel_booking.status_code == 200
    data = cancel_booking.json()

    assert data["show_id"] == show_id
    assert data["status"] == "Cancelled"

    another_booking = client.post("/bookings",
                           headers=normal_auth_headers,
                           json={
                               "show_id":show_id,
                               "seat_ids": seat_ids
                           }
                        )

    assert another_booking.status_code == 200
    assert another_booking.json()["total_amount"] == "600.00"
    assert another_booking.json()["status"] == "Confirmed"
