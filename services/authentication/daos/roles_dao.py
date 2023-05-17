from sqlalchemy import Column, String, Integer, DateTime, Boolean

from db import Base

class RolesDAO(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto generated primary key
    uuid = Column(String)
    admin = Column(Boolean)
    partymember = Column(Boolean)
    citizen = Column(Boolean)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    def __init__(self, id, uuid, admin, partymember, citizen, created_at, edited_at):
        self.id = id
        self.uuid = uuid
        self.admin = admin
        self.partymember = partymember
        self.citizen = citizen
        self.created_at = created_at
        self.edited_at = edited_at