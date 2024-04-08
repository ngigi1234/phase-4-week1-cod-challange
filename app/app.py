#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''
@app.route('/heroes')
def all_heroes():
    all_heroes = []
    heroes = Hero.query.all()
    for hero in heroes:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        all_heroes.append(hero_dict)
    response = make_response(all_heroes, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if not hero:
        response_body = {
            "error": "Hero not found"
            }
        response = make_response(jsonify(response_body), 404)
    else:
        hero_powers = HeroPower.query.filter_by(hero_id=id).all()
        power_ids = []
        powers = []
        for hero_power in hero_powers:
            '''power = {
                "id": hero_power.id,
                "name": hero_power.name,
                "description": hero_power.description
            }
            powers.append(power)'''
            power_id = hero_power.power_id
            power_ids.append(power_id)

        for i in power_ids:
            power = Power.query.filter_by(id=i).first()
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers.append(power_dict)
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": powers
        }
        response = make_response(jsonify(hero_dict), 200)
        #response = make_response(hero_dict, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/powers')
def powers():
    power_list = []
    powers = Power.query.all()
    for power in powers:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        power_list.append(power_dict)
    response = make_response(jsonify(power_list), 200)
    return response

@app.route('/powers/<int:id>', methods=["GET", "PATCH"])
def power(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        response_body = {
            "error": "Power not found"
            }
        response = make_response(jsonify(response_body), 404)
    elif request.method == "GET":
        response_body = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        response = make_response(jsonify(response_body), 200)
    elif request.method == "PATCH":
        json_data = request.get_json()
        new_description = json_data.get("description")
        power.description = new_description
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = {
                "errors": ["validation errors"]
                }
            response = make_response(jsonify(error), 400)
        response_body = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        response = make_response(jsonify(response_body), 200)
    response.headers["Content-Type"] = 'application/json'
    return response

@app.route('/hero_powers', methods=["POST"])
def hero_power():
    json_data = request.get_json()
    new_hero_power = HeroPower (
        strength=json_data.get("strength"),
        power_id=json_data.get("power_id"),
        hero_id=json_data.get("hero_id")
    )
    db.session.add(new_hero_power)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = {
            "errors": ["validation errors"]
            }
        response = make_response(jsonify(error), 400)
    hero_id = new_hero_power.hero_id
    return redirect(url_for('hero_by_id', id=hero_id))

if __name__ == '__main__':
    app.run(port=5555)
