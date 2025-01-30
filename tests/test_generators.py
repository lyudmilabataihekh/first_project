from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions_for_test() -> List[Dict[str, Any]]:
    return [
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}},
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "usd", "code": "usd"}}},
        {"operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}}},
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "", "code": ""}}},
    ]


@pytest.fixture
def no_transactions_for_test() -> List[Dict[str, Any]]:
    return []


def test_filter_by_currency(transactions_for_test: List) -> None:
    expected_usd_transactions: List[Dict[str, Any]] = [
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}},
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "usd", "code": "usd"}}},
    ]
    usd_transactions: List[Dict[str, Any]] = list(filter_by_currency(transactions_for_test, "USD"))
    assert usd_transactions == expected_usd_transactions


def test_filter_by_currency_eur(transactions_for_test: List[Dict[str, Any]]) -> None:
    expected_eur_transactions: List[Dict[str, Any]] = []
    eur_transactions: List[Dict[str, Any]] = list(filter_by_currency(transactions_for_test, "EUR"))
    assert eur_transactions == expected_eur_transactions


def test_filter_by_currency_empty_list(no_transactions_for_test: List[Dict[str, Any]]) -> None:
    expected_eur_transactions: List[Dict[str, Any]] = []
    eur_transactions: List[Dict[str, Any]] = list(filter_by_currency(no_transactions_for_test, "EUR"))
    assert eur_transactions == expected_eur_transactions


@pytest.mark.parametrize(
    "input_description, expected_description",
    [
        ([], []),
        ([{"description": "Перевод со счета на счет"}], ["Перевод со счета на счет"]),
        ([{"description": ""}], []),
    ],
)
def test_transaction_descriptions(
    input_description: List[Dict[str, Any]], expected_description: List[Dict[str, Any]]
) -> None:
    descriptions = list(transaction_descriptions(input_description))
    assert descriptions == expected_description


def test_card_number_generator() -> None:
    generator = card_number_generator(1, 3)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"

    generator = card_number_generator(12345, 123456)
    assert next(generator) == "0000 0000 0001 2345"
    assert next(generator) == "0000 0000 0001 2346"
