from datetime import datetime

from flask import jsonify

from daos.session_dao import SessionDAO
from db import Session
from sqlalchemy import desc



class Session:
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
    def get():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        sessions = session.query(SessionDAO).all()

        if len(sessions) > 0:
            text_out = [{"uuid": session.uuid, 
                         "name": session.name,
                         "start_time": session.start_time,
                         "end_time": session.end_time,
                         "created_at": session.created_at,
                         "edited_at": session.edited_at} for session in sessions]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no sessions'}), 404
        
    @staticmethod
    def get_latest_session():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        session_object = session.query(SessionDAO).order_by(desc('start_time')).first()


        if session_object:
            text_out = {"uuid": session_object.uuid, 
                         "name": session_object.name,
                         "start_time": session_object.start_time,
                         "end_time": session_object.end_time,
                         "created_at": session_object.created_at,
                         "edited_at": session_object.edited_at}
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no sessions'}), 404
    
