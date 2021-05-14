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
    # User picks the salon
    print(show_user(sq).first_name)
    rv = client.get("/salon/")
    print(rv.data)
    # User picks one of the available hairdressers
