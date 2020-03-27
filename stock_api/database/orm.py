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


class User(Base, DBObject):
    __tablename__ = "user"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)

    wallets = relationship('Wallet')


class Wallet(Base, DBObject):
    __tablename__ = "wallet"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("asset.user.id"))
    Name = Column(String)
    description = Column(String)

    stocks = relationship('Transaction')


class Stock(Base, DBObject):
    __tablename__ = "stock"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    code = Column(String)


class StockHistory(Base, DBObject):
    __tablename__ = "stock_history"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    stock_id = Column(Integer, ForeignKey("asset.stock.id"))
    date = Column(Date)
    open = Column(Integer)
    close = Column(Integer)
    min_daily_value = Column(Integer)
    max_daily_value = Column(Integer)


class Transaction(Base, DBObject):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "asset"}
    id = Column(Integer, autoincrement=True, primary_key=True)
    stock_id = Column(Integer, ForeignKey("asset.stock.id"))
    wallet_id = Column(Integer, ForeignKey("asset.wallet.id"))
    transaction_type = Column(String)  # buy / sell
    purchased_at = Column(Date)
    purchased_value = Column(Integer)
    amount = Column(Integer)
