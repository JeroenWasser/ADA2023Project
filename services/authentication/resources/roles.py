from daos.roles_dao import RolesDAO
from db import Session
from flask import jsonify

class Roles:
    @staticmethod
    def get(uuid):
        session = Session()
        person_roles = session.query(RolesDAO).filter(RolesDAO.uuid == int(uuid)).first()
        
        if person_roles: # Check if person exists
            text_out = []
            if person_roles.admin:
                text_out.append('administration')
            if person_roles.partymember:
                text_out.append('party')
            if person_roles.inhabitant:
                text_out.append('voting')
            session.close()
            return jsonify({'message': 'Your login was successful! Which service do you want to use?', 'options': text_out}), 200
        else:
            session.close()
            return jsonify({'message': 'You do not appear in the voting system yet.'}), 404



