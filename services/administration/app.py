import os

from flask import Flask, request, jsonify

from db import Base, engine
from resources.voting_session import VotingSession
from resources.party_admin import PartyAdmin
from resources.party import Party
import random
import requests
import time
<<<<<<< HEAD
import json 
=======
import json
>>>>>>> main

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
        return jsonify('id must be an integer'), 500
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
        return jsonify('id must be an integer'), 500
    body = request.json
    return VotingSession.update(vs_id, body)

#Tested
@app.route('/sessions/<vs_id>', methods=['DELETE'])
def delete_voting_session(vs_id):
    try:
        vs_id = int(vs_id)
    except ValueError:
        return jsonify('id must be an integer'), 500
    return VotingSession.delete(vs_id)


@app.route('/parties/placeholder', methods=['POST'])
def create_placeholder_party():
    body = request.json
    party = Party.create(body)

    if party[1] == 200:
        request_body = jsonify({
            "id": party.id,
            "name": party.name,
        })
        url = f'https://party-admin-service-lf6x6a722q-uc.a.run.app/parties'
        x = requests.post(url, json = request_body)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.post(url, json = request_body)
        if x.status_code == 200:
            return jsonify({'message': 'succesfully assigned admin role'}, 200)
    else:
        return jsonify({'message': 'Could not create party, try again'}, 500)

@app.route('/parties/<p_id>/admin', methods=['POST'])
def create_party_admin(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify({'message': 'id must be an integer'}), 500
    body = request.json
    created_party_admin, status = PartyAdmin.create(p_id, body)
    if status == 200:
        json_stored_created_party_admin = json.loads(created_party_admin.get_data())
        json_stored_created_party = json.loads(Party.get_one(int(json_stored_created_party_admin["party_id"])).get_data())

        request_body = {
            "id": random.randint(5,10000),
            "role": "admin",
            "party_name": json_stored_created_party['name']
        }
        url = f'https://authentication-service-lf6x6a722q-uc.a.run.app/user/{json_stored_created_party_admin["uuid"]}/new_role'
        x = requests.post(url, json = request_body)
        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again')
            time.sleep(1)
            x = requests.post(url, json = request_body)
        if x.status_code == 200:
            return jsonify({'message': 'succesfully assigned admin role'}), 200
    else:
        return jsonify({'message': 'Could not create party admin, try again'}), 500
    return jsonify({'message': 'Could not create party admin, try again'}), 500


@app.route('/parties/<p_id>', methods=['PUT'])
def update_party(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer'), 500
    body = request.json
    return Party.update(p_id, body)

@app.route('/parties/<p_id>', methods=['DELETE'])
def delete_party(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
<<<<<<< HEAD
        return jsonify('id must be an integer', 500)
    party = Party.delete(p_id)

    if party[1] == 200:
        request_body = jsonify({
            "id": party.id,
            "name": party.name,
        })
        url = f'https://party-admin-service-lf6x6a722q-uc.a.run.app/party/{party.id}'
        x = requests.delete(url)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.post(url, json = request_body)
        if x.status_code == 200:
            return jsonify({'message': 'succesfully removed party'}, 200)
    else:
        return jsonify({'message': 'Could not create party, try again'}, 500)
=======
        return jsonify('id must be an integer'), 500
    return Party.delete(p_id)
>>>>>>> main


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
