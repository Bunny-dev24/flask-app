from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Customer(Base):
    """
    Customer model for storing customer-related information
    """
    __tablename__ = 'customers'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic Customer Information
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    
    # Optional Additional Information
    address = Column(Text)
    company = Column(String(100))
    
    # Timestamp Columns
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        """
        String representation of the Customer model
        """
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"

    def to_dict(self):
        """
        Convert the Customer model to a dictionary
        Useful for JSON serialization
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'company': self.company,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data):
        """
        Class method to create a Customer instance from a dictionary
        Useful for creating new customers from input data
        """
        return cls(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            company=data.get('company')
        )