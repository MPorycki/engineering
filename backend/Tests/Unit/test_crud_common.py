import datetime
import uuid

import pytest
from pytest import fixture

from Modules.crud_common import convert_to_dict, fetch_all_objects
from models import Accounts


@fixture(scope="module")
def test_db_object():
    return Accounts(
        id=uuid.uuid4().hex,
        email="marcopolo@test.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Marco",
        last_name="Polo",
        account_type="customer",
        salon_id=uuid.uuid4().hex
    )


@pytest.mark.skip(reason="no way of currently testing this")
def test_convert_to_dict_converts_correctly(test_db_object):
    # GIVEN
    # A test db object...
    # WHEN
    test_result = convert_to_dict(test_db_object)

    # THEN
    assert "email" in test_result
    assert "_sa_instance_state" not in test_result
    assert "id" in test_result


def test_fetch_all_objects_has_proper_structure(test_db_object, monkeypatch):
    # GIVEN
    mock_db_objects = [test_db_object, test_db_object]
    monkeypatch.setattr("Modules.crud_common.all_objects_from_db", lambda x: mock_db_objects)
    monkeypatch.setattr("Modules.crud_common.convert_to_dict", lambda x: x.__dict__)

    # WHEN
    test_result = fetch_all_objects(Accounts)

    # THEN
    assert "Accounts" in test_result
    assert len(test_result["Accounts"]) == 2
    assert type(test_result["Accounts"]) is list
