import datetime
import json

from pytest_mock_resources import create_sqlite_fixture
from pytest import fixture

import app
from models import Accounts, Sessions, Visits
from test_db_setup import set_up_test_db, add_salon_id_for_hairdressers

sq = create_sqlite_fixture(Accounts, session=True)


def show_user(session):
    return session.query(Accounts).first()


def show_session_data(session):
    # Return the session ID that our test user receives when test logging in
    session_result = session.query(Sessions).first()
    return session_result.session_id, session_result.account_id


def show_visits_data(session):
    return session.query(Visits).first()


@fixture
def client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        yield client


def test_base_connection(client):
    rv = client.get('/')
    assert rv.status == "200 OK"
    assert b'True' in rv.data


def test_register_for_a_visit(sq, client, monkeypatch):
    monkeypatch.setattr("models.Session", lambda: sq)
    set_up_test_db(sq)
    add_salon_id_for_hairdressers(sq)
    # User Jan Testowy logs in
    monkeypatch.setattr("Modules.user_management.sha256_crypt.verify", lambda x, y: True)
    client.post("/account/login", json=dict(email="jan@testowy.com", raw_password="anything"))
    # User enters the registration page. List of available salons loads
    rv = client.get("/salon/")
    salon_data = json.loads(rv.data.decode('utf8'))
    assert len(salon_data["Salons"]) == 1
    assert "city" in salon_data["Salons"][0]["address"]
    assert salon_data["Salons"][0]["address"]["city"] == "Warsaw"
    assert "street" in salon_data["Salons"][0]["address"]
    assert salon_data["Salons"][0]["address"]["street"] == "Marszalkowska"
    # User picks the salon
    picked_salon = salon_data["Salons"][0]
    # The list of available hairdressers loads
    hairdressers_request = client.get("/hairdresser/" + picked_salon["id"])
    hairdressers_data = json.loads(hairdressers_request.data.decode('utf8'))["Hairdressers"]
    assert len(hairdressers_data) == 3
    assert "first_name", "last_name" in hairdressers_data[0]
    assert hairdressers_data[0]["firstName"] == "Jan"
    assert hairdressers_data[1]["firstName"] == "Marcin"
    # User picks one of the available hairdressers
    picked_hairdresser = hairdressers_data[1]
    # List of available services is loaded
    services_request = client.get("/service/")
    services_data = json.loads(services_request.data.decode('utf8'))["Services"]
    assert len(services_data) == 2
    assert "name", "gender" in services_data[0]
    assert "service_duration" in services_data[0]
    assert services_data[1]["name"] == "Test"
    # Users selects services
    picked_services = services_data
    # Total service time is being calculated
    total_service_time = 180
    # Available hours for today are loaded
    session_id, account_id = show_session_data(sq)
    todays_date = datetime.datetime.utcnow().strftime("%d/%m/%Y")
    avail_hours_request = client.post("/visit/availability/",
                                      json=dict(date=todays_date,
                                                hairdresserId=picked_hairdresser["id"],
                                                serviceDuration=total_service_time,
                                                salonId=picked_salon["id"]),
                                      headers=dict(session_id=session_id, account_id=account_id))
    avail_hours_data = json.loads(avail_hours_request.data.decode('utf8'))["availableHours"]
    print(avail_hours_data)
    assert len(avail_hours_data) == 10
    # User picks an hour
    picked_hour = "11:00"
    # Users decides to book the visit
    create_visit_request_data = {
        "visit_date_start": todays_date + " " + picked_hour,
        "hairdresser_id": picked_hairdresser["id"],
        "service_duration": total_service_time,
        "salon_id": picked_salon["id"],
        "services": picked_services}
    create_visit_request = client.post("/visit/", json=create_visit_request_data,
                                       headers=dict(session_id=session_id, account_id=account_id))
    visit = show_visits_data(sq)
    assert visit is not None
    assert visit.date_start.strftime("%d/%m/%Y %H:%M") == todays_date + " " + picked_hour
    assert visit.status == 'CREATED'
