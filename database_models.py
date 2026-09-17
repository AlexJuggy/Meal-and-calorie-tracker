from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float , Column, Integer , String, DateTime,ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    daily_goal = Column(Integer)
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__="meals"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    name = Column(String)
    calories = Column(Integer)
    logged_in=Column(DateTime)
    user = relationship("User", back_populates="meals")
    
