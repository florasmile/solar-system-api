import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.planet import Planet
from app.models.moon import Moon

load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_TEST_DATABASE_URI"),
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_saved_planets(app):
    # Arrange
    mercury = Planet(
        name="Mercury",
        description="The smallest planet in our solar system.",
        diameter=3.0,
    )
    venus = Planet(
        name="Venus",
        description="The hottest planet with a thick atmosphere.",
        diameter=7.5,
    )

    db.session.add_all([mercury, venus])
    db.session.commit()

@pytest.fixture
def one_saved_planet_with_two_moons(app):
    # Arrange
    mars = Planet(
        name="Mars", 
        description="The red planet with the tallest volcano.", 
        diameter=4.2
    )

    phobos = Moon(
        name="Phobos",
        description="Surface is covered in deep grooves and impact craters.",
        size=22.4,
        planet_id=1
    )

    deimos = Moon(
        name="Deimos",
        description="Much smoother surface than Phobos — has thick regolith (dust blanket).",
        size=12.4,
        planet_id=1
    )

    db.session.add_all([mars, phobos, deimos])
    db.session.commit()
    
