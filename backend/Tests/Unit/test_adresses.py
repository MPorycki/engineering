from Modules.adresses import validate_city, validate_zip, validate_street, validate_building_no, \
    adress_to_string


def test_validate_city_does_not_allow_bad_characters():
    # GIVEN
    test_city_correct = "Szczecin"
    test_city_incorrect_1 = "CyberWawa2077"
    test_city_incorrect_2 = "oDRWOTNIE"

    # WHEN
    test_result_1 = validate_city(test_city_correct)
    test_result_2 = validate_city(test_city_incorrect_1)
    test_result_3 = validate_city(test_city_incorrect_2)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Nazwa miasta zawiera niedozwolone znaki."
    assert test_result_3["is_validated"] is False
    assert test_result_3["error"] == "Nazwa miasta zawiera niedozwolone znaki."


def test_validate_city_does_not_allow_too_many_words():
    # GIVEN
    test_city_correct = "Kedzierzyn Kozle Dolne"
    test_city_incorrect = "Lidzbark Warminski Mazurski Podlaski"

    # WHEN
    test_result_1 = validate_city(test_city_correct)
    test_result_2 = validate_city(test_city_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Nazwa miasta ma za duzo slow."


def test_validate_zip_does_not_allow_wrong_format():
    # GIVEN
    test_zip_correct = "05-822"
    test_zip_incorrect = "0-123"

    # WHEN
    test_result_1 = validate_zip(test_zip_correct)
    test_result_2 = validate_zip(test_zip_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Niepoprawny format kodu pocztowego."


def test_validate_street_does_not_allow_empty_street_name():
    # GIVEN
    test_street_correct = "Gdansk"
    test_street_incorrect = ""

    # WHEN
    test_result_1 = validate_street(test_street_correct)
    test_result_2 = validate_street(test_street_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Nazwa ulicy jest wymagana."


def test_validate_street_does_not_allow_too_long_street_name():
    # GIVEN
    test_street_correct = "Warszawa"
    test_street_incorrect = "WarszawaWarszawaWarszawaWarszawaWarszawa"

    # WHEN
    test_result_1 = validate_street(test_street_correct)
    test_result_2 = validate_street(test_street_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Niedozwolona dlugosc ulicy."


def test_validate_street_does_not_allow_bad_characters():
    # GIVEN
    test_street_correct = "Sobieskiego"
    test_street_incorrect = "kRAKowska"

    # WHEN
    test_result_1 = validate_street(test_street_correct)
    test_result_2 = validate_street(test_street_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Nazwa ulicy powinna zaczynac sie z duzej litery."


def test_validate_building_no_does_not_allow_empty_number():
    # GIVEN
    test_building_no_correct = "12"
    test_building_no_incorrect = ""

    # WHEN
    test_result_1 = validate_building_no(test_building_no_correct)
    test_result_2 = validate_building_no(test_building_no_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "Numer budynku jest wymagany."


def test_validate_building_no_does_not_allow_wrong_format():
    # GIVEN
    test_building_no_correct = "12"
    test_building_no_incorrect = "123abc"

    # WHEN
    test_result_1 = validate_building_no(test_building_no_correct)
    test_result_2 = validate_building_no(test_building_no_incorrect)

    # THEN
    assert test_result_1["is_validated"] is True
    assert test_result_2["is_validated"] is False
    assert test_result_2["error"] == "W numerze budynku występuja niedozwolone znaki."


def test_adress_to_string_has_correct_format(monkeypatch):
    # GIVEN
    monkeypatch.setattr("Modules.adresses.get_adress",
                        lambda x: {"street": "Test", "building_no": "11",
                                   "city": "TestCity"})
    test_id = "123"

    # WHEN
    test_result = adress_to_string(test_id)

    # THEN
    assert test_result == "Test 11, TestCity"
