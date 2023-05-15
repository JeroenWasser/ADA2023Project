from daos.roles_updates_dao import RolesUpdatesDAO
from daos.roles_dao import RolesDAO
from db import Session
from datetime import datetime
from flask import jsonify

class RolesUpdates:
    @staticmethod
    def add_admin_role(uuid):
        session = Session()
        role_update = RolesUpdatesDAO(id = int(uuid)*99999-1, uuid = int(uuid), user_verified = False, admin_changed= True, partymember_changed= False, party_name= None,status= 'Pending',created_at= datetime.now(),edited_at= datetime.now())
        session.add(role_update)
        session.commit()
        session.close()
        return jsonify({'message': f'New admin role for user {uuid} is now waiting for verification.'}), 200

    @staticmethod
    def add_partymember_role(uuid, body):
        session = Session()
        role_update = RolesUpdatesDAO(id = int(uuid)*99999-2, uuid = int(uuid), user_verified= False, admin_changed= False, partymember_changed= True, party_name= body['party_name'], status = 'Pending', created_at= datetime.now(), edited_at= datetime.now())
        session.add(role_update)
        session.commit()
        session.close()
        return jsonify({'message': f'New party member role for user {uuid} is now waiting for verification.'}), 200

    @staticmethod
    def verify_role(uuid):
        session = Session()
        roles_updates = session.query(RolesUpdatesDAO).filter(RolesUpdatesDAO.uuid == int(uuid)).first()
        if roles_updates.admin_changed:
            session.close()
            return jsonify({'message': 'Please verify that you are a system administrator.'})
        if roles_updates.partymember_changed:
            party = roles_updates.party_name
            session.close()
            return jsonify({'message': f'Please verify that you are a member of {party}.'})
    
    def admin_role_verified(uuid, body):
        session = Session()
        roles_updates = session.query(RolesUpdatesDAO).filter(RolesUpdatesDAO.uuid == int(uuid), RolesUpdatesDAO.admin_changed == True, RolesUpdatesDAO.user_verified == False).first()
        current_info = session.query(RolesDAO).filter(RolesDAO.uuid == int(uuid)).first()
        if body['answer'] == 'yes':
            if roles_updates.admin_changed:
                current_info.admin = True
                current_info.edited_at = datetime.now()
            
            roles_updates.user_verified = True
            roles_updates.status = 'Accepted'
            roles_updates.edited_at = datetime.now()
            session.commit()
            session.close()
            return jsonify({'message': 'Your role has successfully been updated.'})
        if body['answer'] == 'no':
            roles_updates.user_verified = True
            roles_updates.status = 'Rejected'
            roles_updates.edited_at = datetime.now()
            session.commit()
            session.close()
            return jsonify({'message': 'Your choice has been saved.'})
    
    def member_role_verified(uuid, body):
        session = Session()
        roles_updates = session.query(RolesUpdatesDAO).filter(RolesUpdatesDAO.uuid == int(uuid), RolesUpdatesDAO.partymember_changed == True, RolesUpdatesDAO.user_verified == False).first()
        current_info = session.query(RolesDAO).filter(RolesDAO.uuid == int(uuid)).first()
        if body['answer'] == 'yes':
            if roles_updates.partymember_changed:
                current_info.partymember = True
                current_info.edited_at = datetime.now()
            
            roles_updates.user_verified = True
            roles_updates.status = 'Accepted'
            roles_updates.edited_at = datetime.now()
            session.commit()
            session.close()
            return jsonify({'message': 'Your role has successfully been updated.'})
        if body['answer'] == 'no':
            roles_updates.user_verified = True
            roles_updates.status = 'Rejected'
            roles_updates.edited_at = datetime.now()
            session.commit()
            session.close()
            return jsonify({'message': 'Your choice has been saved.'})


            
