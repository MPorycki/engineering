import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from models import Salons, session_scope
from Modules.adresses import create_adress


def create_salon(salon_data: dict) -> dict:
    """
    Create new salon based on provided data
    :param salon_data: JSON with salon data
    :return: Dict with info about the success or failure of the creation
    """
    try:
        validate_salon(salon_data)
    except IntegrityError as e:
        return {"success": False, "error": str(e)}
    _id = uuid.uuid4().hex
    try:
        adress_id = create_adress(salon_data['adress'], _id)
    except Exception as e:
        return {"success": False, "error": str(e)}
    new_service = Salons(
        id=_id,
        adress_id=adress_id,
        opening_hour=salon_data["opening_hour"],
        closing_hour=salon_data["closing_hour"],
        created_at=datetime.datetime.now()
    )
    try:
        with session_scope() as session:
            session.add(new_service)
            return {"success": True}
    except IntegrityError as e:
        return {"success": False, "error": str(e)}


def validate_salon(data):
    pass


def update_salon():
    pass
