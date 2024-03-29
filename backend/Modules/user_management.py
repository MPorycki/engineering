import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid

from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError

from models import Accounts, Sessions, ResetTokens, session_scope
from Modules.crud_common import *
from Modules.salons import salon_has_hairdresser_spot
from settings import FRONTEND_URL, MAIL_ADRESS, MAIL_PASSWORD


# CREATE

def register_user(
        email: str,
        raw_password: str,
        first_name: str,
        last_name: str,
        account_type: str,
        salon_id: str,
) -> dict:
    """
    Registers the user by creating an account record in the database
    :param email: email of the user
    :param raw_password: direct password provided by the user into the form
    :param first_name: first name of the user
    :param last_name: last name of the user
    :param account_type: user or hairdresser
    :param salon_id: ID of the salon, in case the user is a hairdresser
    :return: Payload with data regarding the registration
    """
    payload = dict()
    payload["success"] = False
    payload["email_taken"] = user_with_given_email_exists(email)
    if payload["email_taken"]:
        return payload
    if account_type == "hairdresser":
        if not salon_has_hairdresser_spot(salon_id):
            return payload
    account_id = uuid.uuid4().hex
    password = sha256_crypt.hash(raw_password)
    new_user = Accounts(
        id=account_id,
        email=email,
        hashed_password=password,
        created_at=datetime.datetime.utcnow(),
        first_name=first_name,
        last_name=last_name,
        account_type=account_type,
        salon_id=salon_id
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
            user.name = user_data["name"]
            user.surname = user_data["surname"]
            user.email = user_data["email"]
            session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def handle_password_reset_request(email: str):
    """
    Handles the request by sending a reset password link to users' email
    """
    try:
        with session_scope() as session:
            account = session.query(Accounts).filter(Accounts.email == email).first()
            if account:
                _id = uuid.uuid4().hex
                token = ResetTokens(
                    id=_id,
                    account_id=account.id,
                    created_at=datetime.datetime.utcnow()
                )
                session.add(token)
                email_message = prepare_reset_link_message(_id, account.email, account.first_name)
                send_reset_link(email_message, account.email)
            return True
    except Exception as e:
        return False


def prepare_reset_link_message(token_id: str, email: str, first_name: str):
    message = MIMEMultipart()
    message_body = (
        "<html><head></head>"
        "<body>"
        f"Cześć, {first_name}!<br><br> "
        f"Pod tym <a href={FRONTEND_URL}#/passreset?token={token_id}>linkiem<a/> możesz zresetować swoje hasło.<br>"
        "<br>Salony Marco Polo"
        "</body>"
        "</html>"
    )
    message["From"] = "Salony Fryzjerskie Marco Polo"
    message["To"] = email
    message["Subject"] = "Twoja prośba o reset hasła"
    message.attach(MIMEText(message_body, "html"))

    return message.as_string()


def send_reset_link(message: str, account_email: str):
    # Login to the mailbox
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(MAIL_ADRESS, MAIL_PASSWORD)
        server.sendmail(MAIL_ADRESS, account_email, message)


def change_password(token_id: str, new_password: str) -> bool:
    """
    Changes the password for the user
    :param token_id: Token that is used to change password. Should be removed upon completion
    :param new_password: user's new password
    :return: True if the change was successful, False if there were any errors
    """
    try:
        with session_scope() as session:
            token = fetch_object(ResetTokens, token_id)
            if not token_valid(token):
                return False
            user = session.query(Accounts).filter(Accounts.id == token["account_id"]).first()
            new_password_hash = sha256_crypt.hash(new_password)
            user.hashed_password = new_password_hash
            delete_object(ResetTokens, token_id)
            return True
    except Exception as e:
        print(e)
        return False


def token_valid(token: dict) -> bool:
    """
    Checks whether reset password token is still valid and can
    be used ror password reset.
    :param token: Token object as a dict
    :return: Boolean stating whether the token can still be used to
    reset password
    """
    if token["created_at"] < (datetime.datetime.utcnow() - datetime.timedelta(days=7)):
        return False
    else:
        return True


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
    new_session = Sessions(
        account_id=account_id, session_id=session_id,
        created_at=datetime.datetime.now()
    )
    with session_scope() as session:
        session.add(new_session)
    return session_id


def session_is_valid(session_id: str, account_id: str) -> bool:
    """
    Verifies whether a particular session exists and is still valid for a particular user.
    Session invalidates after 7 days.
    :return: Boolean value confirming whether the session exists or not
    """
    with session_scope() as session:
        session = (
            session.query(Sessions).filter(Sessions.session_id == session_id,
                                           Sessions.account_id == account_id, ).first()
        )
        if not session:
            return False
        if session.created_at < (datetime.datetime.utcnow() - datetime.timedelta(days=7)):
            logout(session_id)
            return False
        return True


def logout(session_id: str) -> bool:
    """
    Logouts the user based on session_id and account_id
    :return: True if the session was removed, False if the given session does not exists for this account
    """
    try:
        with session_scope() as session:
            session.query(Sessions).filter(
                Sessions.session_id == session_id
            ).delete()
            return True
    except Exception as e:
        return False


def get_hairdressers_in_salon(salon_id: str):
    """
    Return the names of all hairdressers working in the given salon
    :param salon_id: uuid of the salon
    :return:
    """
    result = {"Hairdressers": []}
    with session_scope() as session:
        hairdressers = session.query(Accounts).filter(
            Accounts.salon_id == salon_id).all()
        for hairdresser in hairdressers:
            result["Hairdressers"].append(
                {"id": hairdresser.id, "firstName": hairdresser.first_name,
                 "lastName": hairdresser.last_name})
        return result


def is_customer(account_id: str) -> bool:
    with session_scope() as session:
        user = session.query(Accounts).filter(Accounts.id == account_id).first()
        if user.account_type == "customer":
            return True
        else:
            return False


def can_access_admin(session_id, account_id):
    if session_is_valid(session_id, account_id):
        with session_scope() as session:
            if session.query(Accounts.is_admin).filter(Accounts.id == account_id).first()[0]:
                return True
    return False


def account_data_to_dict(account: Accounts) -> dict:
    """
    Converts account data to a dict with keys relevant to what is shown on the frontend
    :param account: Account from which the data should be extracted
    :return: Dict with id, first, last names and email of the provided account
    """
    return {"id": account.id, "firstName": account.first_name, "lastName": account.last_name,
            "email": account.email}


def get_account_data(account_id: str) -> dict:
    """
    Provides relevant account data
    :param account_id: Id for which the data isto be returned
    :return: Dict with the relevant data
    """
    with session_scope() as session:
        account = session.query(Accounts.first_name, Accounts.last_name, Accounts.created_at,
                                Accounts.email, Accounts.id).filter(
            Accounts.id == account_id).first()
        return account_data_to_dict(account)


def get_all_customers_data() -> dict:
    """
    Provides relevant data about all customers.
    :return: Dict with basic data of all customers
    """
    with session_scope() as session:
        accounts = session \
            .query(Accounts.first_name, Accounts.last_name, Accounts.created_at, Accounts.email,
                   Accounts.id) \
            .filter(Accounts.account_type == "customer") \
            .order_by(Accounts.last_name).all()
    result = []
    for account in accounts:
        result.append(account_data_to_dict(account))
    return {"accounts": result}
