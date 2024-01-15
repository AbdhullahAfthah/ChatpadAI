from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    resource = relationship("Resource", back_populates="owner", uselist=False)


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pdf = Column(String, index=True, nullable=True)
    url = Column(URLType, index=True, nullable=True)

    owner = relationship("User", back_populates="resource")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
