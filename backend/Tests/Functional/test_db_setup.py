import datetime
import uuid

from models import Accounts, Adresses, Salons


def set_up_test_db(session):
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
    adress_id = uuid.uuid4().hex
    salon_id = uuid.uuid4().hex
    session.add(Adresses(id=adress_id, city="Warsaw", street="Marszalkowska", building_no=3,
                         salon_id=salon_id, zip_code="05-822", number_of_seats=5,
                         created_at=datetime.datetime.utcnow()))
    session.add(Salons(id=salon_id, adress_id=adress_id, opening_hour="09:00",
                       closing_hour="17:00", created_at=datetime.datetime.utcnow()))
