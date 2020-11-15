import copy
import datetime
import uuid

from .crud_common import delete_object, fetch_object
from models import session_scope, Visits, VisitsServices, Salons, Accounts
from Modules.user_management import is_customer
from Modules.adresses import adress_to_string
from Modules.services import services_to_string, get_visit_services, services_total_duration, \
    services_total_price


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
                                                "%d/%m/%Y %H:%M")
        date_end = calculate_end_date(date_start, visit[
            "service_duration"])  # TODO calculate end date based on duration
    except ValueError as e:
        raise ValueError("The date format is wrong: " + str(e))
    date_check = date_available(date_start, date_end, visit["hairdresser_id"],
                                visit["customer_id"])
    if not date_check["success"]:
        return date_check
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
                   hairdresser_id: str, customer_id: str) -> dict:
    """
    Checks if the given date is available. Expected date example:
    05/04/2020 12:00
    :param date_start: Start date of the visit as string
    :param date_end:
    :param hairdresser_id:
    :param customer_id:
    :return: Boolean stating whether the provided date is available for booking
    """
    for visit in get_hairdresser_visits_for_day(hairdresser_id,
                                                date_start.date()):
        if dates_collide(visit, date_start, date_end):
            return {"success": False, "hairdresser_taken": True,
                    "customer_taken": False}

    for visit in get_customer_visits_for_day(customer_id, date_start.date()):
        if dates_collide(visit, date_start, date_end):
            return {"success": False, "hairdresser_taken": False,
                    "customer_taken": True}
    return {"success": True, "hairdresser_taken": False,
            "customer_taken": False}


def dates_collide(visit: Visits, start: datetime, end: datetime) -> bool:
    """
    Compares provided start and end time of a potential new visit with the hours
    of the provided already existing visit.
    :param visit: Visit object of the already existing visit
    :param start: Start datetime of a potential new visit
    :param end: End datetime of a potential new visit
    :return: Bool stating whether the dates collide with each other
    """
    if (visit.date_start <= start < visit.date_end) \
            or (visit.date_start < end <= visit.date_end) \
            or (start < visit.date_start and end > visit.date_end):
        return True
    else:
        return False


def calculate_end_date(start_date: datetime, duration: int) -> datetime:
    """
    Calculates the end date based on the provided start date
    :param start_date: beginning of the visit
    :param duration: duration to be added to start time
    :return: datetime with added duration
    """
    return start_date + datetime.timedelta(minutes=duration)


def get_available_hours(data: dict) -> dict:
    """
    Provide fronted dates that the user can use to register his or her visit.
    :param data: Dict with the following schema {"date": date selected by user,
    "hairdresserId": hairdresser whose availability needs to be checked,
    "customerId" : customer whose availability needs to be checked,
    "serviceDuration: amount of time neeeded for the visit based on services'
     length,
     "salonId": salon where the service is supposed to take place}
    :return: Start dates that the user can pick
    """
    available_hours = list()
    salon = fetch_object(Salons, data["salonId"])
    try:
        date_start = datetime.datetime.strptime(
            # TODO handle case when the visit is for today
            f"{data['date']} {salon['opening_hour']}", "%d/%m/%Y %H:%M")
        date_end = calculate_end_date(date_start, data["serviceDuration"])
    except ValueError as e:
        raise ValueError("The date format is wrong: " + str(e))
    while date_end < datetime.datetime.strptime(
            f"{data['date']} {salon['closing_hour']}", "%d/%m/%Y %H:%M"):
        if date_available(date_start, date_end,
                          data["hairdresserId"], data["customerId"]):
            available_hours.append(
                datetime.datetime.strftime(date_start, "%H:%M"))
        date_start = date_start + datetime.timedelta(minutes=30)
        date_end = date_end + datetime.timedelta(minutes=30)
    return {"availableHours": available_hours}


def add_services(visit_id: str, services: list) -> bool:
    """
    Adds all visit services to the database
    :param visit_id: Id of the visit for which the services should be added
    :param services: List of service_id of services to be added
    :return: Bool stating the success of the operation
    """
    try:
        with session_scope() as session:
            for service in services:
                session.add(
                    VisitsServices(service_id=service["id"], visit_id=visit_id))
    except Exception as e:
        print("Add services failed" + e)
        return False
    return True


def update_services(visit_id: str, services: list) -> bool:
    """
    Adds and or removes services for a given visit based on a provided list
    of services
    :param visit_id:
    :param services:
    :return:
    """
    try:
        with session_scope() as session:
            old_services = session.query(VisitsServices.service_id).filter(
                VisitsServices.visit_id == visit_id).all()
            old_services = [x[0] for x in old_services]
            for _id in old_services:
                if _id not in services:
                    deletion = session.query(VisitsServices).filter(
                        VisitsServices.visit_id == visit_id).filter(
                        VisitsServices.service_id == _id)
                    deletion.delete()
                    session.commit()
            for _id in services:
                if _id not in old_services:
                    session.add(
                        VisitsServices(service_id=_id, visit_id=visit_id))
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
    print("Hairdresser check" + str(date))  # TODO remove?
    with session_scope() as session:
        for visit in session.query(Visits).filter(
                Visits.hairdresser_id == hairdresser_id) \
                .filter(Visits.date_start.like("%" + str(date) + "%")).all():
            yield visit


def get_customer_visits_for_day(customer_id: str,
                                date: datetime.date) -> list:
    with session_scope() as session:
        for visit in session.query(Visits).filter(
                Visits.customer_id == customer_id).all():
            # .filter(str(Visits.date_start)[:10] == str(date)).all(): # TODO fix
            yield visit


def update_visit(visit_data: dict):
    """
    Updates a visit based on provided data.
    :param visit_data: Dict with the updated data of the visit
    :return:
    """
    try:
        date_start = datetime.datetime.strptime(visit_data["visit_date_start"],
                                                "%d/%m/%Y %H:%M")
        date_end = datetime.datetime.strptime(visit_data["visit_date_end"],
                                              "%d/%m/%Y %H:%M")
    except ValueError as e:
        raise ValueError("The date format is wrong: " + str(e))
    if not date_available(date_start, date_end, visit_data["hairdresser_id"],
                          visit_data["id"]):
        return {"success": False}
    try:
        if update_services(visit_data["id"], visit_data["services"]):
            with session_scope() as session:
                visit = (
                    session.query(Visits)
                        .filter(Visits.id == visit_data["id"])
                        .first()
                )
                visit.date_start = date_start
                visit.date_end = date_end
            return {"success": True}
        return {"success": False}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_visit(visit_id):
    if delete_visit_services(visit_id):
        with session_scope() as session:
            deletion = session.query(Visits).filter(
                Visits.id == visit_id).first()
            session.delete(deletion)
            session.commit()
            return True
    else:
        False


def delete_visit_services(visit_id: str) -> bool:
    """
    Deletes all services associated with the given visit
    :param visit_id:
    :return:
    """
    with session_scope() as session:
        services = session.query(VisitsServices).filter(
            VisitsServices.visit_id == visit_id).all()
        for service in services:
            session.delete(service)
        session.commit()
        return True


def get_account_visits(account_id: str) -> dict:
    """
    Provides date, address/full name of customer, and id of the visits of the given account id
    """
    if is_customer(account_id):
        return get_customer_visits(account_id)
    else:
        return get_hairdresser_visits(account_id)


def get_customer_visits(account_id):
    result = {"visits": []}
    with session_scope() as session:
        visits = session.query(Visits).filter(
            Visits.customer_id == account_id).order_by(
            Visits.date_start.desc()).all()
        for visit in visits:
            result["visits"].append(
                {"visit_date": visit.date_start.strftime("%d.%m.%y, %H:%M"),
                 "visit_data": visit.salon_id,
                 "visit_id": visit.id,
                 "visit_status": visit.status})
    for item in result["visits"]:
        item["visit_data"] = adress_to_string(item["visit_data"])
    return result


def get_hairdresser_visits(account_id):
    result = {"visits": []}
    with session_scope() as session:
        visits = session.query(Visits).filter(
            Visits.hairdresser_id == account_id).order_by(
            Visits.date_start.desc()).all() 
        for visit in visits:
            result["visits"].append(
                {"visit_date": visit.date_start.strftime("%d.%m.%y, %H:%M"),
                 "visit_data": visit.customer_id,
                 "visit_id": visit.id,
                 "visit_status": visit.status})
        return result


def get_visit_details(visit_id):
    """
    Return required visit data for FE to render
    :param visit_id:
    :return:
    """
    details_list = []
    visit_raw = fetch_object(Visits, visit_id)
    details_list.append({"field_name": "Data wizyty",
                         "field_value": visit_raw["date_start"].strftime("%d.%m.%y, %H:%M")})
    details_list.append({"field_name": "Salon",
                         "field_value": adress_to_string(visit_raw["salon_id"])})
    services = get_visit_services(visit_raw["id"])
    details_list.append({"field_name": "Usługi",
                         "field_value": services_to_string(services)})
    details_list.append({"field_name": "Czas trwania",
                         "field_value": services_total_duration(services)})
    details_list.append({"field_name": "Cena",
                         "field_value": services_total_price(services)})
    return {"details": details_list}


def get_visit_details_for_edit(visit_id: str) -> dict:
    """
    Returns visit data needed to render the edit view.
    """
    details_list = {}
    visit = fetch_object(Visits, visit_id)
    details_list["salon"] = fetch_object(Salons, visit["salon_id"])
    details_list["hairdresser"] = fetch_object(Accounts, visit["hairdresser_id"]) #todo create method, too much data passed now

    print (details_list)
    return {"details_for_edit": details_list}
