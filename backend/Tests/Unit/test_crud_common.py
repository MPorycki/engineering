import datetime
import uuid

from pytest import fixture

from Modules.crud_common import convert_to_dict
from models import Accounts


@fixture(scope="module")
def test_db_object():
    obj = Accounts(
        id=uuid.uuid4().hex,
        email="marcopolo@test.com",
        hashed_password="anything",
        created_at=datetime.datetime(2020, 5, 17),
        first_name="Marco",
        last_name="Polo",
        account_type="customer",
        salon_id=uuid.uuid4().hex
    )
    return test_db_object


def test_convert_to_dict_converts_correctly(test_db_object):
    # GIVEN
    # A test db object...
    # WHEN
    test_result = convert_to_dict(test_db_object)

    # THEN
    assert "email" in test_result
    assert "_sa_instance_state" not in test_result
    assert "id" in test_result


def test_get_object_returns_correct_object():
    pass


def test_fetch_object_returns_the_correct_object():
    pass


def test_fetch_object_returns_only_one_object():
    pass


def all_objects_from_db_returns_all_objects():
    pass


def test_fetch_all_objects_has_proper_structure():
    pass


def test_fetch_all_objects_fetches_all_objects():
    pass


def test_delete_objects_deletes_correct_object():
    pass