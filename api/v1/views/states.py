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