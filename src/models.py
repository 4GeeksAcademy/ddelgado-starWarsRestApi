from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#Planets
class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))

    # Relaciones
    people: Mapped[list["Person"]] = relationship("Person", back_populates="planet")
    species: Mapped[list["Species"]] = relationship("Species", back_populates="planet")

    def __repr__(self):
        return f"<Planet {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "people": [p.id for p in self.people],    
            "species": [s.id for s in self.species],
        }

#Species
class Species(db.Model):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)

    # Relaciones
    planet: Mapped["Planet"] = relationship("Planet", back_populates="species")
    people: Mapped[list["Person"]] = relationship("Person", back_populates="species")

    def __repr__(self):
        return f"<Species {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id,
            "people": [p.id for p in self.people],
        }

# People
class Person(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=False)

    # Relaciones
    planet: Mapped["Planet"] = relationship("Planet", back_populates="people")
    species: Mapped["Species"] = relationship("Species", back_populates="people")

    def __repr__(self):
        return f"<Person {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id,
            "species_id": self.species_id,
        }
