import datetime
import uuid

from pytest import fixture

from models import Accounts
from Modules.user_management import account_data_to_dict, prepare_reset_link_message, token_valid


@fixture(scope="module")
def test_account_obj():
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


def test_send_reset_link_has_correct_headers():
    # GIVEN
    test_token = uuid.uuid4().hex
    test_email = "test@polo.pl"
    test_name = ' John'

    # WHEN
    test_result = prepare_reset_link_message(test_token, test_email, test_name)

    # THEN
    assert "From: Salony Fryzjerskie Marco Polo" in test_result
    assert f"To: {test_email}" in test_result


def test_token_valid_validates_correctly():
    # GIVEN
    test_token_valid = {"id": uuid.uuid4().hex, "account_id": uuid.uuid4().hex,
                        "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=5)}
    test_token_invalid = {"id": uuid.uuid4().hex, "account_id": uuid.uuid4().hex,
                          "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=14)}

    # WHEN
    test_result_true = token_valid(test_token_valid)
    test_result_false = token_valid(test_token_invalid)

    # THEN
    assert test_result_true is True
    assert test_result_false is False


def test_account_data_to_dict_has_correct_format(test_account_obj):
    # GIVEN
    test_account = test_account_obj

    # WHEN
    test_result = account_data_to_dict(test_account)

    # THEN
    assert "id" in test_result
    assert "firstName" in test_result
    assert "lastName" in test_result
    assert "email" in test_result
