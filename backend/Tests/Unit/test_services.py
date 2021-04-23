from Modules.services import validate_service, translate_gender


def test_validate_service_does_not_allow_too_long_name():
    # GIVEN
    test_service = []

    # WHEN


def test_validate_service_does_not_allow_negative_price():
    pass


def test_validate_service_does_not_allow_wrong_gender():
    pass


def test_validate_service_does_not_allow_negative_service_duration():
    pass


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


def test_services_data_to_dict_has_proper_structure():
    pass


def test_services_to_string_converts_correctly():
    pass


def test_services_total_duration_is_calculated_correctly():
    pass


def test_services_total_price_is_calculated_correctly():
    pass
