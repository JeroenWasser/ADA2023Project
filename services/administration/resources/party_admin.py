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
        date_now = datetime.now()
        party_admin = PartyAdminDAO(random.randint(5,10000),body['first_name'], body['last_name'], body['status'], body['uuid'], int(p_id), date_now, date_now)
        session.add(party_admin)
        session.commit()
        session.refresh(party_admin)
        session.close()
        text_out = {
            "id": party_admin.id,
            "first_name": party_admin.first_name,
            "last_name": party_admin.last_name,
            "status": party_admin.status,
            "uuid": party_admin.uuid,
            "party_id": p_id,
            "created_at": date_now,
            "edited_at": date_now
        }
        return jsonify(text_out), 200