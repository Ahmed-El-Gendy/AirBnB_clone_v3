#!/usr/bin/python3
"""import the modules"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from datetime import datetime
from models.state import State
import uuid
from models.city import City

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''get the city whith id = city_id'''
    cities = storage.all("City").values()
    city = [inst.to_dict() for inst in cities if inst.id == city_id]
    if city == []:
        abort(404)
    return jsonify(city[0])

@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Updates a City with id = city_id'''
    cities = storage.all("City").values()
    city = [inst.to_dict() for inst in cities if inst.id == city_id]
    if city == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city[0]['name'] = request.json['name']
    for inst in cities:
        if inst.id == city_id:
            inst.name = request.json['name']
    storage.save()
    return jsonify(city[0]), 200

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a City with id  = city_id'''
    cities = storage.all("City").values()
    city = [inst.to_dict() for inst in cities if inst.id == city_id]
    if city == []:
        abort(404)
    city.remove(city[0])
    for inst in cities:
        if inst.id == city_id:
            storage.delete(inst)
            storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''get all cities whit id'''
    states = storage.all("State").values()
    state = [inst.to_dict() for inst in states if inst.id == state_id]
    if state == []:
        abort(404)
    cities = storage.all("City").values()
    all_cities = [inst.to_dict() for inst in cities
                   if state_id == inst.state_id]
    return jsonify(all_cities)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a City with id'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = storage.all("State").values()
    state = [inst.to_dict() for inst in states if inst.id == state_id]
    if state == []:
        abort(404)
    cities = []
    new = City(name=request.json['name'], state_id=state_id)
    storage.new(new)
    storage.save()
    cities.append(new.to_dict())
    return jsonify(cities[0]), 201