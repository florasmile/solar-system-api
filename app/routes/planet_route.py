from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from ..db import db
from ..models.planet import Planet
from .route_utilities import validate_model, create_model
from ..models.moon import Moon

# create a blueprint
bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@bp.post("")
def create_a_planet():
    request_body = request.get_json()
    return create_model(Planet, request_body)


@bp.get("")
def get_all_planets():
    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    min_diameter_param = request.args.get("min_diameter")
    max_diameter_param = request.args.get("max_diameter")
    if min_diameter_param:
        query = query.where(Planet.diameter >= min_diameter_param)
    if max_diameter_param:
        query = query.where(Planet.diameter <= max_diameter_param)

    query = query.order_by(desc(Planet.name))
    planets = db.session.scalars(query)

    response = []

    for planet in planets:
        response.append(planet.to_dict())

    return response


@bp.get("/<planet_id>")
def get_a_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict()


@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    # validate_model_data(Planet, request_body)

    # planet.update_from_dict(request_body)
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.diameter = request_body["diameter"]
    planet.moons = []
    if request_body.get("moons"):
        for moon_data in request_body.get("moons"):
            new_moon = Moon.from_dict(moon_data)
            planet.moons.append(new_moon)

    print(planet.name, planet.diameter, planet.description, planet.moons)

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<planet_id>/moons")
def create_moon_with_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    request_body["planet_id"] = planet.id

    try:
        new_moon = Moon.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_moon)
    db.session.commit()
    return make_response(new_moon.to_dict(), 201)


@bp.get("/<planet_id>/moons")
def get_moons_by_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    response = []
    for moon in planet.moons:
        response.append(moon.to_dict())

    return response


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
