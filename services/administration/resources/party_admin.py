from datetime import datetime

from flask import jsonify

from daos.party_admin_dao import PartyAdminDAO
from db import Session
import uuid


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
        party_admin = PartyAdminDAO(body['first_name'], body['last_name'], p_id, body['status'], str(uuid.uuid4()), datetime.now(), datetime.now())
        session.add(party_admin)
        session.commit()
        session.refresh(party_admin)
        session.close()
        return jsonify(party_admin), 200