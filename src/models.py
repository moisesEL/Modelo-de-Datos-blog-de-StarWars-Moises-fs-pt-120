from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import List

db = SQLAlchemy()

## Usuario ##
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    suscription_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

   ## is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False) ##

    # relaciones
    favorites_characters: Mapped[List["favorites_characters"]] = relationship("favorites_characters",
                                                                              back_populates="user")
    favorites_planets: Mapped[List["favorites_planets"]
                              ] = relationship("favorites_planets", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "suscription_date": self.suscription_date,
            # do not serialize the password, its a security breach
        }


## Planeta ##
class planets(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(String(20))
    population: Mapped[str] = mapped_column(String(10))
    climate: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    ## relaciones ##
    favorites: Mapped[List["favorites_planets"]] = relationship(
        "favorites_planets", back_populates="planet")
    characters: Mapped[List["characters"]] = relationship(
        "characters", back_populates="planet")


## Personajes ##

class characters(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    mass: Mapped[int] = mapped_column(Integer)
    birth_year: Mapped[str] = mapped_column(String)
    home_world: Mapped[int] = mapped_column(ForeignKey(
        "planets.id"))  # Clave foranea id de tabla planets

# relaciones de personajes

    planet: Mapped["planets"] = relationship(
        "planets", back_populates="characters")
    favorites: Mapped[List["favorites_characters"]] = relationship(
        "favorites_characters", back_populates="character")


## tabla favorites_characters ##

class favorites_characters(db.Model):
    __tablename__ = "favorites_characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

# relaciones inversa
    user: Mapped["User"] = relationship(
        "users", back_populates="favorites_characters")
    character: Mapped["characters"] = relationship(
        "characters", back_populates="favorites")


## tabla favorites_planets ##

class favorites_planets(db.Model):
    __tablename__ = "favorites_planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

# relaciones inversa
    user: Mapped["User"] = relationship(
        "users", back_populates="favorites_planets")
    planet: Mapped["planets"] = relationship(
        "planets", back_populates="favorites")
