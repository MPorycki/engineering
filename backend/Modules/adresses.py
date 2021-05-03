import datetime
import re
import uuid

from sqlalchemy.exc import IntegrityError

from models import Adresses, session_scope


# CREATE


def create_adress(adress: dict, salon_id: str) -> str:
    """
    Create an adress for a salon
    :param adress: Data for the adress
    :param salon_id: ID of the salon that this adress is created for
    :return: UUID of the created adress object
    """
    try:
        validate_adress(adress)
    except ValueError as e:
        raise e
    adress_id = uuid.uuid4().hex
    new_adress = Adresses(
        id=adress_id,
        salon_id=salon_id,
        city=adress["city"],
        zip_code=adress["zip_code"],
        street=adress["street"],
        building_no=adress["building_no"],
        number_of_seats=adress["number_of_seats"],
        created_at=datetime.datetime.utcnow()
    )
    try:
        with session_scope() as session:
            session.add(new_adress)
    except IntegrityError as e:
        raise e
    return adress_id


def validate_adress(adress: dict):
    """
    Validate the data provided for the adress
    :param adress:
    :return:
    """
    if not validate_city(adress["city"])["is_validated"]:
        raise ValueError(validate_city(adress["city"])["error"])

    elif not validate_zip(["zip_code"])["is_validated"]:
        raise ValueError(validate_zip(["zip_code"])["error"])

    elif not validate_street(adress["street"])["is_validated"]:
        raise ValueError(validate_street(adress["street"])["error"])

    elif not validate_building_no(adress["building_no"])["is_validated"]:
        raise ValueError(validate_building_no(adress["building_no"])["error"])


def validate_city(city: str) -> bool:
    result = {"is_validated": False}
    city_regex = re.compile("^[A-Z].*")
    number_regex = re.compile("[0-9]")
    if not city_regex.match(city) or number_regex.match(
            city):
        result["error"] = "Nazwa miasta zawiera niedozwolone znaki."
    elif len(city.split(" ")) > 3:
        result["error"] = "Nazwa miasta ma za duzo slow."
    else:
        result["is_validated"] = True
    return result


def validate_zip(zip: str) -> bool:
    result = {"is_validated": False}
    zip_regex = re.compile("[0-9]{2}-[0-9]{3}")
    if not zip_regex.match(zip):
        result["error"] = "Niepoprawny format kodu pocztowego."
    else:
        result["is_validated"] = True
    return result


def validate_street(street: str) -> bool:
    result = {"is_validated": False}
    street_regex = re.compile("^[A-Z].*")
    if len(street) == 0:
        result["error"] = "Nazwa ulicy jest wymagana"
    if len(street) > 32:
        result["error"] = "Niedozwolona dlugosc ulicy."
    elif not street_regex.match(street):
        result["error"] = "W nazwie ulicy znajduja sie niedozwolone znaki."
    else:
        result["is_validated"] = True
    return result


def validate_building_no(building_no: str) -> bool:
    result = {"is_validated": False}
    building_no_regex = re.compile("^[0-9]{1,3}[a-z]?$")
    if len(building_no) == 0:
        result["error"] = "Numer budynku jest wymagany."
    elif not building_no_regex.match(building_no):
        result["error"] = "W numerze budynku występuja niedozwolone znaki."
    else:
        result["is_validated"] = True
    return result


def get_adress(salon_id: str) -> dict:
    """
    Get adress object based on salon_id
    :param salon_id: id of the salon the adress should be returned for
    :return:
    """
    with session_scope() as session:
        result = (
            session.query(Adresses)
                .filter(Adresses.salon_id == salon_id)
                .first()
        )
        result = result.__dict__

        del result["_sa_instance_state"]
        return result


def update_adress(salon_id, adress_data: dict) -> bool:
    """
    Update salon adress data. Exceptions are handled in update_salon function,
    hence there were removed from this one
    :param salon_id: id of the salon that should have its adress udpated
    :param adress_data: Updated data of the adress
    :return: Boolean stating whether the update was successful
    """
    validate_adress(adress_data)
    with session_scope() as session:
        adress = (
            session.query(Adresses)
                .filter(Adresses.salon_id == salon_id)
                .first()
        )
        adress.city = adress_data["city"]
        adress.zip_code = adress_data["zip_code"]
        adress.street = adress_data["street"]
        adress.building_no = adress_data["building_no"]
        adress.number_of_seats = adress_data["number_of_seats"]


def adress_to_string(salon_id: str) -> str:
    """
    Provides adress in format {{street}} {{building_no}}, {{city}} as string
    """
    adress = get_adress(salon_id)
    return f"{adress['street']} {adress['building_no']}, {adress['city']}"
