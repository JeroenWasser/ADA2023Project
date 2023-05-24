from datetime import datetime
from daos.voting_session_dao import VotingSessionDAO
from flask import jsonify
import uuid

from db import Session


class VotingSession:
    @staticmethod
    def create(body):
        session = Session()
        voting_session = VotingSessionDAO(body["id"], body['name'], datetime.now(), body["end_time"], datetime.now(), datetime.now(), str(uuid.uuid4()))
        
        try:
            session.add(voting_session)
            session.commit()
            session.refresh(voting_session)
            session.close()
            
            text_out = {
                "id": voting_session.id,
                "name": voting_session.name,
                "start_time": voting_session.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": voting_session.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "created_at": voting_session.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "edited_at": voting_session.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "uuid": voting_session.uuid
            }
            return jsonify(text_out), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500   

    @staticmethod
    def get(vs_id):
        session = Session()
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
        voting_sessions = session.query(VotingSessionDAO).all()

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

        try:
            session.commit()
            session.close()
            
            text_out = {
                "id": voting_session.id,
                "name": voting_session.name,
                "start_time": voting_session.start_time,
                "end_time": voting_session.end_time,
                "created_at": voting_session.created_at,
                "edited_at": voting_session.created_at,
                "uuid": voting_session.uuid
            }
            return jsonify(text_out), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500   