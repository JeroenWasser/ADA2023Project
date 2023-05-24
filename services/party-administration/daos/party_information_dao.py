from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.party_dao import PartyDAO


class PartyInformationDAO(Base):
    __tablename__ = 'party_information'
    id = Column(Integer, primary_key=True)  # Auto generated primary key

    description = Column(String)

    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    # reference to status as foreign key relationship. This will be automatically assigned.
    party_id = Column(Integer, ForeignKey('party.id'))
    # party = relationship(PartyDAO.__name__, backref=backref("party", uselist=False))

    def __init__(self, id, description, party_id, created_at, edited_at):
        self.id = id
        self.description = description
        self.party_id = party_id
        self.created_at = created_at
        self.edited_at = edited_at