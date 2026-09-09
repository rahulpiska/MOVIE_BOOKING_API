import pytest


@pytest.mark.movies
def test_create_movie(client, admin_auth_headers):
    

    response = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"
                           }
                        )

    assert response.status_code == 200
    assert response.json()["title"] == "Paradise"
    assert response.json()["language"] == "Telugu"



@pytest.mark.movies
def test_create_duplicate_movies(client, admin_auth_headers):

    
    create_movie = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"
                           }
                        )

    assert create_movie.status_code == 200
    assert create_movie.json()["title"] == "Paradise"
    assert create_movie.json()["language"] == "Telugu"


    response = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Movie with this title already exists"


@pytest.mark.movies
def test_create_movie_without_login(client):

    response = client.post("/movies",
                            json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"
                           }                           
                        )

    assert response.status_code == 401


@pytest.mark.movies
def test_create_movie_with_normal_user(client, normal_auth_headers):

    response = client.post("/movies",
                           headers=normal_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"
                               }
                            )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"
    


@pytest.mark.movies
def test_create_movie_with_missing_data(client, admin_auth_headers):

    response = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "release_date": "2026-09-24"                               
                           }
                        )

    assert response.status_code == 422


@pytest.mark.movies
def test_create_case_insensitive_duplicate_title(client, admin_auth_headers):


    create_movie = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"Paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"                               
                           }
                        )

    assert create_movie.status_code == 200
    assert create_movie.json()["title"] == "Paradise"
    assert create_movie.json()["genre"] == "Drama"


    response = client.post("/movies",
                           headers=admin_auth_headers,
                           json={
                               "title":"paradise",
                               "description":"Staring Nani, directed by Srikanth odela",
                               "language":"Telugu",
                               "genre":"Drama",
                               "duration_minutes":165,
                               "release_date": "2026-09-24"                               
                           }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Movie with this title already exists"



@pytest.mark.movies
def test_get_movies(client,create_movie):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    response = client.get("/movies")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["title"] == "Spirit"
    assert data[0]["description"] == "Staring Prabhas, Directed by SRV"



@pytest.mark.movies
def test_get_movies_with_empty_db(client):

    response = client.get("/movies")

    assert response.status_code == 200
    assert response.json() == []



@pytest.mark.movies
def test_get_movie_by_id(client, create_movie):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    movie_id = movie.json()["id"]


    response = client.get(f"/movies/{movie_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Spirit"
    assert response.json()["genre"] == "Action_drama"



@pytest.mark.movies
def test_get_non_exist_movie_by_id(client):

    response = client.get("/movies/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


@pytest.mark.movies
def test_get_movie_using_invalid_id(client):

    response = client.get("/movies/abc")

    assert response.status_code == 422

@pytest.mark.movies
def test_get_shows_of_movie(client, create_movie, create_screen, admin_auth_headers):

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

    movie_id = movie.json()["id"]

    response = client.get(f"/movies/{movie_id}/shows")

    assert response.status_code == 200
    data = response.json()

    assert any(
        item["ticket_price"] == "300.00"
        and item["start_time"] == "2026-09-24T09:30:00"
        and item["end_time"] == "2026-09-24T12:30:00"
        for item in data
    )


@pytest.mark.movies
def test_get_shows_of_non_exists_movie(client):

    response = client.get("/movies/999999/shows")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


@pytest.mark.movies
def test_get_shows_of_movie_with_no_shows(client, create_movie):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2026-09-24"
    )

    movie_id = movie.json()["id"]

    response = client.get(f"/movies/{movie_id}/shows")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie has no shows"


@pytest.mark.movies
def test_get_shows_of_movie_invalid_id(client, create_movie, create_screen, admin_auth_headers):

    response = client.get("/movies/acdv/shows")

    assert response.status_code == 422


@pytest.mark.movies
def test_update_movie(client, create_movie, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    movie_id = movie.json()["id"]


    response = client.put(f"/movies/{movie_id}",
                          headers=admin_auth_headers,
                          json={
                              "title":"Raaka",
                              "description":"Staring Allu Arjun",
                              "language":"Telug",
                              "genre":"Sci-fi",
                              "duration_minutes":185,
                              "release_data":"2027-11-18"
                          }
                        )

    assert response.status_code == 200
    assert response.json()["title"] == "Raaka"
    assert response.json()["duration_minutes"] == 185



@pytest.mark.movies
def test_update_non_exist_movie(client,admin_auth_headers):

    response = client.put("/movies/99999",
                          headers=admin_auth_headers,
                          json={
                              "title":"Animal_Park"
                          }
                        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


@pytest.mark.movies
def test_update_movie_to_duplicate(client, create_movie, admin_auth_headers):

    movie_1 = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    
    assert movie_1.status_code == 200
    assert movie_1.json()["title"] == "Spirit"
    assert movie_1.json()["genre"] == "Action_drama"


    movie_2 = create_movie(
        "Salaar",
        "Staring Prabhas, Directed by Prashanth neel",
        "Telugu",
        "Action_drama",
        170,
        "2027-08-14"
    )

    
    assert movie_2.status_code == 200
    assert movie_2.json()["title"] == "Salaar"
    assert movie_2.json()["genre"] == "Action_drama"

    movie_id = movie_2.json()["id"]


    response = client.put(f"/movies/{movie_id}",
                          headers=admin_auth_headers,
                          json={
                              "title":"spirit"
                          }
                        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Movie title already exists"



@pytest.mark.movies
def test_update_movie_using_normal_user(client, create_movie, normal_auth_headers):


    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    movie_id = movie.json()["id"]

    response = client.put(f"/movies/{movie_id}",
                          headers=normal_auth_headers,
                          json={
                              "title":"Leo"
                          }
                        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.movies
def test_update_movie_without_login(client, create_movie, admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    movie_id = movie.json()["id"]


    response = client.put(f"/movies/{movie_id}",
                          json={
                              "duration_minutes":185
                          }
                        )

    assert response.status_code == 401


@pytest.mark.movies
def test_update_movie_with_invalid_data(client,create_movie,admin_auth_headers):

    movie = create_movie(
        "Spirit",
        "Staring Prabhas, Directed by SRV",
        "Telugu",
        "Action_drama",
        180,
        "2027-03-15"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Spirit"
    assert movie.json()["genre"] == "Action_drama"

    movie_id = movie.json()["id"]

    response = client.put(f"/movies/{movie_id}",
                          headers=admin_auth_headers,
                          json={
                              "duration_minutes": "170_minutes"
                          }
                        )

    assert response.status_code == 422


@pytest.mark.movies
def test_update_movie_using_invalid_movie_id(client, admin_auth_headers):


    response = client.put(f"/movies/abc",
                          headers=admin_auth_headers,
                          json={
                              "duration_minutes":185
                          }
                        )

    assert response.status_code == 422

#------------------------------------------

@pytest.mark.movies
def test_delete_movie(client, create_movie, admin_auth_headers):

    movie = create_movie(
        "Raaka",
        "Staring Allu Arjun, Directed by Atlee",
        "Telugu",
        "Sci-fi",
        170,
        "2027-12-19"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Raaka"
    assert movie.json()["genre"] == "Sci-fi"

    movie_id = movie.json()["id"]


    response = client.delete(f"/movies/{movie_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Movie deleted successfully"

    get_movie = client.get(f"/movies/{movie_id}")

    assert get_movie.status_code == 404
    assert get_movie.json()["detail"] == "Movie not found"


@pytest.mark.movies
def test_delete_non_exist_movie(client, admin_auth_headers):

    response = client.delete("/movies/99999",
                             headers=admin_auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


@pytest.mark.movies
def test_delete_movie_without_login(client, create_movie):


    movie = create_movie(
        "Raaka",
        "Staring Allu Arjun, Directed by Atlee",
        "Telugu",
        "Sci-fi",
        170,
        "2027-12-19"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Raaka"
    assert movie.json()["genre"] == "Sci-fi"

    movie_id = movie.json()["id"]


    response = client.delete(f"/movies/{movie_id}")

    assert response.status_code == 401


@pytest.mark.movies
def test_delete_movie_using_normal_user(client, create_movie, normal_auth_headers):

    movie = create_movie(
        "Raaka",
        "Staring Allu Arjun, Directed by Atlee",
        "Telugu",
        "Sci-fi",
        170,
        "2027-12-19"
    )

    assert movie.status_code == 200
    assert movie.json()["title"] == "Raaka"
    assert movie.json()["genre"] == "Sci-fi"

    movie_id = movie.json()["id"]


    response = client.delete(f"/movies/{movie_id}",
                             headers=normal_auth_headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@pytest.mark.movies
def test_delete_movie_using_invalid_movie_id(client,admin_auth_headers):

    response = client.delete("/movies/abc",
                             headers=admin_auth_headers)

    assert response.status_code == 422


@pytest.mark.movies
def test_delete_movie_having_shows(client, create_movie, create_screen, admin_auth_headers):

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

    assert show.status_code == 200

    movie_id = movie.json()["id"]

    response = client.delete(f"/movies/{movie_id}",
                             headers=admin_auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Movie has shows"