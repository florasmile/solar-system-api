from app.db import db
from app.models.planet import Planet


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
        "moons": [],
    }


def test_get_one_planet_with_no_data(client):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet id 1 not found."}


def test_get_one_planet_with_non_int_id_and_two_saved_records(
    client, two_saved_planets
):
    # Act
    response = client.get("/planets/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet id cat is invalid."}


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
            "moons": [],
        },
        {
            "id": 1,
            "name": "Mercury",
            "description": "The smallest planet in our solar system.",
            "diameter": 3.0,
            "moons": [],
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
        "moons": [],
    }


def test_create_one_planet_with_missing_field(client):
    # Act
    response = client.post(
        "/planets",
        json={"name": "New Planet", "description": "The Best!"},
    )
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "missing Planet information."}


def test_delete_planet_not_found(client):
    # Act
    response = client.delete("/planets/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet id 1 not found."}


def test_delete_planet(client, two_saved_planets):
    # Act
    response = client.delete("/planets/1")
    # Assert
    assert response.status_code == 204
    get_response = client.get("/planets/1")
    assert get_response.status_code == 404
    # query = db.select(Planet).where(Planet.id == 1)
    # assert db.session.scalar(query) == None


def test_update_planet(client, two_saved_planets):
    # Act
    response = client.put(
        "/planets/1",
        json={
            "name": "Updated Planet Name",
            "description": "Updated Planet Description",
            "diameter": 10.0,
        },
    )
    # Assert
    assert response.status_code == 204
    # query = db.select(Planet).where(Planet.id == 1)
    # planet = db.session.scalar(query)
    # assert planet.name == "Updated Planet Name"
    # assert planet.description == "Updated Planet Description"
    # assert planet.diameter == 10.0
    get_response = client.get("/planets/1")
    get_data = get_response.get_json()
    assert get_response.status_code == 200
    assert get_data["name"] == "Updated Planet Name"
    assert get_data["description"] == "Updated Planet Description"
    assert get_data["diameter"] == 10.0


def test_create_moon_with_valid_planet_id(client, two_saved_planets):
    response = client.post(
        "/planets/1/moons",
        json={
            "name": "A test moon for planet 1",
            "description": "A description for test moon",
            "size": 1.0,
        },
    )

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "A test moon for planet 1",
        "description": "A description for test moon",
        "size": 1.0,
        "planet_id": 1,
    }


def test_get_moons_by_planet_with_one_saved_planet(
    client, one_saved_planet_with_two_moons
):
    # Act
    response = client.get("/planets/1/moons")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Phobos",
            "description": "Surface is covered in deep grooves and impact craters.",
            "size": 22.4,
            "planet_id": 1,
        },
        {
            "id": 2,
            "name": "Deimos",
            "description": "Much smoother surface than Phobos — has thick regolith (dust blanket).",
            "size": 12.4,
            "planet_id": 1,
        },
    ]
