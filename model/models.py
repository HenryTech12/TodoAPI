from db import db
from sqlalchemy import Column, Integer, String, Boolean

class Todo(db.Base):
    __tablename__ = "todo"
    
    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, index=True)
    item = Column(String, index=True)
    
    class Config:
        orm_mode=True
    
    
    
    