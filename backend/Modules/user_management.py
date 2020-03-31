import datetime
import uuid

from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError

from models import Accounts, Sessions, session_scope
from .crud_common import *


# CREATE


def register_user(
        email: str,
        raw_password: str,
        first_name: str,
        last_name: str,
        account_type: str,
) -> dict:
    """
    Registers the user by creating an account record in the database
    :param email: email of the user
    :param raw_password: direct password provided by the user into the form
    :param first_name: first name of the user
    :param last_name: last name of the user
    :param account_type: user or admin
    :return: Payload with data regarding the registration
    """
    payload = dict()
    payload["success"] = False
    payload["email_taken"] = user_with_given_email_exists(email)
    if payload["email_taken"]:
        return payload
    account_id = uuid.uuid4().hex
    password = sha256_crypt.hash(raw_password)
    new_user = Accounts(
        id=account_id,
        email=email,
        hashed_password=password,
        created_at=datetime.datetime.now(),
        first_name=first_name,
        last_name=last_name,
        type=account_type,
    )
    try:
        with session_scope() as session:
            session.add(new_user)
            payload["success"] = True
    except IntegrityError:
        return payload
    return payload


def user_with_given_email_exists(email: str) -> bool:
    """
    Verifies whether the provided email already belongs to an existing user
    :param email: Provided email
    :return: Boolean with the result of the check of email existence
    """
    with session_scope() as session:
        exists_instance = (
            session.query(Accounts).filter(Accounts.email == email).exists()
        )
        return session.query(exists_instance).scalar()


# UPDATE


def update_user(user_data: dict) -> bool:
    """
    Update user data
    :param user_data: data of the given user account to be updated
    :return:
    """
    try:
        with session_scope() as session:
            user = (
                session.query(Accounts)
                    .filter(Accounts.id == user_data["user_id"])
                    .first()
            )
            user.username = user_data["login"]
            user.name = user_data["name"]
            user.surname = user_data["surname"]
            user.email = user_data["email"]
            session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def change_password(account_id: str, new_password: str) -> bool:
    """
    Changes the password for the user
    :param account_id: user's account_id
    :param new_password: user's new password
    :return: True if the change was successful, False if there were any errors
    """
    with session_scope() as session:
        user = get_object(Accounts, account_id)
        new_password_hash = sha256_crypt.hash(new_password)
        user.hashed_password = new_password_hash
        session.commit()
        return True
    return False


# AUTHENTICATION


def login(email: str, raw_password: str) -> dict:
    """
    Log ins the user based on the username and password they provide
    :param email: email of the user
    :param raw_password:direct password inputted by the user into the form
    :return: Session_id and the corresponding account_id or (None, None) if failed
    """
    payload = dict()
    payload["session_id"] = None
    payload["account_id"] = None
    payload["correct_pass"] = False
    payload["email_exists"] = True
    if not user_with_given_email_exists(email):
        payload["email_exists"] = False
        return payload
    with session_scope() as session:
        user = session.query(Accounts).filter(Accounts.email == email).first()
        encrypted_from_db = user.hashed_password
        account_id = user.id
    if sha256_crypt.verify(raw_password, encrypted_from_db):
        payload["session_id"] = create_session_for_user(account_id)
        payload["account_id"] = account_id
        payload["correct_pass"] = True
        return payload
    else:
        return payload


def create_session_for_user(account_id: str) -> str:
    """
    Creates session for the given user
    :param account_id:
    :return: newly created session_id
    """
    session_id = uuid.uuid4().hex
    created_at = str(datetime.datetime.now())
    new_session = Sessions(
        um_accounts_id=account_id, session_id=session_id, created_at=created_at
    )
    with session_scope() as session:
        session.add(new_session)
    return session_id


def session_exists(session_id: str, account_id: str) -> bool:
    """
    Verifies whether a particular session exists for a particular user
    :return: Boolean value confirming whether the session exists or not
    """
    with session_scope() as session:
        exists_object = (
            session.query(Sessions)
                .filter(
                Sessions.session_id == session_id,
                Sessions.um_accounts_id == account_id,
            )
                .exists()
        )
        return session.query(exists_object).scalar()


def logout(session_id: str, account_id: str) -> bool:
    """
    Logouts the user based on session_id and account_id
    :return: True if the session was removed, False if the given session does not exists for this account
    """
    if session_exists(session_id, account_id):
        with session_scope() as session:
            session.query(Sessions).filter(
                Sessions.session_id == session_id
            ).delete()
            return True
    return False
