import datetime

import uuid

from pytest import fixture

from models import Visits
from Modules.visits import dates_collide, calculate_end_date, get_available_hours


@fixture(scope="function")
def test_visit_obj():
    return Visits(
        id=uuid.uuid4().hex,
        customer_id=uuid.uuid4().hex,
        hairdresser_id=uuid.uuid4().hex,
        salon_id=uuid.uuid4().hex,
        created_at=datetime.datetime.utcnow(),
        date_start=datetime.datetime.strptime("05/04/2021 14:00",
                                              "%d/%m/%Y %H:%M"),
        date_end=datetime.datetime.strptime("05/04/2021 15:00",
                                            "%d/%m/%Y %H:%M"),
        status="CREATED"
    )


def test_dates_collide_finds_collision_when_visit_starts_earlier(test_visit_obj):
    # GIVEN
    test_visit = test_visit_obj  # 05/04/21 14:00 to 15:00
    test_start_earlier = datetime.datetime.strptime("05/04/2021 12:00", "%d/%m/%Y %H:%M")
    test_end_earlier = datetime.datetime.strptime("05/04/2021 13:30", "%d/%m/%Y %H:%M")
    test_end_same_as_start = datetime.datetime.strptime("05/04/2021 14:00", "%d/%m/%Y %H:%M")
    test_end_same_as_end = datetime.datetime.strptime("05/04/2021 15:00", "%d/%m/%Y %H:%M")
    test_end_later = datetime.datetime.strptime("05/04/2021 16:00", "%d/%m/%Y %H:%M")

    # WHEN
    test_result_1 = dates_collide(test_visit, test_start_earlier, test_end_earlier)
    test_result_2 = dates_collide(test_visit, test_start_earlier, test_end_same_as_start)
    test_result_3 = dates_collide(test_visit, test_start_earlier, test_end_same_as_end)
    test_result_4 = dates_collide(test_visit, test_start_earlier, test_end_later)

    # THEN
    assert test_result_1 is False
    assert test_result_2 is False
    assert test_result_3 is True
    assert test_result_4 is True


def test_dates_collide_finds_collision_when_visit_starts_the_same_time(test_visit_obj):
    # GIVEN
    test_visit = test_visit_obj  # 05/04/21 14:00 to 15:00
    test_start_same = datetime.datetime.strptime("05/04/2021 14:00", "%d/%m/%Y %H:%M")
    test_end_same_as_end = datetime.datetime.strptime("05/04/2021 15:00", "%d/%m/%Y %H:%M")
    test_end_later = datetime.datetime.strptime("05/04/2021 16:00", "%d/%m/%Y %H:%M")

    # WHEN
    test_result_1 = dates_collide(test_visit, test_start_same, test_end_same_as_end)
    test_result_2 = dates_collide(test_visit, test_start_same, test_end_later)

    # THEN
    assert test_result_1 is True
    assert test_result_2 is True


def test_dates_collide_finds_collision_when_visit_starts_same_as_end(test_visit_obj):
    # GIVEN
    test_visit = test_visit_obj  # 05/04/21 14:00 to 15:00
    test_start_same_as_end = datetime.datetime.strptime("05/04/2021 15:00", "%d/%m/%Y %H:%M")
    test_end_later = datetime.datetime.strptime("05/04/2021 16:00", "%d/%m/%Y %H:%M")

    # WHEN
    test_result_1 = dates_collide(test_visit, test_start_same_as_end, test_end_later)

    # THEN
    assert test_result_1 is False


def test_dates_collide_finds_collision_when_visit_starts_later(test_visit_obj):
    # GIVEN
    test_visit = test_visit_obj  # 05/04/21 14:00 to 15:00
    test_start_same_later = datetime.datetime.strptime("05/04/2021 16:00", "%d/%m/%Y %H:%M")
    test_end_later = datetime.datetime.strptime("05/04/2021 17:00", "%d/%m/%Y %H:%M")

    # WHEN
    test_result_1 = dates_collide(test_visit, test_start_same_later, test_end_later)

    # THEN
    assert test_result_1 is False


def test_calulate_end_date_returns_correct_date():
    # GIVEN
    test_start_date = datetime.datetime.strptime("05/04/2021 14:00", "%d/%m/%Y %H:%M")
    test_duration = 120

    # WHEN
    test_result = calculate_end_date(test_start_date, test_duration)

    # THEN
    assert test_result == test_start_date + datetime.timedelta(hours=2)
