from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from db import Base


class PartyInformationDAO(Base):
    __tablename__ = 'party_information'
    id = Column(Integer, primary_key=True)  # Auto generated primary key

    description = Column(String)

    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    # reference to status as foreign key relationship. This will be automatically assigned.
    party_id = Column(Integer, ForeignKey('party.id'))

    def __init__(self, description, party_id, created_at, edited_at):
        self.description = description
        self.party_id = party_id
        self.created_at = created_at
        self.edited_at = edited_at