from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base
from app.models.enums import TransactionType, TransactionStatus

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
