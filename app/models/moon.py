from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING

# if TYPE_CHECKING:
#   from .planet import Planet


class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size: Mapped[float]
    description: Mapped[str]
    # update
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "description": self.description,
            "planet_id": self.planet_id,
        }

    @classmethod
    def from_dict(cls, moon_data):
        return cls(
            name=moon_data["name"],
            size=moon_data["size"],
            description=moon_data["description"],
            planet_id=moon_data["planet_id"],
        )
