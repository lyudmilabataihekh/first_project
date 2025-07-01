from typing import Dict, List

import pytest

from src.operations import process_bank_operations, process_bank_search

TEST_TRANSACTIONS = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    },
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Открытие вклада",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 587085106,
        "state": "EXECUTED",
        "date": "2018-03-23T10:45:06.972075",
        "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
]


@pytest.mark.parametrize(
    "search_str, expected_count",
    [
        ("перевод", 3),
        ("вклад", 1),
        ("открытие", 1),
        ("", 0),
        ("кредит", 0),
    ],
)
def test_process_bank_search(search_str: str, expected_count: int) -> None:
    result = process_bank_search(TEST_TRANSACTIONS, search_str)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(search_str.lower() in t.get("description", "").lower() for t in result)


@pytest.mark.parametrize(
    "categories, expected",
    [
        (["перевод", "вклад"], {"перевод": 3, "вклад": 1}),
        (["организац", "карт"], {"организац": 1, "карт": 1}),
        (["клиент", "открытие"], {"клиент": 1, "открытие": 1}),
        (["кредит", "депозит"], {}),
        ([], {}),
    ],
)
def test_process_bank_operations(categories: List[str], expected: Dict[str, int]) -> None:
    test_data = [
        {"description": "Перевод организации"},
        {"description": "Перевод между картами"},
        {"description": "Открытие вклада"},
        {"description": "Перевод клиенту"},
    ]
    result = process_bank_operations(test_data, categories)
    assert result == expected
