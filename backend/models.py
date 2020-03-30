from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    JSON,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db = create_engine(
    "postgresql+psycopg2://MCAdmin:uwq8SZYxC<V6HR2et["
    ":c5gW!wtC4Hm%e@responsible-citizen-db.cqtzg8fun5lr.us-east-2.rds.amazonaws"
    ".com:5432/responsible_citizen"
)
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
    __tablename__ = "accounts"

    id = Column(String(length=32), primary_key=True)
    name = Column(String(length=32))
    surname = Column(String(length=32))
    email = Column(String, unique=True)
    hashed_password = Column(String)
    username = Column(String, unique=True)
    created_at = Column(TIMESTAMP)
    hearts_rating = Column(Integer)
    type = Column(String)


class Sessions(base):
    __tablename__ = "sessions"

    um_accounts_id = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    session_id = Column(String(length=32), primary_key=True)
    created_at = Column(TIMESTAMP)


class Projects(base):
    __tablename__ = "projects"

    id = Column(String(length=32), primary_key=True)
    id_owner = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    name = Column(String(length=32))
    Description = Column(String)
    created_at = Column(TIMESTAMP)
    requested_participants = Column(Integer)
    is_active = Column(Boolean)
    upvotes = Column(Integer)
    downvotes = Column(Integer)


class Adresses(base):
    __tablename__ = "adresses"

    id = Column(String(length=32), primary_key=True)
    id_project = Column(
        String(length=32),
        ForeignKey(Projects.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    city = Column(String)
    zip_code = Column(String)
    street = Column(String)
    building_no = Column(Integer)
    flat_no = Column(Integer)
    exact_location = Column(Boolean)


class Comments(base):
    __tablename__ = "comments"

    id = Column(String(length=32), primary_key=True)
    id_owner = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    id_project = Column(
        String(length=32),
        ForeignKey(Projects.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    created_at = Column(TIMESTAMP)
    upvotes = Column(Integer)
    downvotes = Column(Integer)
    text = Column(String)


class InitiativesParticipants(base):
    __tablename__ = "initiatives_participants"

    id = Column(String(length=32), primary_key=True)
    id_participant = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    id_project = Column(
        String(length=32),
        ForeignKey(Projects.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    joined_at = Column(TIMESTAMP)
    role = Column(String)
    contributed = Column(Boolean)


class Votes(base):
    __tablename__ = "votes"

    id = Column(String(length=32), primary_key=True)
    type = Column(String)
    user_id = Column(
        String(length=32),
        ForeignKey(Accounts.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    object_id = Column(
        String(length=32)
    )
    is_upvote = Column(Boolean)


base.metadata.create_all(db)
