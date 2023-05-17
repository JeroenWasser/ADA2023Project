import os

from flask import Flask, request, jsonify, redirect

from db import Base, engine
from resources.login import Login
from resources.roles_history import RolesHistory
from resources.roles import Roles

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/login/<uuid>/<digid_message>', methods=['GET'])
def verify_login(uuid, digid_message):
    return Login.digid_check(uuid, digid_message)

@app.route('/login/<uuid>/service_choice', methods=['GET'])
def provide_service_choices(uuid):
    return Roles.get(uuid)

@app.route('/login/<uuid>/service_choice', methods=['POST'])
def give_service_choice(uuid):
    choice = request.get_json()
    cookie = Login.create_cookie(uuid, choice)

    if choice['service'] == 'administration':
        return jsonify({'message': 'redirecting to administration service', 'cookie': cookie})
    if choice['service'] == 'party':
        return jsonify({'message': 'redirecting to party service', 'cookie': cookie})
    if choice['service'] == 'voting':
        return jsonify({'message': 'redirecting to voting service', 'cookie': cookie})

@app.route('/user/<uuid>/new_role', methods=['POST'])
def new_role(uuid):
    body = request.get_json()
    try:
        body['role']
    except KeyError:
        return jsonify({'Message': 'Please provide a role to request'})
    return RolesHistory.add_role(uuid, body)

# @app.route('/user/<uuid>/new_partymember_role', methods=['POST'])
# def new_partymember_role(uuid):
#     body = request.get_json()
#     return RolesHistory.add_partymember_role(uuid, body)

@app.route('/user/verification/<uuid>', methods=['GET'])
def verify_role_user(uuid):
    return RolesHistory.verify_role(uuid)

# @app.route('/user/<uuid>/verification/admin', methods=['POST'])
# def user_admin_role_verified(uuid):
#     req_data = request.get_json()
#     return RolesHistory.admin_role_verified(uuid, req_data)

# @app.route('/user/<uuid>/verification/member', methods=['POST'])
# def user_member_role_verified(uuid):
#     req_data = request.get_json()
#     return RolesHistory.member_role_verified(uuid, req_data)

@app.route('/user/verification/<uuid>', methods=['POST'])
def user_role_verified(uuid):
    req_data = request.get_json()
    return RolesHistory.role_verified(uuid, req_data)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
