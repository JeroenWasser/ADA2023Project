from datetime import datetime

from flask import jsonify

from daos.party_member_dao import PartyMemberDAO
from db import Session


class PartyMember:
    @staticmethod
    def create(body):
        session = Session()
        party_member = PartyMemberDAO(body['first_name'], body['last_name'], body['status'], body['uuid'], datetime.now(), datetime.now())
        session.add(party_member)
        session.commit()
        session.refresh(party_member)
        session.close()
        return jsonify({'party_member_id': party_member.id}), 200

    @staticmethod
    def get(m_id):
        session = Session()
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
    def get_all():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        party_members = session.query(PartyMemberDAO).all()

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
    
    @staticmethod
    def update(uuid, body):
        session = Session()
        party_member = session.query(PartyMemberDAO).filter(PartyMemberDAO.uuid == uuid).first()
        if party_member:
            party_member.status = body['status']
            session.commit()
            session.close()
            return jsonify({'message': 'Party member information updated'}), 200
        else:
            session.close()
            return jsonify({'message': 'This user is not in the party database'}), 404