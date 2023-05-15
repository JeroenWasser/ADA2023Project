from datetime import datetime

from flask import jsonify

from daos.party_dao import PartyDAO
from db import Session


class Party:
    # @staticmethod
    # def create(body):
        # session = Session()
        # delivery = DeliveryDAO(body['customer_id'], body['provider_id'], body['package_id'], datetime.now(),
        #                        datetime.strptime(body['delivery_time'], '%Y-%m-%d %H:%M:%S.%f'),
        #                        StatusDAO(STATUS_CREATED, datetime.now()))
        # session.add(delivery)
        # session.commit()
        # session.refresh(delivery)
        # session.close()
        # return jsonify({'delivery_id': delivery.id}), 200

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
        voting_session = PartyDAO(body['name'], datetime.now(), datetime.now())
        session.add(voting_session)
        session.commit()
        session.refresh(voting_session)
        session.close()
        return jsonify({'voting_session_id': voting_session.id}), 200
    
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