from datetime import datetime

from flask import jsonify

from daos.vote_dao import VoteDAO
from db import Session
from sqlalchemy import desc



class Vote:
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
    def get_for_session(session_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        votes = session.query(VoteDAO).filter(VoteDAO.session_id == session_id).all()

        if len(votes) > 0:
            text_out = [{"uuid": vote.uuid, 
                         "voter_id": vote.voter_id,
                         "created_at": session.created_at} for vote in votes]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no votes'}), 404
    
