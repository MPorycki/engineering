import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from models import Services, session_scope


def create_service(name: str, price: int, description: str, gender: str, service_duration: int) -> dict:
    payload = dict()
    payload["success"] = False
    try:
        validate_service(name, price, gender, service_duration)
    except IntegrityError as e:
        payload["error"] = str(e)
        return payload
    _id = uuid.uuid4().hex
    new_service = Services(
        id=_id,
        name=name,
        price=price,
        created_at=datetime.datetime.now(),
        description=description,
        gender=gender,
        service_duration=service_duration,
    )
    try:
        with session_scope() as session:
            session.add(new_service)
            payload["success"] = True
            return payload
    except IntegrityError as e:
        payload["error"] = str(e)
        return payload


def validate_service(name: str, price: int, gender: str, service_duration: int):
    """
    Checks input service data and make sures it fulfills all the requirements
    :param name: Name of the service, can't be longer than 32 characters
    :param price: Price of the service, can't be lower than 0
    :param gender: Gender for which the service is designed, has to be one of: (MALE, FEMALE)
    :param service_duration: Duration of the service, has to be higher than 0
    """
    if len(name) > 32:
        raise IntegrityError("Nazwa uslugi jest za dluga")
    if price < 0:
        raise IntegrityError("Cena nie moze byc ujemna")
    if gender not in ("MALE", "FEMALE"):
        raise IntegrityError("Niepoprawna plec")
    if service_duration <= 0:
        raise IntegrityError("Czas trwania uslugi musi byc dodatni")


def update_service(service_updated_data: dict) -> bool:
    """
        Update service data
        :param service_updated_data: data of the given service to be updated
        :return: Boolean stating whether the update was successful
        """
    try:
        with session_scope() as session:
            service = (
                session.query(Services)
                    .filter(Services.id == service_updated_data["service_id"])
                    .first()
            )
            service.price = service_updated_data["price"]
            service.name = service_updated_data["name"]
            service.description = service_updated_data["description"]
            service.gender = service_updated_data["gender"]
            service.service_duration = service_updated_data["service_duration"]
            session.commit()
        return True
    except Exception as e:
        print(e)
        return False
