from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from db import Base


class PartyAdminDAO(Base):
    __tablename__ = 'party_admin'
    id = Column(Integer, primary_key=True)  # Auto generated primary key

    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)
    uuid = Column(String)
    party_id = Column(Integer)

    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    # reference to status as foreign key relationship. This will be automatically assigned.
    party_id = Column(Integer, ForeignKey('party.id'))

    def __init__(self, id, first_name, last_name, status, uuid, party_id, created_at, edited_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.party_id = party_id
        self.status = status
        self.uuid = uuid
        self.created_at = created_at
        self.edited_at = edited_at