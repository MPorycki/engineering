import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from models import Services, session_scope


def create_service(data: dict) -> dict:
    try:
        validate_service(data)
    except IntegrityError as e:
        return {"success": False, "error": str(e)}
    _id = uuid.uuid4().hex
    new_service = Services(
        id=_id,
        name=data["name"],
        price=data["price"],
        created_at=datetime.datetime.utcnow(),
        description=data["description"],
        gender=data["gender"],
        service_duration=data["service_duration"],
    )
    try:
        with session_scope() as session:
            session.add(new_service)
            return {"success": True}
    except IntegrityError as e:
        return {"success": False, "error": str(e)}


def validate_service(data: dict):
    """
    Checks input service data and make sures it fulfills all the requirements
    :param data: Dict with the following keys:
    name: Name of the service, can't be longer than 32 characters
    price: Price of the service, can't be lower than 0
    gender: Gender for which the service is designed, has to be one of: (MALE, FEMALE)
    service_duration: Duration of the service, has to be higher than 0
    """
    if len(data["name"]) > 32:
        raise IntegrityError("Nazwa uslugi jest za dluga")
    if data["price"] < 0:
        raise IntegrityError("Cena nie moze byc ujemna")
    if data["gender"] not in ("MALE", "FEMALE"):
        raise IntegrityError("Niepoprawna plec")
    if data["service_duration"] <= 0:
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
