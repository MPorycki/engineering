import datetime
import uuid

from models import Visits
from .services import get_specific_services


def create_visit(visit: dict) -> dict:
    """
    Creates a visit based on provided data
    :param visit_data: A dict with the following keys: ["customer_id", 
    "hairdresser_id", "salon_id", "visit_date"  "services"]
    :return:
    """
    visit_duration = calculate_visit_duration(visit["services"])
    if date_available(visit["visit_date"], visit["hairdresser_id"],
                      visit_duration):
        pass


def date_available(date: str, hairdresser: str, duration: int) -> bool:
    """
    Checks if the given date is available. Expected date example:
    05/04/2020 12:00
    :param date:
    :param hairdresser:
    :return:
    """
    try:
        date_converted = datetime.strptime(date, "%d/%m/%Y %H:%M")
    except ValueError as e:
        raise ValueError("The date format is wrong: " + e)


def calculate_visit_duration(services: list):
    """
    Calculates the total minutes all the services should take
    :param services: list of ids of services
    :return:
    """
    time = 0
    for service in get_specific_services(services):
        time += service.service_duration
    return time