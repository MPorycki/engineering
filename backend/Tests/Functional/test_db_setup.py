import datetime
import uuid

from models import Accounts, Adresses, Salons


def set_up_test_db(session):
    add_salons(session)
    add_customers(session)
    add_hairdressers(session)
    add_services(session)



def add_customers(session):
    session.add(Accounts(
        id=uuid.uuid4().hex,
        email="marcopolo@test.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Marco",
        last_name="Polo",
        account_type="customer",
        salon_id=None
    ))


def add_hairdressers(session):
    session.add(Accounts(
        id=uuid.uuid4().hex,
        email="jan@testowy.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Jan",
        last_name="Testowy",
        account_type="hairdresser",
        salon_id="219556b04e104ba2b19486cb7fda677a"
    ))
    session.add(Accounts(
        id=uuid.uuid4().hex,
        email="marcin@gmail.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Marcin",
        last_name="Testowin",
        account_type="hairdresser",
        salon_id="219556b04e104ba2b19486cb7fda677a"
    ))
    session.add(Accounts(
        id=uuid.uuid4().hex,
        email="krzys.nowak@test.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Krzysztof",
        last_name="Nowak",
        account_type="hairdresser",
        salon_id="219556b04e104ba2b19486cb7fda677a"
    ))


def add_salons(session):
    adress_id = "c988c9eb72484455a07ef15351e2030d"
    salon_id = "219556b04e104ba2b19486cb7fda677a"
    session.add(Adresses(id=adress_id, city="Warsaw", street="Marszalkowska", building_no=3,
                         salon_id=salon_id, zip_code="05-822", number_of_seats=5,
                         created_at=datetime.datetime.utcnow()))
    session.add(Salons(id=salon_id, adress_id=adress_id, opening_hour="09:00",
                       closing_hour="17:00", created_at=datetime.datetime.utcnow()))


def add_services(session):
    pass
