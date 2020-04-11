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
    """
    Checks input service data and makes sure it fulfills all the requirements
    :param data: Dict with at least the following schema:
    {"opening_hour": "", "closing_hour": ""}
    and requirements for the data:
    "opening_hour" -> Must be an hour between 06:00 and 10:00
    "closing_hour" -> Must be an hour between 16:00 and 20:00
    The open time (closing_hour - opening_hour) must be at least 8 hours
    To unify the time, it will be converted into minutes into the day beforehand.
    :return:
    """
    opening_hour = minutes_into_the_day(data["opening_hour"])
    closing_hour = minutes_into_the_day(data["closing_hour"])
    if not 360 <= opening_hour <= 600:
        raise IntegrityError("Godzina otwarcia musi byc miedzy 06:00 a 10:00.")
    if not 960 <= closing_hour <= 1200:
        raise IntegrityError("Godzina zamkniecia musi byc miedzy 16:00 a 20:00.")
    if closing_hour - opening_hour < 640:
        raise IntegrityError("Salon musi byc otwarty przez przynajmniej 8 godzin.")


def minutes_into_the_day(time: str) -> int:
    """
    Converts time inputed in format XX:XX into minutes into the day
    Minutes into the day means the minutes passed since midnight (00:00)
    03:00 equals 180 minutes into the day, 13:00 equals 13*60 = 780 etc.
    :param time: Time to be converted
    :return: Time in new format of minutes into the day
    """
    hours_minutes = time.split(":")
    return int(hours_minutes[0]) * 60 + int(hours_minutes[1])


def update_salon():
    pass
