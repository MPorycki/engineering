from pytest import fixture
import os

from Modules.salons import get_all_salons


@fixture(scope="module")
def fetch_test_salons():
    # replaces the functionality of crud_common.fetch_all_objects
    test_salons = {"Salons": [
        {"id": "1", "adress_id": "1", "opening_hour": "09:00", "closing_hour": "17:00"},
        {"id": "2", "adress_id": "2", "opening_hour": "09:00", "closing_hour": "17:00"},
        {"id": "3", "adress_id": "3", "opening_hour": "09:00", "closing_hour": "17:00"}
    ]}
    return test_salons


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


def test_hairdresser_matches_salon_returns_correct_info_for_hairdresser(monkeypatch):
    pass


def test_salon_has_hairdresser_spot_returns_correct_info():
    pass
