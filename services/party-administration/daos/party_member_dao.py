from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.party_dao import PartyDAO


class PartyMemberDAO(Base):
    __tablename__ = 'party_member'
    id = Column(Integer, primary_key=True)  # Auto generated primary key

    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)
    uuid = Column(String)

    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    # reference to status as foreign key relationship. This will be automatically assigned.
    party_id = Column(Integer, ForeignKey('party.id'))
    # party = relationship(PartyDAO.__name__, backref=backref("party", uselist=False))

    def __init__(self, id, first_name, last_name, status, uuid, party_id, created_at, edited_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.uuid = uuid
        self.party_id = party_id
        self.created_at = created_at
        self.edited_at = edited_at