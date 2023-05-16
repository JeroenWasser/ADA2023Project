import os

from flask import Flask, request, jsonify

from db import Base, engine
from resources.voting_session import VotingSession
from resources.party_admin import PartyAdmin
from resources.party import Party
import random
import requests

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/', methods=['GET'])
def get_test():
    return jsonify({'message': f'The standard endpoint works'}), 200

# @app.route('/parties/<p_id>/admin', methods=['POST'])
# def create_party_admin(p_id):
#     return Delivery.get(d_id)

#Tested
@app.route('/sessions/<vs_id>', methods=['GET'])
def get_voting_session(vs_id):
    try:
        vs_id = int(vs_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    return VotingSession.get(vs_id)

#Tested
@app.route('/sessions/', methods=['GET'])
def get_voting_sessions():
    return VotingSession.get_all()

#Tested
@app.route('/sessions/create', methods=['POST'])
def create_voting_session():
    body = request.json
    return VotingSession.create(body)

#Tested
@app.route('/sessions/<vs_id>', methods=['PUT'])
def update_voting_session(vs_id):
    try:
        vs_id = int(vs_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    body = request.json
    return VotingSession.update(vs_id, body)

#Tested
@app.route('/sessions/<vs_id>', methods=['DELETE'])
def delete_voting_session(vs_id):
    try:
        vs_id = int(vs_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    return VotingSession.delete(vs_id)


@app.route('/parties/placeholder', methods=['POST'])
def create_placeholder_party():
    body = request.json
    return Party.create(body)

@app.route('/parties/<p_id>/admin', methods=['POST'])
def create_party_admin(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    body = request.json
    created_party_admin = PartyAdmin.create(p_id, body)
    if create_party_admin[1] == 200:
        request_body = jsonify({
            "id": random.randint(5,10000),
            "role": "admin",
            "party_name": Party.get_one(int(created_party_admin[0]["party_id"]))[0]['name']
        })
        url = f'https://authentication-service-lf6x6a722q-uc.a.run.app/user/{created_party_admin[0]["uuid"]}/new_role'
        x = requests.post(url, json = request_body)
        return jsonify({'succesfully assigned user'}, 200)
    else:
        return jsonify({'Could not create party admin, try again'}, 500)


@app.route('/parties/<p_id>', methods=['PUT'])
def update_party(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    body = request.json
    return Party.update(p_id, body)

@app.route('/parties/<p_id>', methods=['DELETE'])
def delete_party(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    return Party.delete(p_id)

@app.route('/user/<uuid>/status', methods=['PUT'])
def update_role(uuid):
    body = request.get_json()
    return PartyAdmin.update(uuid, body)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
