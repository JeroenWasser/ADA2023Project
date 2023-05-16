from datetime import datetime

from flask import jsonify

from daos.party_dao import PartyDAO
from db import Session


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
    def create(body):
        session = Session()
        party = PartyDAO(body["id"], body['name'], datetime.now(), datetime.now())
        session.add(party)
        session.commit()
        session.refresh(party)
        party_id = party.id
        session.close()
        return jsonify({'message': f"{party_id} is deployed as placeholder"})
    
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
        session.commit()
        session.close()
        return jsonify({'effected_rows': effected_rows}), 200