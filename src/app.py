"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException
from admin.setup_admin import setup_admin
from models import db, Person, Planet, Species

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()
    setup_admin(app)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenido a la mini SWAPI 🚀"}), 200


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# People
@app.route('/people', methods=["GET"])
def get_people():
    people = Person.query.all()
    return jsonify([p.serialize() for p in people]), 200


@app.route('/people/<int:person_id>', methods=["GET"])
def get_person(person_id):
    person = Person.query.get_or_404(person_id)
    return jsonify({
        "id": person.id,
        "name": person.name,
        "planet": person.planet.name if person.planet else None,
        "species": person.species.name if person.species else None
    }), 200


@app.route('/people', methods=["POST"])
def create_person():
    data = request.get_json()
    name = data.get("name")
    planet_id = data.get("planet_id")
    species_id = data.get("species_id")

    if not name or not planet_id or not species_id:
        return jsonify({"error": "Falta name, planet_id o species_id"}), 400

    
    planet = Planet.query.get(planet_id)
    species = Species.query.get(species_id)
    if not planet or not species:
        return jsonify({"error": "planet_id o species_id inválido"}), 400

    person = Person(name=name, planet_id=planet_id, species_id=species_id)
    db.session.add(person)
    db.session.commit()
    return jsonify(person.serialize()), 201


@app.route('/people/<int:person_id>', methods=["DELETE"])
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": f"Person {person_id} deleted"}), 200


# Pllanets
@app.route('/planets', methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({
        "id": planet.id,
        "name": planet.name,
        "climate": planet.climate,
        "people": [p.name for p in planet.people],
        "species": [s.name for s in planet.species]
    }), 200


@app.route('/planets', methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Falta el nombre"}), 400
    planet = Planet(name=data["name"], climate=data.get("climate"))
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} deleted"}), 200


# Species
@app.route("/species", methods=["GET"])
def get_species():
    species = Species.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "planet": s.planet.name if s.planet else None,
        "people": [p.name for p in s.people]
    } for s in species]), 200


@app.route("/species/<int:species_id>", methods=["GET"])
def get_species_detail(species_id):
    s = Species.query.get_or_404(species_id)
    return jsonify({
        "id": s.id,
        "name": s.name,
        "planet": s.planet.name if s.planet else None,
        "people": [p.name for p in s.people]
    }), 200


@app.route("/species", methods=["POST"])
def create_species():
    data = request.get_json()
    name = data.get("name")
    planet_id = data.get("planet_id")

    if not name or not planet_id:
        return jsonify({"error": "Falta name o planet_id"}), 400

    # Validar existencia del planeta
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "planet_id inválido"}), 400

    species = Species(name=name, planet_id=planet_id)
    db.session.add(species)
    db.session.commit()
    return jsonify(species.serialize()), 201


@app.route("/species/<int:species_id>", methods=["DELETE"])
def delete_species(species_id):
    s = Species.query.get_or_404(species_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": f"Species {species_id} deleted"}), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
