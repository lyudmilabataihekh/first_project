import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Различные входные форматы
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 987654321", "Счет **4321"),
        ("Счет 1234-5678-9012-3456", "Счет **3456"),
        ("4111 1111 1111 1111", "4111 11** **** 1111"),
        ("4100 0000 0000 0000", "4100 00** **** 0000"),
        # Нестандартная длина номера
        ("123", ""),
        ("12", ""),
        ("1", ""),
        # Неверные форматы
        ("abc", ""),
        ("1234 5678 9012 abcd", ""),
    ],
)
def test_mast_account_card(input_data: str, expected_output: str) -> None:
    assert mask_account_card(input_data) == expected_output


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Различные входные форматы
        ("1999/08/09", "09.08.1999"),
        ("1999.08.09", "09.08.1999"),
        # Пустой ввод
        ("", ""),
        # Неверные форматы
        ("abc", ""),
        ("!@#$$abcd", ""),
    ],
)
def test_get_date(input_data: str, expected_output: str) -> None:
    assert get_date(input_data) == expected_output
