from flask import Blueprint
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