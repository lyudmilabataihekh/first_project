from typing import Any, Dict, List

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

test_transactions: List[Dict[str, Any]] = [
    {"operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}},
    {"operationAmount": {"amount": "9824.07", "currency": {"name": "usd", "code": "usd"}}},
    {"operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}}},
    {"operationAmount": {"amount": "9824.07", "currency": {"name": "", "code": ""}}},
]


test_descriptions: List[Dict[str, Any]] = [
    {"description": 0},
    {"description": "Перевод со счета на счет"},
    {"description": ""},
]


def test_filter_by_currency() -> None:
    expected_usd_transactions: List[Dict[str, Any]] = [
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}},
        {"operationAmount": {"amount": "9824.07", "currency": {"name": "usd", "code": "usd"}}},
    ]
    usd_transactions: List[Dict[str, Any]] = list(filter_by_currency(test_transactions, "USD"))
    assert usd_transactions == expected_usd_transactions


def test_transaction_descriptions() -> None:
    expected_descriptions: List[Any] = [0, "Перевод со счета на счет"]
    descriptions: List[Any] = list(transaction_descriptions(test_descriptions))
    assert descriptions == expected_descriptions


def test_card_number_generator() -> None:
    generator = card_number_generator(1, 3)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"

    generator = card_number_generator(12345, 123456)
    assert next(generator) == "0000 0000 0001 2345"
    assert next(generator) == "0000 0000 0001 2346"
