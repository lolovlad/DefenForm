import datetime
import enum
from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, Float, Text, MetaData
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.description}"


class TypeService(db.Model):
    __tablename__ = "type_service"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    phone = Column(String(20), nullable=False)
    email = Column(String(32), nullable=False)

    id_role = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role")

    id_type_service = Column(Integer, ForeignKey('type_service.id'), nullable=True)
    type_service = relationship("TypeService")

    password_hash = Column(String, nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, val):
        self.password_hash = generate_password_hash(val)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymics[0]}."


class ServiceSelection(db.Model):
    __tablename__ = "service_selection"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"{self.name}"


class Priority(db.Model):
    __tablename__ = "priority"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    coast = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"{self.name}"


class Status(db.Model):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class Claim(db.Model):
    __tablename__ = "claim"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    datetime_claim = Column(DateTime, nullable=False, default=datetime.datetime.now())
    address = Column(String, nullable=False)
    description = Column(Text)

    id_user = Column(Integer, ForeignKey('users.id'))
    id_worker = Column(Integer, ForeignKey('users.id'), nullable=True)
    id_service_selection = Column(Integer, ForeignKey('service_selection.id'))
    id_priority = Column(Integer, ForeignKey('priority.id'), nullable=True)
    id_status = Column(Integer, ForeignKey('status.id'), nullable=True)

    user = relationship(User, foreign_keys=[id_user])
    worker = relationship(User, foreign_keys=[id_worker])
    service_selection = relationship(ServiceSelection, foreign_keys=[id_service_selection])
    priority = relationship(Priority, foreign_keys=[id_priority])
    status = relationship(Status, foreign_keys=[id_status])
    contract = relationship("Contract", backref="claim", uselist=False)


class Contract(db.Model):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    id_claim = Column(Integer, ForeignKey('claim.id'))
    number = Column(Integer, nullable=False, server_default="1")

    datetime_contract = Column(DateTime, nullable=True, default=datetime.datetime.now())
    description = Column(Text)
    terms_and_conditions = Column(Text)
    coast = Column(Float)