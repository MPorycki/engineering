import datetime
import time
import uuid

from .crud_common import delete_object
from models import session_scope, Visits, VisitsServices


def create_visit(visit: dict) -> dict:
    """
    Creates a visit based on provided data
    :param visit: A dict with the following keys: ["customer_id",
    "hairdresser_id", "salon_id", "visit_date_start", "visit_date_end",
    "services"]
    :return: Dict with information about the result of the creation
    """
    try:
        date_start = datetime.datetime.strptime(visit["visit_date_start"],
                                                "%Y-%m-%d %H:%M")
        date_end = datetime.datetime.strptime(visit["visit_date_end"],
                                              "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError("The date format is wrong: " + str(e))
    if not date_available(date_start, date_end, visit["hairdresser_id"]):
        return {"success": False}
    _id = uuid.uuid4().hex
    visit_object = Visits(
        id=_id,
        customer_id=visit["customer_id"],
        hairdresser_id=visit["hairdresser_id"],
        salon_id=visit["salon_id"],
        created_at=datetime.datetime.utcnow(),
        date_start=date_start,
        date_end=date_end,
        status="CREATED"
    )
    try:
        with session_scope() as session:
            session.add(visit_object)
    except Exception as e:
        raise e
        return {"success": False}
    if add_services(_id, visit["services"]):
        return {"success": True}
    else:
        delete_object(Visits, _id)
        return {"success": False}


def date_available(date_start: datetime, date_end: datetime,
                   hairdresser_id: str) -> bool:
    """
    Checks if the given date is available. Expected date example:
    05/04/2020 12:00
    :param date_start: Start date of the visit as string
    :param date_end:
    :param hairdresser_id:
    :return: Boolean stating whether the provided date is available for booking
    """
    for visit in get_hairdresser_visits_for_day(hairdresser_id,
                                                date_start.date()):
        print("Check" + str(visit.date_start))
        if dates_collide(visit, date_start, date_end):
            return False
    return True


def dates_collide(visit: Visits, start: datetime, end: datetime) -> bool:
    """
    Compares provided start and end time of a potential new visit with the hours
    of the provided already existing visit.
    :param visit: Visit object of the already existing visit
    :param start: Start datetime of a potential new visit
    :param end: End datetime of a potential new visit
    :return: Bool stating whether the dates collide with each other
    """
    print(visit.date_start)
    print(start)
    if (visit.date_start <= start < visit.date_end) \
            or (visit.date_start < end <= visit.date_end) \
            or (start < visit.date_start and end > visit.date_end):
        return True
    else:
        return False


def add_services(visit_id: str, services: list) -> bool:
    """
    Adds all visit services to the database
    :param visit_id: Id of the visit for which the services should be added
    :param services: List of service_id of services to be added
    :return: Bool stating the success of the operation
    """
    try:
        with session_scope() as session:
            for service_id in services:
                session.add(
                    VisitsServices(service_id=service_id, visit_id=visit_id))
    except Exception as e:
        print(e)
        return False
    return True


def get_hairdresser_visits_for_day(hairdresser_id: str,
                                   date: datetime.date) -> list:
    """
    Returns list of hairdresser's visits on a provided day.
    :param hairdresser_id: ID of the hairdresser the visits should be returned
     for
    :param date: the day for which the visits should be returned
    :return: List of Visit objects
    """
    print(date)
    with session_scope() as session:
        for visit in session.query(Visits).filter(
                Visits.hairdresser_id == hairdresser_id).all():
                #.filter(str(Visits.date_start)[:10] == str(date)).all():
            yield visit


def delete_visit(visit_id: str):
    """
    Deletes a visit
    :param visit_id: Id of the visit ot be deleted
    :return:
    """
    pass
