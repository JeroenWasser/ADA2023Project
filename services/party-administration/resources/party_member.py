from datetime import datetime

from flask import jsonify

from daos.party_member_dao import PartyMemberDAO
from db import Session
import uuid

class PartyMember:
    @staticmethod
    def create(body):
        session = Session()

        try:
            id = int(body['id'])
        except:
            return jsonify({'ID must be an integer'}, 500)

        party_member = PartyMemberDAO(id, body['first_name'], body['last_name'], 'pending', str(uuid.uuid4()), body['party_id'], datetime.now(), datetime.now())
        
        try:
            session.add(party_member)
            session.commit()
            session.refresh(party_member)
            session.close()

            text_out = {
                 "id": party_member.id,
                 "first_name": party_member.first_name,
                 "last_name": party_member.last_name,
                 "uuid": party_member.uuid,
                 "status": party_member.status,
                 "party_id": party_member.party_id,
                 "created_at": party_member.created_at,
                 "edited_at": party_member.edited_at
            }
            return jsonify(text_out), 200
        except Exception as err:
            session.close()
            return jsonify({'message': f'Could not create party, encountered error: {err}'}), 500

    @staticmethod
    def get(m_id):
        session = Session()

        try:
            m_id = int(m_id)
        except:
            return jsonify({'ID must be an integer'}, 500)

        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        party_member = session.query(PartyMemberDAO).filter(PartyMemberDAO.id == m_id).first()

        if party_member:
            text_out = {
                "first_name": party_member.first_name,
                "last_name": party_member.first_name,
                "status": party_member.first_name,
                "uuid": party_member.first_name,
                "created_at": party_member.created_at,
                "edited_at": party_member.edited_at
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no Party Member with id {m_id}'}), 404
        
    @staticmethod
    def delete(m_id):
        session = Session()

        try:
            m_id = int(m_id)
        except:
            return jsonify({'ID must be an integer'}, 500)
        
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        effected_rows = session.query(PartyMemberDAO).filter(PartyMemberDAO.id == m_id).delete()

        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no party member with id {m_id}'}), 404
        else:
            return jsonify({'message': 'The party member is removed'}), 200

    @staticmethod
    def get_party_members(p_id):
        session = Session()

        try:
            p_id = int(p_id)
        except:
            return jsonify({'ID must be an integer'}, 500)
        
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        party_members = session.query(PartyMemberDAO).filter(PartyMemberDAO.party_id == p_id).all()

        if len(party_members) > 0:
            text_out = [{
                "first_name": party_member.first_name,
                "last_name": party_member.first_name,
                "status": party_member.first_name,
                "uuid": party_member.first_name,
                "created_at": party_member.created_at,
                "edited_at": party_member.edited_at
            } for party_member in party_members]
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There are no party members in this party'}), 404