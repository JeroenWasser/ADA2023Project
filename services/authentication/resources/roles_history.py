from daos.roles_history_dao import RolesHistoryDAO
from daos.roles_dao import RolesDAO
from db import Session
from datetime import datetime
from flask import jsonify
from uuid import uuid4
import requests
import time

class RolesHistory:
    # @staticmethod
    # def add_admin_role(uuid):
    #     session = Session()
    #     user = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
    #     role_update = RolesHistoryDAO(update_uuid = str(uuid4()), user_id=user.id, user_verified = False, admin_changed= True, partymember_changed= False, party_name= None,status= 'Pending',created_at= datetime.now(),edited_at= datetime.now())
    #     session.add(role_update)
    #     session.commit()
    #     session.close()
    #     return jsonify({'message': f'New admin role for user {user.id} is now waiting for verification.'}), 200

    # @staticmethod
    # def add_partymember_role(uuid, body):
    #     session = Session()
    #     user = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
    #     role_update = RolesHistoryDAO(update_uuid = str(uuid4()), user_id = user.id, user_verified= False, admin_changed= False, partymember_changed= True, party_name= body['party_name'], status = 'Pending', created_at= datetime.now(), edited_at= datetime.now())
    #     session.add(role_update)
    #     session.commit()
    #     session.close()
    #     return jsonify({'message': f'New party member role for user {user.id} is now waiting for verification.'}), 200

    @staticmethod
    def add_role(uuid, body):
        session = Session()
        user = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
        if body['role'] == 'admin':
            role_update = RolesHistoryDAO(id = body['id'], update_uuid = str(uuid4()), user_id=user.id, user_verified = False, admin_changed= True, partymember_changed= False, party_name= body['party_name'],status= 'Pending',created_at= datetime.now(),edited_at= datetime.now())
            user_id = user.id
            session.add(role_update)
            session.commit()
            session.close()
            return jsonify({'message': f'New admin role for user {user_id} is now waiting for verification.'}), 200
        elif body['role'] == 'partymember':
            try:
                body['party_name']
            except KeyError:
                return jsonify({'message': f'Please provide a party name'}), 404
            role_update = RolesHistoryDAO(id = body['id'], update_uuid = str(uuid4()), user_id = user.id, user_verified= False, admin_changed= False, partymember_changed= True, party_name= body['party_name'], status = 'Pending', created_at= datetime.now(), edited_at= datetime.now())
            user_id = user.id
            session.add(role_update)
            session.commit()
            session.close()
            return jsonify({'message': f'New party member role for user {user_id} is now waiting for verification.'}), 200
        else:
            return jsonify({'message': f'"{body["role"]}" is an undefined role, please try again.'}), 404

    @staticmethod
    def verify_role(uuid):
        session = Session()
        user = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
        roles_updates = session.query(RolesHistoryDAO).filter(RolesHistoryDAO.user_id == user.id).first()
        if roles_updates.admin_changed:
            session.close()
            return jsonify({'message': 'Please verify that you are a system administrator.'})
        if roles_updates.partymember_changed:
            party = roles_updates.party_name
            session.close()
            return jsonify({'message': f'Please verify that you are a member of {party}.'})
    
    # def admin_role_verified(uuid, body):
    #     session = Session()
    #     roles_updates = session.query(RolesHistoryDAO).filter(RolesHistoryDAO.update_uuid == uuid, RolesHistoryDAO.admin_changed == True, RolesHistoryDAO.user_verified == False).first()
    #     current_info = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
    #     if body['answer'] == 'yes':
    #         if roles_updates.admin_changed:
    #             current_info.admin = True
    #             current_info.edited_at = datetime.now()
            
    #         roles_updates.user_verified = True
    #         roles_updates.status = 'Accepted'
    #         roles_updates.edited_at = datetime.now()
    #         session.commit()
    #         session.close()
    #         return jsonify({'message': 'Your role has successfully been updated.'})
    #     if body['answer'] == 'no':
    #         roles_updates.user_verified = True
    #         roles_updates.status = 'Rejected'
    #         roles_updates.edited_at = datetime.now()
    #         session.commit()
    #         session.close()
    #         return jsonify({'message': 'Your choice has been saved.'})
    
    # def member_role_verified(uuid, body):
    #     session = Session()
    #     roles_updates = session.query(RolesHistoryDAO).filter(RolesHistoryDAO.update_uuid == uuid, RolesHistoryDAO.partymember_changed == True, RolesHistoryDAO.user_verified == False).first()
    #     current_info = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
    #     if body['answer'] == 'yes':
    #         if roles_updates.partymember_changed:
    #             current_info.partymember = True
    #             current_info.edited_at = datetime.now()
            
    #         roles_updates.user_verified = True
    #         roles_updates.status = 'Accepted'
    #         roles_updates.edited_at = datetime.now()
    #         session.commit()
    #         session.close()
    #         return jsonify({'message': 'Your role has successfully been updated.'})
    #     if body['answer'] == 'no':
    #         roles_updates.user_verified = True
    #         roles_updates.status = 'Rejected'
    #         roles_updates.edited_at = datetime.now()
    #         session.commit()
    #         session.close()
    #         return jsonify({'message': 'Your choice has been saved.'})

    @staticmethod
    def role_verified(uuid, body):
        session = Session()
        user = session.query(RolesDAO).filter(RolesDAO.uuid == uuid).first()
        if body['role'] == 'admin':
            role_update = session.query(RolesHistoryDAO).filter(RolesHistoryDAO.user_id == user.id, RolesHistoryDAO.admin_changed == True).first()
        elif body['role'] == 'partymember':
            role_update = session.query(RolesHistoryDAO).filter(RolesHistoryDAO.user_id == user.id, RolesHistoryDAO.partymember_changed == True).first()
        else:
            return jsonify({'message': f'"{body["role"]}" is an undefined role, please try again.'}), 404
        
        if body['answer'] == 'yes':
            if role_update.partymember_changed:
                user.partymember = True
                user.edited_at = datetime.now()
            elif role_update.admin_changed:
                user.admin = True
                user.edited_at = datetime.now()

            role_update.status = 'Accepted'
            role_update.user_verified = True
            role_update.edited_at = datetime.now()
            session.commit()
            session.close()
            if body['role'] == 'admin':
                x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/administration/user/{uuid}/status',
                                  json = {"status": "accepted"})
                if x.status_code != 200:
                    print('failed once, trying again')
                    time.sleep(1)
                    x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/administration/user/{uuid}/status',
                                  json = {"status": "accepted"})
                    if x.status_code != 200:
                        return jsonify({'message': f'PUT request failed with code {x.statuscode}'})
                if x.status_code == 200:
                    return jsonify({'message': 'Your role has successfully been updated.'})
            if body['role'] == 'partymember':
                x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/party-managment/user/{uuid}/status',
                                  json = {"status": "accepted"})
                if x.status_code != 200:
                    print('failed once, trying again')
                    time.sleep(1)
                    x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/party-managment/user/{uuid}/status',
                                  json = {"status": "accepted"})
                    if x.status_code != 200:
                        return jsonify({'message': f'PUT request failed with code {x.statuscode}'})
                if x.status_code == 200:
                    return jsonify({'message': 'Your role has successfully been updated.'})
        if body['answer'] == 'no':
            role_update.user_verified = True
            role_update.status = 'Rejected'
            role_update.edited_at = datetime.now()
            session.commit()
            session.close()
            if body['role'] == 'admin':
                x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/administration/user/{uuid}/status',
                                  data = {"status": "rejected"})
                if x.status_code != 200:
                    print('failed once, trying again')
                    time.sleep(1)
                    x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/administration/user/{uuid}/status',
                                  data = {"status": "rejected"})
                    if x.status_code != 200:
                        return jsonify({'message': f'PUT request failed with code {x.statuscode}'})
                if x.status_code == 200:
                    return jsonify({'message': 'Your role has successfully been updated.'}), 200
            if body['role'] == 'partymember':
                x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/party-managment/user/{uuid}/status',
                                  data = {"status": "rejected"})
                if x.status_code != 200:
                    print('failed once, trying again')
                    time.sleep(1)
                    x = requests.put(f'https://api-gateway-lf6x6a722q-uc.a.run.app/v1/party-managment/user/{uuid}/status',
                                  data = {"status": "rejected"})
                    if x.status_code != 200:
                        return jsonify({'message': f'PUT request failed with code {x.statuscode}'})
                if x.status_code == 200:
                    return jsonify({'message': 'Your choice has been saved.'})
        



            
