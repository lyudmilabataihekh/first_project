import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "input_card, expected_output",
    [
        # Различные входные форматы
        ("7000792289606361", "7000 79** **** 6361"),
        ("70 00792289606 361", "7000 79** **** 6361"),
        ("7000-7922-8960-6361", "7000 79** **** 6361"),
        ("7000.7922.8960.6361", "7000 79** **** 6361"),  # Проверка альтернативного разделителя
        # Нестандартная длина
        ("7000", ""),
        ("7000 79", ""),
        ("7000 79 22", ""),
        ("", ""),
        # Неверные форматы
        ("abc", ""),
        ("1234 5678 9012 abcd", ""),
        ("12345678901234567", ""),  # Слишком длинный номер
        ("12345678901234", ""),
    ],
)
def test_get_mask_card_number(input_card: str, expected_output: str) -> None:
    assert get_mask_card_number(input_card) == expected_output