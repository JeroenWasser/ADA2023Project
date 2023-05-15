from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from db import Base


class VoteDAO(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    uuid = Column(String)
    # reference to voter as foreign key relationship. This will be automatically assigned.
    voter_uuid = Column(String)
    # reference to session as foreign key relationship. This will be automatically assigned.
    session_id = Column(Integer, ForeignKey('voting_session.id'))
    voted_for = Column(String)

    created_at = Column(DateTime)



    def __init__(self, id, uuid, voter_uuid, session_id, created_at, voted_for):
        self.id = id
        self.uuid = uuid
        self.voter_uuid = voter_uuid
        self.session_id = session_id
        self.created_at = created_at
        self.voted_for = voted_for