import json

from pytest_mock_resources import create_sqlite_fixture
from pytest import fixture

import app
from models import Accounts
from test_db_setup import set_up_test_db

sq = create_sqlite_fixture(Accounts, session=True)


def show_user(session):
    return session.query(Accounts).first()


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
    # User enters the registration page. List of available salons loads
    rv = client.get("/salon/")
    salon_data = json.loads(rv.data.decode('utf8'))
    print(rv.data.decode('utf8'))
    assert len(salon_data["Salons"]) == 1
    assert "city" in salon_data["Salons"][0]["address"]
    assert salon_data["Salons"][0]["address"]["city"] == "Warsaw"
    assert "street" in salon_data["Salons"][0]["address"]
    assert salon_data["Salons"][0]["address"]["street"] == "Marszalkowska"
    # User picks the salon
    picked_salon = salon_data["Salons"][0]
    # The list of available hairdressers loads
    hairdressers_request = client.get("/hairdresser/" + picked_salon["id"])
    print(hairdressers_request.data)
    hairdressers_data = json.loads(hairdressers_request.data.decode('utf8'))["Hairdressers"]
    assert len(hairdressers_data) == 3
    assert "first_name", "last_name" in hairdressers_data[0]
    assert hairdressers_data[0]["firstName"] == "Jan"
    assert hairdressers_data[1]["firstName"] == "Marcin"
    # User picks one of the available hairdressers
    picked_hairdresser = hairdressers_data[1]
    # List of available services is loaded
    services_request = client.get("/service/")
    print(services_request.data)
    services_data = json.loads(services_request.data.decode('utf8'))["Services"]