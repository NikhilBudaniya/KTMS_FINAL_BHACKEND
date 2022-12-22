from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship,Mapped
from ..database import Base

class VendorModel(Base):
    __tablename__ = "vendor"

    name = Column(String)
    Phone = Column(Integer,)
    email = Column(String,nullable=False,primary_key=True)

    menu: Mapped[list["MenuModel"]] = relationship("MenuModel",back_populates="vendor")


class MenuModel(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("vendor.email",ondelete="CASCADE"),nullable=False) 
    breakfast = Column(String)
    lunch = Column(String)
    dinner = Column(Integer)
    date = Column(String)

    vendor: Mapped["VendorModel"] = relationship("VendorModel",back_populates="menu")

class SessionModel(Base):
    __tablename__="session"
    
    sessionId = Column(String, primary_key=True)
    email = Column(String)