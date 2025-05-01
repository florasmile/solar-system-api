def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "The smallest planet in our solar system.",
        "diameter": 3.0,
    }


def test_get_one_planet_with_no_data(client):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet id 1 not found."}


def test_get_all_planets_with_two_saved_records(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 2,
            "name": "Venus",
            "description": "The hottest planet with a thick atmosphere.",
            "diameter": 7.5,
        },
        {
            "id": 1,
            "name": "Mercury",
            "description": "The smallest planet in our solar system.",
            "diameter": 3.0,
        },
    ]


def test_create_one_planet(client):
    # Act
    response = client.post(
        "/planets",
        json={"name": "New Planet", "description": "The Best!", "diameter": 4.0},
    )
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New Planet",
        "description": "The Best!",
        "diameter": 4.0,
    }
