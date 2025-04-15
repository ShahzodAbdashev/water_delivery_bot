import asyncio

from sqlalchemy import String, Integer, DateTime, Boolean, Column, ForeignKey, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from utils.config import settings

engine = create_async_engine(settings.DB_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=False)
    language = Column(String(100))
    telegram_id = Column(String(100))

    orders = relationship('Order', back_populates='user')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    image = Column(String(300), nullable=False)
    price = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)

    orders = relationship('Order', back_populates='product')  

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    product_id = Column(ForeignKey('products.id', ondelete='CASCADE')) 
    quantity = Column(Integer)
    delivery_time = Column(String(100))
    location = Column(String(100))
    is_delivered = Column(Boolean, default=False)

    product = relationship('Product', back_populates='orders')  
    user = relationship('User', back_populates='orders')