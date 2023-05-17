from datetime import datetime

from flask import jsonify

from daos.party_dao import PartyDAO
from db import Session
import uuid

class Party:

    @staticmethod
    def get_all():
        session = Session()
        parties = session.query(PartyDAO).all()

        if len(parties) > 0:
            text_out = [{"name": party.name, 
                         "created_at": party.created_at,
                         "edited_at": party.edited_at} for party in parties]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no parties'}), 404
        
    @staticmethod
    def get_one(party_id):
        session = Session()

        party = session.query(PartyDAO).filter(PartyDAO.id == int(party_id)).first()

        if party != None:
            text_out = {"id": party.id,
                        "name": party.name, 
                        "created_at": party.created_at,
                        "edited_at": party.edited_at}
            session.close()
            return jsonify(text_out)
        else:
            session.close()
            return jsonify({'message': f'There are no parties'}), 404
        
    @staticmethod
    def create(body):
        session = Session()
        party = PartyDAO(body["id"], body['name'], str(uuid.uuid4()), datetime.now(), datetime.now())

        try:
            session.add(party)
            session.commit()
            session.refresh(party)
            session.close()
            
            text_out = {
                "id": party.id,
                "name": party.name,
                "uuid": party.uuid,
                "created_at": party.created_at,
                "edited_at": party.created_at
            }
            return jsonify(text_out), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500
    
    @staticmethod
    def update(p_id, body):
        session = Session()
        effected_rows = session.query(PartyDAO).filter(PartyDAO.id == p_id).update(body)
        session.commit()
        session.close()
        return jsonify({'effected_rows': effected_rows}), 200
    
    @staticmethod
    def delete(p_id):
        session = Session()
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
