from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    diameter: Mapped[float]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter,
        }

    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            name=planet_data["name"],
            description=planet_data["description"],
            diameter=planet_data["diameter"],
        )

    # def update_from_dict(self, planet_data):
    #     self.name=planet_data["name"],
    #     self.description=planet_data["description"],
    #     self.diameter=planet_data["diameter"]


# class Planet:
#   def __init__(self, id, name, description, diameter):
#     self.id = id
#     self.name = name
#     self.description = description
#     self.diameter = diameter
#     # assume diameter is in kilomiles
# planets = [
#     Planet(1, "Mercury", "The smallest planet in our solar system.", 3.0),
#     Planet(2, "Venus", "The hottest planet with a thick atmosphere.", 7.5),
#     Planet(3, "Earth", "Our home planet, the only one known to support life.", 7.9),
#     Planet(4, "Mars", "The red planet with the tallest volcano.", 4.2)
# ]
