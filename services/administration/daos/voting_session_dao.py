from sqlalchemy import Column, String, Integer, DateTime

from db import Base


class VotingSessionDAO(Base):
    __tablename__ = 'voting_session'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    def __init__(self, id, name, start_time, end_time, created_at, edited_at):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at
        self.edited_at = edited_at
