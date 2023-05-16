from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

from db import Base

class RolesHistoryDAO(Base):
    __tablename__ = 'roles_history'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto generated primary key
    update_uuid = Column(String)
    user_id = Column(Integer, ForeignKey('roles.id'))
    user_verified = Column(Boolean)
    admin_changed = Column(Boolean)
    partymember_changed = Column(Boolean)
    party_name = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    def __init__(self, id, update_uuid, user_id, user_verified, admin_changed, partymember_changed, party_name,  status, created_at, edited_at):
        self.id = id
        self.update_uuid = update_uuid
        self.user_id = user_id
        self.user_verified = user_verified
        self.admin_changed = admin_changed
        self.partymember_changed = partymember_changed
        self.party_name = party_name
        self.status = status
        self.created_at = created_at
        self.edited_at = edited_at