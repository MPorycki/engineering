from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///baza.db")
base = declarative_base()
Session = sessionmaker(db)
session = Session()


@contextmanager
def session_scope(_session=None):
    if _session is None:
        _session = Session()

    try:
        yield _session
        _session.commit()
    except Exception as e:
        _session.rollback()
        raise e
    finally:
        _session.close()


class Accounts(base):
    """
    Table representing user accounts in the application.

    :account_type: Can have one of 3 values = "hairdresser", "customer", "admin"
    """
    __tablename__ = "accounts"

    id = Column(String(length=32), primary_key=True)
    first_name = Column(String(length=32))
    last_name = Column(String(length=32))
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP)
    account_type = Column(String)
    # salonId = Column(String(length=32), ForeignKey)


class Sessions(base):
    __tablename__ = "sessions"

    account_id = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    session_id = Column(String(length=32), primary_key=True)
    created_at = Column(TIMESTAMP)


class Services(base):
    __tablename__ = "services"

    id = Column(String(length=32), primary_key=True)
    name = Column(String(length=32))
    price = Column(Float, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP)
    gender = Column(String)
    service_duration = Column(Integer)


class Adresses(base):
    __tablename__ = "adresses"

    id = Column(String(length=32), primary_key=True)
    # salon_id
    city = Column(String)
    zip_code = Column(String)
    street = Column(String)
    building_no = Column(Integer)
    number_of_seats = Column(Integer)

base.metadata.create_all(db)
