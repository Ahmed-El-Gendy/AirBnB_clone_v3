#!/usr/bin/python3
"""new view for state"""
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import uuid
from datetime import datetime


@app_views.route('/states/', methods=['GET'])
def list_states():
    '''get all states'''
    states = [inst.to_dict() for inst in storage.all("State").values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''get one state'''
    all_states = storage.all("State").values()
    state = [int.to_dict() for inst in all_states if inst.id == state_id]
    if state == []:
        abort(404)
    return jsonify(state[0])

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a State with id'''
    states = storage.all("State").values()
    state = [inst.to_dict() for inst in states if inst.id == state_id]
    if state == []:
        abort(404)
    state.remove(state[0])
    for obj in states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = []
    new = State(name=request.json['name'])
    storage.new(new)
    storage.save()
    state.append(new.to_dict())
    return jsonify(state[0]), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Update'''
    states = storage.all("State").values()
    state = [inst.to_dict() for inst in states if inst.id == state_id]
    if state == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state[0]['name'] = request.json['name']
    for ustate in states:
        if ustate.id == state_id:
            ustate.id.name = request.json['name']
    storage.save()
    return jsonify(state[0]), 200
