from sqlalchemy import Column, String, Integer, DateTime

from db import Base


class PartyDAO(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)


    def __init__(self, id, name, created_at, edited_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.edited_at = edited_at