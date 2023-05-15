from sqlalchemy import Column, String, Integer, DateTime, Boolean

from db import Base

class RolesUpdatesDAO(Base):
    __tablename__ = 'roles_updates'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    uuid = Column(Integer, foreign_key='roles.uuid')
    user_verified = Column(Boolean)
    admin_changed = Column(Boolean)
    partymember_changed = Column(Boolean)
    party_name = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    def __init__(self, id, uuid, user_verified, admin_changed, partymember_changed, party_name,  status, created_at, edited_at):
        self.id = id
        self.uuid = uuid
        self.user_verified = user_verified
        self.admin_changed = admin_changed
        self.partymember_changed = partymember_changed
        self.party_name = party_name
        self.status = status
        self.created_at = created_at
        self.edited_at = edited_at