from datetime import datetime
from daos.voting_session_dao import VotingSessionDAO
from flask import jsonify
import random

from db import Session


class VotingSession:
    @staticmethod
    def create(body):
        session = Session()
        voting_session = VotingSessionDAO(body["id"], body['name'], datetime.now(), body["end_time"], datetime.now(), datetime.now())
        session.add(voting_session)
        session.commit()
        session.refresh(voting_session)
        session.close()
        return jsonify({'voting_session_id': voting_session.id}), 200

    @staticmethod
    def get(vs_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        # parties = session.query(VotingSessionDAO).all()
        voting_session = session.query(VotingSessionDAO).filter(VotingSessionDAO.id == vs_id).first()
        text_out = [{"name": voting_session.name, 
                         "start_time": voting_session.start_time,
                        "end_time": voting_session.end_time,
                        "created_at": voting_session.created_at,
                        "edited_at": voting_session.edited_at}]
        session.close()
        return jsonify(text_out), 200
    
    @staticmethod
    def get_all():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        voting_sessions = session.query(VotingSession).all()

        if len(voting_sessions) > 0:
            text_out = [{
                "name": voting_session.name, 
                "start_time": voting_session.start_time,
                "end_time": voting_session.end_time,
                "created_at": voting_session.created_at,
                "edited_at": voting_session.edited_at
            } for voting_session in voting_sessions]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no voting sessions created yet'}), 404
        
    @staticmethod
    def delete(vs_id):
        session = Session()
        effected_rows = session.query(VotingSessionDAO).filter(VotingSessionDAO.id == vs_id).delete()

        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no party member with id {vs_id}'}), 404
        else:
            return jsonify({'message': f'The voting session {vs_id} is removed'}), 200
        
    def update(vs_id, body):
        session = Session()
        voting_session = session.query(VotingSessionDAO).filter(VotingSessionDAO.id == vs_id).first()
        # Update attributes from the body parameter
        voting_session.name = body.get('name', voting_session.name)
        voting_session.start_time = body.get('start_time', voting_session.start_time)
        voting_session.end_time = body.get('end_time', voting_session.end_time)
        voting_session.edited_at = datetime.now()
        voting_session.edited_at = datetime.now()
        session.commit()
        session.close()
        return jsonify({'message': f'The voting session {vs_id} is updated'}), 200