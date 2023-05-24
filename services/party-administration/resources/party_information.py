from datetime import datetime

from flask import jsonify

from daos.party_information_dao import PartyInformationDAO
from db import Session


class PartyInformation:
    @staticmethod
    def get(p_id):
        session = Session()

        try:
            p_id = int(p_id)
        except:
            return jsonify({'ID must be an integer'}, 500)

        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        party_information = session.query(PartyInformationDAO).filter(PartyInformationDAO.party_id == p_id).first()

        if party_information:
            text_out = {
                "description": party_information.description,
                "created_at": party_information.created_at,
                "edited_at": party_information.edited_at
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no Party Information for party with id {p_id}'}), 404
        
    @staticmethod
    def create(p_id, body):
        session = Session()

        try:
            id = int(body["id"])
            p_id = int(p_id)
        except:
            return jsonify({'ID must be an integer'}, 500)

        party_information = PartyInformationDAO(id, body['description'], p_id, datetime.now(), datetime.now())
        session.add(party_information)
        session.commit()
        session.refresh(party_information)
        session.close()
        return jsonify({'party_information_id': party_information.id}), 200

    @staticmethod
    def update(p_id, body):
        session = Session()

        try:
            p_id = int(p_id)
        except:
            return jsonify({'ID must be an integer'}, 500)

        party_information = session.query(PartyInformationDAO).filter(PartyInformationDAO.party_id == p_id).first()
        party_information.description = body['description']
        party_information.edited_at = datetime.now()

        try:
            session.commit()
            session.close()
            
            text_out = {
                "id": party_information.id,
                "description": party_information.description,
                "created_at": party_information.created_at,
                "edited_at": party_information.created_at
            }
            return jsonify(text_out), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500   
