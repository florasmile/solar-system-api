from flask import Blueprint, abort, make_response
from app.models.planet import planets

# create a blueprint
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.get("/")
def get_all_planets():
  result_list = []
  for planet in planets:
    result_list.append(dict(
      id = planet.id,
      name = planet.name,
      description = planet.description,
      diameter = planet.diameter
    ))
  return result_list

@planets_bp.get("/<planet_id>")
def get_a_planet(planet_id):
  planet = validate_planet(planet_id)
  planet_dic = dict(
          id = planet.id,
          name = planet.name,
          description = planet.description,
          diameter = planet.diameter
  )
  return planet_dic

#helper function to validate if the planet id can be converted to an int and exits in the planets
def validate_planet(planet_id):
  try:
    planet_id = int(planet_id)
  except:
    invalid = {"message": f"Planet id {planet_id} is invalid."}
    abort(make_response(invalid, 400))
  
  for planet in planets:
    if planet.id == planet_id:
      return planet
  
  not_found = {"message": f"Planet id {planet_id} not found."}
  abort(make_response(not_found, 404))