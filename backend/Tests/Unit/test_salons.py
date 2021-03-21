from pytest import fixture

from Modules.salons import get_all_salons, hairdresser_matches_salon


@fixture(scope="module")
def fetch_test_salons():
    # replaces the functionality of crud_common.fetch_all_objects
    test_salons = {"Salons": [
        {"id": "1", "adress_id": "1", "opening_hour": "09:00", "closing_hour": "17:00"},
        {"id": "2", "adress_id": "2", "opening_hour": "09:00", "closing_hour": "17:00"},
        {"id": "3", "adress_id": "3", "opening_hour": "09:00", "closing_hour": "17:00"}
    ]}
    return test_salons


@fixture(scope="module")
def fetch_one_salon():
    # replaces the functionality of crud_common.fetch_object
    return {"id": "561acc9298174af7ab40675bbd30dc08", "adress_id": "1", "opening_hour": "09:00",
            "closing_hour": "17:00"},


@fixture(scope="module")
def generate_test_hairdresser():
    return {"id": "1", "first_name": "John", "last_name": "Test", "email": "test@gmail.com",
            "hashed_password": "haaash", "account_type": "hairdresser",
            "salon_id": "561acc9298174af7ab40675bbd30dc08", "is_admin": 0}


@fixture(scope="module")
def generate_test_customer():
    return {"id": "2", "first_name": "Mart", "last_name": "Customer", "email": "test2@gmail.com",
            "hashed_password": "haaash", "account_type": "customer",
            "salon_id": "", "is_admin": 0}


def test_get_all_salons_returns_all_salons(fetch_test_salons, monkeypatch):
    # GIVEN
    monkeypatch.setattr("Modules.salons.fetch_all_objects", lambda x: fetch_test_salons)
    monkeypatch.setattr("Modules.salons.get_adress", lambda x: "Test_Adress")

    # WHEN
    test_result = get_all_salons()

    # THEN
    assert len(test_result["Salons"]) == 3


def test_get_all_salons_return_correct_salon_data(fetch_test_salons, monkeypatch):
    # GIVEN
    monkeypatch.setattr("Modules.salons.fetch_all_objects", lambda x: fetch_test_salons)
    monkeypatch.setattr("Modules.salons.get_adress", lambda x: "Test_Adress")

    # WHEN
    test_result = get_all_salons()
    test_salon = test_result["Salons"][0]

    # THEN
    assert test_salon["id"] == "1"
    assert test_salon["opening_hour"] == "09:00"
    assert test_salon["closing_hour"] == "17:00"
    assert test_salon["address"] == "Test_Adress"


def test_hairdresser_matches_salon_returns_correct_info_for_hairdresser(generate_test_hairdresser,
                                                                        monkeypatch):
    # GIVEN
    monkeypatch.setattr("Modules.salons.fetch_object", lambda x, y: generate_test_hairdresser)
    test_salon_id_correct = "561acc9298174af7ab40675bbd30dc08"
    test_salon_id_false = "e3cdd3de1eeb48d0ba279772810e6c06"

    # WHEN
    test_result_1 = hairdresser_matches_salon(salon_id=test_salon_id_correct, hairdresser_id="1")
    test_result_2 = hairdresser_matches_salon(salon_id=test_salon_id_false, hairdresser_id="1")

    # THEN
    assert test_result_1 is True
    assert test_result_2 is False
