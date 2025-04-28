from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.planet import Planet
# from app.models.planet import planets

# create a blueprint
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.post("")
def create_a_planet():
    request_body = request.get_json()

    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"],
        diameter=request_body["diameter"],
    )

    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "diameter": new_planet.diameter,
    }
    return response, 201


@planets_bp.get("/")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    response = []

    for planet in planets:
        response.append(
            dict(
                id=planet.id,
                name=planet.name,
                description=planet.description,
                diameter=planet.diameter,
            )
        )

    return response


@planets_bp.get("/<planet_id>")
def get_a_planet(planet_id):
    planet = validate_planet(planet_id)
    planet_dic = dict(
        id=planet.id,
        name=planet.name,
        description=planet.description,
        diameter=planet.diameter,
    )
    return planet_dic


# helper function to validate if the planet id can be converted to an int and exits in the planets
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        invalid = {"message": f"Planet id {planet_id} is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        not_found = {"message": f"Planet id {planet_id} not found."}
        abort(make_response(not_found, 404))
    return planet


@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.diameter = request_body["diameter"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="applcation/json")


# @planets_bp.get("/")
# def get_all_planets():
#   result_list = []
#   for planet in planets:
#     result_list.append(dict(
#       id = planet.id,
#       name = planet.name,
#       description = planet.description,
#       diameter = planet.diameter
#     ))
#   return result_list
