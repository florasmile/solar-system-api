from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from ..db import db
from ..models.planet import Planet
from .route_utilities import validate_model

# create a blueprint
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.post("")
def create_a_planet():
    request_body = request.get_json()

    new_planet = validate_planet_data(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201


@planets_bp.get("")
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
        response.append(
            planet.to_dict()
        )

    return response


@planets_bp.get("/<planet_id>")
def get_a_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict()





@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    planet.update_from_dict(request_body)
    # planet.name = request_body["name"]
    # planet.description = request_body["description"]
    # planet.diameter = request_body["diameter"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="applcation/json")

def validate_planet_data(planet_data):
    try:
        new_planet = Planet.from_dict(planet_data)
    except KeyError:
        response = {"message": "missing planet information."}
        abort(make_response(response, 400))
    return new_planet
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
