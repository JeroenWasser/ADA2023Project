from datetime import datetime

from flask import jsonify

from daos.party_admin_dao import PartyAdminDAO
from db import Session
import random


class PartyAdmin:
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
    def create(p_id, body):
        session = Session()
        party_admin = PartyAdminDAO(random.randint(5,10000),body['first_name'], body['last_name'], body['status'], body['uuid'], int(p_id), datetime.now(), datetime.now())
        session.add(party_admin)
        session.commit()
        session.refresh(party_admin)
        session.close()
        return jsonify(party_admin), 200

    @staticmethod
    def create(uuid, body):
        session = Session()
        party_admin = session.query(PartyAdminDAO).filter(PartyAdminDAO.uuid == uuid).first()
        if party_admin:
            party_admin.status = body['status']
            session.commit()
            session.close()
            return jsonify({'message': 'Party admin information updated'}), 200
        else:
            session.close()
            return jsonify({'message': 'This user is not in the party admin database'}), 404
        