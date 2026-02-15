from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    is_admin = Column(Boolean, default=False)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, unique=True, index=True)
    tariff = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    notified = Column(Boolean, default=False)  # для отслеживания отправленных уведомлений
    created_at = Column(DateTime, default=datetime.utcnow())
    
    company = relationship("Company", back_populates="subscriptions")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    phone = Column(String)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="leads")
    
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    owner_telegram_id = Column(Integer)
    bot_token = Column(String, unique=True)
    name = Column(String)
    

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    owner_tg_id = Column(Integer, unique=True, nullable=False)
    # telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    
    trial_expires_at = Column(DateTime, nullable=True)  # для отслеживания окончания пробного периода
    created_at = Column(DateTime, default=datetime.utcnow())
    
    subscriptions = relationship("Subscription", back_populates="company")
    leads = relationship("Lead", back_populates="company")