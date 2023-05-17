import os

from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from google.cloud import pubsub_v1

from db import Base, engine
from resources.party_member import PartyMember
from resources.party_information import PartyInformation
from resources.party import Party
import json
import requests

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

auth = HTTPTokenAuth(scheme='Bearer')

ADMINISTRATION_SERVICE_ENDPOINT = 'https://administration-serv-lf6x6a722q-uc.a.run.app'

tokens = {
    "123": "admin",
    "456": "partymember",
    "789": "inhabitant"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    
@auth.login_required
@app.route('/parties', methods=['GET'])
def get_parties():
    return Party.get_all()

@auth.login_required
@app.route('/parties', methods=['POST'])
def add_party():
    req_data = request.get_json()
    return Party.add_party(req_data)

@auth.login_required
@app.route('/party/<p_id>', methods=['DELETE'])
def remove_party(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    removed_party, status = Party.delete_party(p_id)

    if status == 200:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("votingadaproject", "party_managment")
        data = [
            {
                "party_member": p_id,
                "status": "removed",
            }
        ]
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)

        try:
            future.result()  # see https://docs.python.org/3/library/concurrent.futures.html
        except Exception as ex:
            return jsonify('topic message not send'), 500
        return jsonify({"message": f'Party with ID {p_id} removed'}), 200

@auth.login_required
@app.route('/party-members/<p_id>/<m_id>', methods=['GET'])
def get_party_member(m_id):
    try:
        m_id = int(m_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    
    return PartyMember.get(m_id)

@auth.login_required
@app.route('/party-members/<m_id>', methods=['DELETE'])
def delete_party_member(m_id):
    try:
        m_id = int(m_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    
    return PartyMember.delete(m_id)

@auth.login_required
@app.route('/party-members/<p_id>', methods=['GET'])
def get_party_members(p_id):
    return PartyMember.get_party_members(p_id)

@auth.login_required
@app.route('/party-members', methods=['POST'])
def add_party_member():
    req_data = request.get_json()
    party_member, status = PartyMember.create(req_data)

    if status == 200:
        json_stored_created_party_member = json.loads(party_member.get_data())

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("votingadaproject", "party_managment")
        data = [
            {
                "party_member": json_stored_created_party_member['id'],
                "status": json_stored_created_party_member['status'],
            }
        ]
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)

        try:
            future.result()  # see https://docs.python.org/3/library/concurrent.futures.html
        except Exception as ex:
            return jsonify('topic message not send'), 500
        return jsonify({"message": f'Party member with ID {json_stored_created_party_member["id"]} created'}), 200
    else:
        return party_member

@auth.login_required
@app.route('/party-information/<p_id>', methods=['PUT'])
def get_party_information(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    
    return PartyInformation.get(p_id)

@auth.login_required
@app.route('/party-information/<p_id>', methods=['PUT'])
def update_party_information(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    
    req_data = request.get_json()
    party_info, status = PartyInformation.update(p_id, req_data)

    if status == 200:
        json_stored_update_party_info = json.loads(party_info.get_data())
        request_body = {
            "description": json_stored_update_party_info['name'],
        }
        url = f'{ADMINISTRATION_SERVICE_ENDPOINT}/parties/{json_stored_update_party_info["id"]}'
        x = requests.put(url, json = request_body)

        # Simulated retry policy of one retry
        if x.status_code != 200:
            print('failed once, trying again.')
            time.sleep(1)
            x = requests.put(url, json = request_body)       
        if x.status_code == 200:
            return jsonify({'message': 'succesfully created party'}), 200
    else:
        return party_info, status
    return party_info, status

@auth.login_required
@app.route('/party-information/<p_id>', methods=['POST'])
def create_party_information(p_id):
    try:
        p_id = int(p_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    
    req_data = request.get_json()
    return PartyInformation.create(p_id, req_data)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3051)), host='0.0.0.0', debug=True)
