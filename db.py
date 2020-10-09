from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):

    __tablename__ = "message"

    message_id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False)
    username = Column(String, nullable=False)
    content = Column(String, nullable=False)

    def __init__(self, timestamp, username, content):
        self.timestamp = timestamp
        self.username = username
        self.content = content
    
    

    
        
