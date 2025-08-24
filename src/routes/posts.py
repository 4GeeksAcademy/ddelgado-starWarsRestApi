from flask import request, jsonify
from models import db, Person, Planet

from flask import Flask, jsonify
from models import db, Person, Planet

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starwars.db"
db.init_app(app)

@app.route("/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    return jsonify([p.serialize() for p in people])

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])

