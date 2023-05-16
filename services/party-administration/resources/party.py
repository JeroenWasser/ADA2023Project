from datetime import datetime

from flask import jsonify

from daos.party_dao import PartyDAO
from db import Session


class Party:
    @staticmethod
    def get_all():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        parties = session.query(PartyDAO).all()

        if len(parties) > 0:
            text_out = [{
                 "id": party.id,
                 "name": party.name,
                 "uuid": party.uuid,
                 "created_at": party.created_at,
                 "edited_at": party.edited_at
            } for party in parties]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no parties'}), 404
        
    @staticmethod
    def add_party(body):
        session = Session()
        
        try:
            id = int(body['id'])
        except:
            return jsonify({'ID must be an integer'}, 500)

        party = PartyDAO(id, body['name'], body['uuid'], datetime.now(), datetime.now())
        
        try:
            session.add(party)
            session.commit()
            session.refresh(party)
            session.close()
            return jsonify({'message': f'Successfully created party with id; {party.id}'}), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500
    
    @staticmethod
    def delete_party(p_id):
        session = Session()
        
        try:
            p_id = int(p_id)
        except:
            return jsonify({'ID must be an integer'}, 500)

        effected_rows = session.query(PartyDAO).filter(PartyDAO.id == p_id).delete()

        try:
            session.commit()
            session.close()
            if effected_rows == 0:
                return jsonify({'message': f'There is no party  with id {p_id}'}), 404
            else:
                return jsonify({'message': 'The party is removed'}), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500
