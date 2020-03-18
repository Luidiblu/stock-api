import enum
import traceback
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    JSON,
    Boolean,
    ForeignKey,
    Date,
    UniqueConstraint,
    Float,
    Text,
    Enum,
)
from datetime import datetime
from sqlalchemy.orm import relationship
from stock_api.database import Base, DBObject, DBContext, engine


class User(Base, DBContext):
    __tablename__ = "user"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    stock_list_id = Column(Integer, ForeignKey("stock.user_list"))
    stock_list = relationship('Stock_List', foreign_keys=[stock_list_id])


class User_Stocks(Base, DBContext):
    __tablename__ = "stock_list"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("asset.user"))
    amount = Column(Integer)
    total_price = Column(Integer)
    purchase_at = Column(Date)
    value_at_purchase = Column(Integer)


class Stocks(Base, DBContext):
    __tablename__ = "stocks"
    __table_args__ = {"schema": "stock"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    code = Column(String)
    price = Column(String)
