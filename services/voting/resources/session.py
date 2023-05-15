from datetime import datetime

from flask import jsonify

from daos.session_dao import SessionDAO
from db import Session
from sqlalchemy import desc
import uuid




class Voting_Session:

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
    
    @staticmethod
    def create(body):
        session = Session()
        voting_session = SessionDAO(body["id"],
                                        body["name"], 
                                        body["start_time"], 
                                        body["end_time"],
                                        body["created_at"],
                                        body["edited_at"],
                                        body["uuid"])
        try:
            session.add(voting_session)
            session.commit()
            session.refresh(voting_session)
            session.close()
            return jsonify({'voting session added with uuid': voting_session.uuid}), 200
        except Exception as err:
            session.close()
            return jsonify({f'Could not create voting session encountered error: {err}'}), 500
