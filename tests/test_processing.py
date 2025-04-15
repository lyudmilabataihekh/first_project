from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def data() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_executed(data: List[Dict[str, Any]]) -> None:
    assert filter_by_state(data, state="EXECUTED") == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_canceled(data: List[Dict[str, Any]]) -> None:
    assert filter_by_state(data, state="CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_empty(data: List[Dict[str, Any]]) -> None:
    assert filter_by_state(data, state="") == []


def test_filter_by_state_done(data: List[Dict[str, Any]]) -> None:
    assert filter_by_state(data, state="DONE") == []


def test_sort_by_date(data: List[Dict[str, Any]]) -> None:
    assert sort_by_date(data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date_reverse(data: List[Dict[str, Any]]) -> None:
    assert sort_by_date(data, sorting=False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.fixture
def same_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2022-01-01T00:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2022-01-01T00:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2022-01-01T00:00:01"},
    ]


def test_sorting_by_date(same_data: List[Dict[str, Any]]) -> None:
    assert sort_by_date(same_data) == [
        {"id": 3, "state": "EXECUTED", "date": "2022-01-01T00:00:01"},
        {"id": 1, "state": "EXECUTED", "date": "2022-01-01T00:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2022-01-01T00:00:00"},
    ]


@pytest.fixture
def incorrect_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "not-a-date"},
        {"id": 2, "state": "EXECUTED", "date": "2022-01-01T00:00:00"},
    ]


def test_sorting_incorrect_data(incorrect_data: List[Dict[str, Any]]) -> None:
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(incorrect_data)
    assert str(exc_info.value) == "Некорректный формат даты"
