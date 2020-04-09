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
    adress_id = uuid.uuid4().hex
    new_adress = Adresses(
        id=adress_id,
        salon_id=salon_id,
        city=adress["city"],
        zip_code=adress["zip_code"],
        street=adress["street"],
        building_no=adress["building_no"],
        number_of_seats=adress["numbetr_of_seats"]
    )
    try:
        with session_scope() as session:
            session.add(new_adress)
    except IntegrityError as e:
        print(str(e.__class__.__name__) + ": " + str(e))
        return None
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
        return False
    elif len(adress["city"].split(" ")) > 3:
        return False

    zip_regex = re.compile("[0-9]{2}-[0-9]{3}")
    if len(adress["zip_code"]) > 6 or len(adress["zip_code"]) == 0:
        return False
    elif not zip_regex.match(adress["zip_code"]):
        return False

    street_regex = re.compile("^[A-Z].*")
    if len(adress["street"]) > 32 or len(adress["street"]) == 0:
        return False
    elif not street_regex.match(adress["street"]):
        return False

    building_no_regex = re.compile("^[0-9]{1,3}[a-z]?$")
    if len(adress["building_no"]) == 0:
        return False
    elif not building_no_regex.match(adress["building_no"]):
        return False

    flat_no_regex = re.compile("^[0-9]{1,3}$")
    if adress["flat_no"] is None:
        return False
    elif not flat_no_regex.match(str(adress["flat_no"])):
        return False
    return True


def get_adress(salon_id: str) -> Adresses:
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
        """
        del result["_sa_instance_state"]
        del result["id"]
        del result["id_project"]
        """
        return result


def update_adress(salon_id, adress_data: dict) -> str:
    """
    Update salon adress data
    :param salon_id: id of the salon that should have its adress udpated
    :param adress_data: Updated data of the adress
    :return: Boolean stating whether the update was successful
    """
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
