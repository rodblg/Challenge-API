from sqlalchemy import Column, Integer, String,Numeric, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    balance = Column(Numeric, nullable=False, default=0)
    
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Numeric, nullable=False)
    name_movement = Column(String, nullable=False, default='')
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)