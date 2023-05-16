import os

from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth

from db import Base, engine
from resources.party_member import PartyMember
from resources.party_information import PartyInformation
from resources.party import Party

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

auth = HTTPTokenAuth(scheme='Bearer')

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
    
    return Party.delete_party(p_id)

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
    return PartyMember.create(req_data)

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
    return PartyInformation.update(p_id, req_data)

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
