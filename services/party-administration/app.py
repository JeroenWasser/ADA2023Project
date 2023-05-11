import os

from flask import Flask, request

from db import Base, engine
from resources.party_member import PartyMember
from resources.party_information import PartyInformation

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)




@app.route('/party-members/<m_id>', methods=['GET'])
def get_party_member(m_id):
    return PartyMember.get(m_id)

@app.route('/party-members/<m_id>', methods=['DELETE'])
def delete_party_member(m_id):
    return PartyMember.delete(m_id)

@app.route('/party-members', methods=['GET'])
def get_party_members():
    return PartyMember.get_all()

@app.route('/party-members', methods=['POST'])
def add_party_member():
    req_data = request.get_json()
    return PartyMember.create(req_data)

@app.route('/party-information/<p_id>', methods=['PUT'])
def get_party_information(p_id):
    return PartyInformation.get(p_id)

@app.route('/party-information/<p_id>', methods=['PUT'])
def update_party_information(p_id):
    req_data = request.get_json()
    return PartyInformation.update(p_id, req_data)

@app.route('/party-information/<p_id>', methods=['POST'])
def create_party_information(p_id):
    req_data = request.get_json()
    return PartyInformation.create(p_id, req_data)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
