from datetime import datetime

from flask import jsonify

from daos.vote_dao import VoteDAO
from db import Session
from sqlalchemy import desc
import uuid




class Vote:
    @staticmethod
    def create(body, session_id):
        session = Session()
        try:
            vote_id = int(body["id"])
        except:
            return jsonify({'ID must be an integer'}, 500)
        vote = VoteDAO(vote_id, str(uuid.uuid4()), body['voter_uuid'], session_id ,datetime.now(), body['member_uuid'])
        
        
        try:
            session.add(vote)
            session.commit()
            session.refresh(vote)
            session.close()

            text_out = {
                 "id": vote.id,
                 "uuid": vote.voter_uuid,
                 "member_uuid": vote.voter_uuid
            }
            return jsonify(text_out), 200
        except:
            session.close()
            return jsonify({'Could not place vote encountered error'}), 500

    @staticmethod
    def get_for_session(session_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        votes = session.query(VoteDAO).filter(VoteDAO.session_id == session_id).all()

        if len(votes) > 0:
            text_out = [{"uuid": vote.uuid, 
                         "voter_id": vote.voter_id,
                         "created_at": session.created_at,
                         "voted_for": vote.voted_for} for vote in votes]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no votes'}), 404
    
