import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from models import Services, VisitsServices, session_scope


def create_service(data: dict) -> dict:
    validation = validate_service(data)
    if not validation["success"]:
        return validation
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
    result = {"success": False}
    if len(data["name"]) > 32:
        result["error"] = "Nazwa uslugi jest za dluga"
    elif data["price"] < 0:
        result["error"] = "Cena nie moze byc ujemna"
    elif data["gender"] not in ("MALE", "FEMALE"):
        result["error"] = "Niepoprawna plec"
    elif data["service_duration"] <= 0:
        raise IntegrityError("Czas trwania uslugi musi byc dodatni")
        result["error"] = "Czas trwania uslugi musi byc dodatni"
    else:
        result["success"] = True
    return result


def update_service(service_updated_data: dict) -> bool:
    """
        Update service data
        :param service_updated_data: data of the given service to be updated
        :return: Boolean stating whether the update was successful
        """
    if not validate_service(service_updated_data)["success"]:
        return False
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


def translate_gender(gender: str) -> str:
    """
    Translate gender from MALE to M and FEMALE to K, to represent it in polish
    :param gender: gender to be translated
    :return: Letter corresponding to either male or female
    """
    if gender.lower() == "male":
        return "M"
    else:
        return "K"


def services_data_to_dict(service: Services) -> dict:
    """
    Converts relevant service information to dict
    :param service: Service that needs to be converted
    :return: Dict with servcie data
    """
    return {"id": service.id,
            "description": service.description,
            "gender": translate_gender(service.gender),
            "name": service.name,
            "price": service.price,
            "service_duration": service.service_duration}


def get_all_services() -> dict:
    """
    Returns relevant data for all services
    :return: Dict with services data
    """
    result = []
    with session_scope() as session:
        services = session.query(Services.id, Services.description, Services.gender, Services.name,
                                 Services.price, Services.service_duration).order_by(
            Services.gender).order_by(Services.name).all()
        for service in services:
            result.append(services_data_to_dict(service))
        return {"Services": result}


def get_visit_services(_id: str) -> list:
    """
    Return the list of service objects based on a list of their ids
    :param _id: visit id for which the services are to be returned
    :return:
    """
    with session_scope() as session:
        visits_services = [x[0] for x in session.query(VisitsServices.service_id).filter(
            VisitsServices.visit_id == _id).all()]  # Done to unpack the id from a tuple it comes in
        result = [services_data_to_dict(service) for service in
                  session.query(Services.id, Services.description, Services.gender, Services.name,
                                Services.price, Services.service_duration)
                      .filter(Services.id.in_(visits_services)).all()]
        return result


def services_to_string(services: list) -> str:
    result_string = ""
    for service in services:
        result_string += service["name"] + ", "
    return result_string[:-2]


def services_total_duration(services: list) -> str:
    duration = 0
    for service in services:
        duration += service["service_duration"]
    return str(duration) + " min"


def services_total_price(services: list) -> str:
    price = 0
    for service in services:
        price += service["price"]
    return str(price) + " zł"
