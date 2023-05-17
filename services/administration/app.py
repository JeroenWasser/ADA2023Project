import os

from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

from db import Base, engine
from resources.voting_session import VotingSession
from resources.party_admin import PartyAdmin
from resources.party import Party
import random
import requests
import time
import json 

VOTE_SERVICE_ENDPOINT = 'https://voting-lf6x6a722q-ue.a.run.app'
PARTY_MANAG_SERVICE_ENDPOINT = 'https://party-admin-service-lf6x6a722q-uc.a.run.app'
AUTH_SERVICE_ENDPOINT = 'https://authentication-service-lf6x6a722q-uc.a.run.app'

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
    voting_session, status = VotingSession.create(body)

    if status == 200:
        json_stored_update_session = json.loads(voting_session.get_data())
        request_body = {
            "id": json_stored_update_session['id'],
            "name": json_stored_update_session['name'],
            "start_time": json_stored_update_session['start_time'],
            "end_time": json_stored_update_session['start_time'],
            "uuid": json_stored_update_session['uuid'],
            "created_at": json_stored_update_session['created_at'],
            "edited_at": json_stored_update_session['edited_at']
        }
        url = f'{VOTE_SERVICE_ENDPOINT}/sessions'
        x = requests.post(url, json = request_body)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.post(url, json = request_body)       
        if x.status_code == 200:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path("votingadaproject", "voting_session")
            data = [
                {
                    "session_id": json_stored_update_session['id'],
                    "status": "created",
                }
            ]
            data = json.dumps(data).encode("utf-8")
            future = publisher.publish(topic_path, data)

            try:
                future.result()  # see https://docs.python.org/3/library/concurrent.futures.html
            except Exception as ex:
                return jsonify('topic message not send'), 500
            return jsonify({"message": f'Session created'}), 200
    else:
        return voting_session, status
    return voting_session, status

#Tested
@app.route('/sessions/<vs_id>', methods=['PUT'])
def update_voting_session(vs_id):
    try:
        vs_id = int(vs_id)
    except ValueError:
        return jsonify('id must be an integer'), 500
    body = request.json
    voting_session, status = VotingSession.update(vs_id, body)

    if status == 200:
        json_stored_update_session = json.loads(voting_session.get_data())
        request_body = {
            "id": json_stored_update_session['id'],
            "name": json_stored_update_session['name'],
            "start_time": json_stored_update_session['start_time'],
            "end_time": json_stored_update_session['start_time'],
        }
        url = f'{VOTE_SERVICE_ENDPOINT}'
        x = requests.put(url, json = request_body)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.put(url, json = request_body)       
        if x.status_code == 200:
            return jsonify({'message': 'succesfully created party'}), 200
    else:
        return voting_session, status
    return voting_session, status


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
    party, status = Party.create(body)

    if status == 200:
        json_stored_created_party = json.loads(party.get_data())
        request_body = {
            "id": json_stored_created_party['id'],
            "name": json_stored_created_party['name'],
            "uuid": json_stored_created_party['uuid'],
        }
        url = f'{PARTY_MANAG_SERVICE_ENDPOINT}/parties'
        x = requests.post(url, json = request_body)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.post(url, json = request_body)       
        if x.status_code == 200:
            return jsonify({'message': 'succesfully created party'}), 200
    else:
        return party, status
    return party, status

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
            "id": json_stored_created_party_admin['id'],
            "role": "admin",
            "party_name": json_stored_created_party['name']
        }
        url = f'{AUTH_SERVICE_ENDPOINT}/user/{json_stored_created_party_admin["uuid"]}/new_role'
        x = requests.post(url, json = request_body)
        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again')
            time.sleep(1)
            x = requests.post(url, json = request_body)

        
        request_body = {
            "id": json_stored_created_party_admin['id'],
            "first_name": json_stored_created_party_admin['first_name'],
            "last_name": json_stored_created_party_admin['last_name'],
            "party_id": json_stored_created_party_admin["party_id"]
        }
        url = f'{PARTY_MANAG_SERVICE_ENDPOINT}/party-members'
        x = requests.post(url, json = request_body)
        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again')
            time.sleep(1)
            x = requests.post(url, json = request_body)
        
        if x.status_code == 200:
            return jsonify({'message': 'Succesfully created admin'}), 200
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
        return jsonify('id must be an integer', 500)
    party, status = Party.delete(p_id)

    if status == 200:
        url = f'{PARTY_MANAG_SERVICE_ENDPOINT}/parties/{p_id}'
        x = requests.delete(url)
        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.delete(url)
        if x.status_code == 200:
            return jsonify({'message': 'succesfully removed party'}, 200)
    else:
        return party
    return jsonify({'message': 'Could not create party, try again'}, 500)
@app.route('/user/<uuid>/status', methods=['PUT'])
def update_role(uuid):
    body = request.json
    return PartyAdmin.update(uuid, body)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
