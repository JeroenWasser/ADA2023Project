from flask import jsonify, redirect, url_for
from datetime import datetime, timedelta
from daos.roles_dao import RolesDAO
from db import Session

class Login:
    @staticmethod
    def digid_check(uuid, digid_message):
        session = Session()
        user = session.query(RolesDAO).filter(RolesDAO.uuid == int(uuid)).first()
        if user:
            session.close()
            if digid_message == 'rejected':
                return jsonify({'message': 'Your login with DigID was unsuccessful, please try again'}), 404
            elif digid_message == 'accepted':
                return redirect(f'/login/{uuid}/service_choice'), 200
            else:
                return jsonify({'message': 'An unknown error has occured, please try logging in with DigID again'}), 404
        else:
            return jsonify({'message': 'Sorry, you are not included in the voting system yet.'}), 404

    def create_cookie(uuid, body):
        if body['service'] == 'administration':
            token = '123'
        elif body['service'] == 'party':
            token = '456'
        elif body['service'] == 'voting':
            token = '789'
        else:
            return jsonify({'message': 'This service does not exist, please try again'}), 404
        valid_to = datetime.now() + timedelta(hours=1)

        return f'token={token}; uuid={uuid}; valid_to={valid_to}'

