from pytest import fixture

from models import Services
from Modules.services import validate_service, translate_gender, services_data_to_dict, \
    services_to_string


@fixture(scope="function")
def generate_test_service_dict():
    return {"name": "Test_service", "price": 121, "gender": "MALE", "service_duration": 120}


@fixture(scope="function")
def generate_test_services_list(generate_test_service_dict):
    return [generate_test_service_dict, generate_test_service_dict, generate_test_service_dict]


@fixture(scope="function")
def generate_test_service_object():
    return Services(
        id=1,
        name="Test",
        price=15,
        description="Description",
        created_at="2020-04-05 16:00",
        gender="MALE",
        service_duration=120
    )


def test_validate_service_does_not_allow_too_long_name(generate_test_service_dict):
    # GIVEN
    test_service = generate_test_service_dict
    test_service["name"] = "TestTestTestTestTestTestTestTestTest"

    # WHEN
    test_validation = validate_service(test_service)

    # THEN
    assert test_validation["success"] is False
    assert test_validation["error"] == "Nazwa uslugi jest za dluga"


def test_validate_service_does_not_allow_negative_price(generate_test_service_dict):
    # GIVEN
    test_service = generate_test_service_dict
    test_service["price"] = -5

    # WHEN
    test_validation = validate_service(test_service)

    # THEN
    assert test_validation["success"] is False
    assert test_validation["error"] == "Cena nie moze byc ujemna"


def test_validate_service_does_not_allow_wrong_gender(generate_test_service_dict):
    # GIVEN
    test_service = generate_test_service_dict
    test_service["gender"] = "NoneOfTheAbove"

    # WHEN
    test_validation = validate_service(test_service)

    # THEN
    assert test_validation["success"] is False
    assert test_validation["error"] == "Niepoprawna plec"


def test_validate_service_does_not_allow_negative_service_duration(generate_test_service_dict):
    # GIVEN
    test_service = generate_test_service_dict
    test_service["service_duration"] = -100

    # WHEN
    test_validation = validate_service(test_service)

    # THEN
    assert test_validation["success"] is False
    assert test_validation["error"] == "Czas trwania uslugi musi byc dodatni"


def test_translate_gender_translates_male_correctly():
    # GIVEN
    test_string1 = "male"
    test_string2 = "MALE"
    test_string3 = "Male"

    # WHEN
    test_result1 = translate_gender(test_string1)
    test_result2 = translate_gender(test_string2)
    test_result3 = translate_gender(test_string3)

    # THEN
    assert test_result1 == "M"
    assert test_result2 == "M"
    assert test_result3 == "M"


def test_translate_gender_translates_female_correctly():
    # GIVEN
    test_string1 = "female"

    # WHEN
    test_result1 = translate_gender(test_string1)

    # THEN
    assert test_result1 == "K"


def test_services_data_to_dict_has_proper_structure(generate_test_service_object):
    # GIVEN
    test_service = generate_test_service_object

    # WHEN
    test_result = services_data_to_dict(test_service)

    # THEN
    assert "id" in test_result
    assert "description" in test_result
    assert "gender" in test_result
    assert "name" in test_result
    assert "price" in test_result
    assert "service_duration" in test_result


def test_services_to_string_converts_correctly(generate_test_services_list):
    # GIVEN
    test_services_list = generate_test_services_list

    # WHEN
    test_result = services_to_string(test_services_list)

    # THEN
    assert test_result == "Test_service, Test_service, Test_service"


def test_services_total_duration_is_calculated_correctly():
    pass


def test_services_total_price_is_calculated_correctly():
    pass
