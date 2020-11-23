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


def validate_adress(adress: dict) -> bool:
    """
    Validate the data provided for the adress
    :param adress:
    :return:
    """
    city_regex = re.compile("^[A-Z].*")
    number_regex = re.compile("[0-9]")

    if not city_regex.match(adress["city"]) or number_regex.match(
            adress["city"]
    ):
        raise ValueError("Nazwa miasta zawiera niedozwolone znaki.")
    elif len(adress["city"].split(" ")) > 3:
        raise ValueError("Nazwa miasta ma za duzo slow.")

    zip_regex = re.compile("[0-9]{2}-[0-9]{3}")
    if len(adress["zip_code"]) > 6 or len(adress["zip_code"]) == 0:
        raise ValueError("Kod pocztowy posiada niedozwolona dlugosc.")
    elif not zip_regex.match(adress["zip_code"]):
        raise ValueError("Niepoprawny format kodu pocztowego.")

    street_regex = re.compile("^[A-Z].*")
    if len(adress["street"]) > 32 or len(adress["street"]) == 0:
        raise ValueError("Niedozwolona dlugosc ulicy")
    elif not street_regex.match(adress["street"]):
        raise ValueError("W nazwie ulicy znajduja sie niedozwolone znaki")

    building_no_regex = re.compile("^[0-9]{1,3}[a-z]?$")
    if len(adress["building_no"]) == 0:
        raise ValueError("Numer budynku jest wymagany")
    elif not building_no_regex.match(adress["building_no"]):
        raise ValueError("W numerze budynku występuja niedozwolone znaki")


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


def update_adress(salon_id, adress_data: dict) -> str:
    """
    Update salon adress data
    :param salon_id: id of the salon that should have its adress udpated
    :param adress_data: Updated data of the adress
    :return: Boolean stating whether the update was successful
    """
    if not validate_adress(adress_data):
        return False
    try:
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
    except IntegrityError:
        return False
    except Exception as e:
        print(str(e.__class__.__name__) + ": " + str(e))
        return False
    return True


def adress_to_string(salon_id: str) -> str:
    """
    Provider adress in format {{street}} {{building_no}}, {{city}} as string
    """
    adress = get_adress(salon_id)
    return f"{adress['street']} {adress['building_no']}, {adress['city']}"
