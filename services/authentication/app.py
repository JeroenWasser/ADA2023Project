import os

from flask import Flask, request, jsonify, redirect

from db import Base, engine
from resources.login import Login
from resources.roles_updates import RolesUpdates
from resources.roles import Roles

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/login/<uuid>/<digid_message>', methods=['GET'])
def verify_login(uuid, digid_message):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    return Login.digid_check(uuid, digid_message)

@app.route('/login/<uuid>/service_choice', methods=['GET'])
def provide_service_choices(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    return Roles.get(uuid)

@app.route('/login/<uuid>/service_choice', methods=['POST'])
def give_service_choice(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'The id must be an integer'}), 500
    choice = request.get_json()
    cookie = Login.create_cookie(uuid, choice)

    if choice['service'] == 'administration':
        return jsonify({'service': choice['service'], 'cookie': cookie})
        #return redirect()
    if choice['service'] == 'party':
        return jsonify({'service': choice['service'], 'cookie': cookie})
        #return redirect()
    if choice['service'] == 'voting':
        return jsonify({'service': choice['service'], 'cookie': cookie})
        #return redirect()

@app.route('/user/<uuid>/new_admin_role', methods=['POST'])
def new_admin_role(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    return RolesUpdates.add_admin_role(uuid)

@app.route('/user/<uuid>/new_partymember_role', methods=['POST'])
def new_partymember_role(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    body = request.get_json()
    return RolesUpdates.add_partymember_role(uuid, body)

@app.route('/user/<uuid>/verification', methods=['GET'])
def verify_role_user(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    return RolesUpdates.verify_role(uuid)

@app.route('/user/<uuid>/verification/admin', methods=['POST'])
def user_admin_role_verified(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    req_data = request.get_json()
    return RolesUpdates.admin_role_verified(uuid, req_data)

@app.route('/user/<uuid>/verification/member', methods=['POST'])
def user_member_role_verified(uuid):
    try:
        uuid = int(uuid)
    except ValueError:
        return jsonify({'message': 'The id must be an integer'}), 500
    req_data = request.get_json()
    return RolesUpdates.member_role_verified(uuid, req_data)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
