from sqlalchemy.exc import IntegrityError

from models import Salons


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
    new_service = Salons(
        id=,
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
            return {"success": True}
    except IntegrityError as e:
        return {"success": False, "error": str(e)}


def validate_salon(data):
    pass


def update_salon():
    pass