from sqlalchemy import Column, String, Integer, DateTime

from db import Base


class SessionDAO(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String)

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    created_at = Column(DateTime)
    edited_at = Column(DateTime)

    uuid = Column(String)

    def __init__(self, name, start_time, end_time, created_at, edited_at, uuid):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at
        self.edited_at = edited_at
        self.uuid = uuid
