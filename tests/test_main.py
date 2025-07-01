from typing import List
from unittest.mock import mock_open, patch

import pytest

from src.main import main

# Тестовые данные для main
MAIN_TEST_DATA = [
    {
        "state": "EXECUTED",
        "description": "Перевод организации",
        "date": "2023-01-01T00:00:00",
        "operationAmount": {"amount": "1000", "currency": {"name": "руб."}},
        "from": "Счет 1234567890",
        "to": "Счет 0987654321",
    }
]


@pytest.mark.parametrize(
    "user_input, expected_in_output",
    [
        (["1", "EXECUTED", "нет", "нет", "перевод"], "Перевод организации"),
        (["1", "EXECUTED", "да", "по возрастанию", "нет", "перевод"], "01.01.2023"),
    ],
)
def test_main_json(user_input: List[str], expected_in_output: str) -> None:
    with patch("builtins.input", side_effect=user_input), patch("json.load", return_value=MAIN_TEST_DATA), patch(
        "builtins.open", mock_open()
    ), patch("builtins.print") as mock_print:
        main()
        assert any(expected_in_output in str(call) for call in mock_print.call_args_list)


@pytest.mark.parametrize(
    "user_input, expected_in_output",
    [
        (["2", "EXECUTED", "нет", "нет", "перевод"], "Перевод организации"),
    ],
)
def test_main_csv(user_input: List[str], expected_in_output: str) -> None:
    with patch("builtins.input", side_effect=user_input), patch("csv.DictReader", return_value=MAIN_TEST_DATA), patch(
        "builtins.open", mock_open()
    ), patch("builtins.print") as mock_print:
        main()
        assert any(expected_in_output in str(call) for call in mock_print.call_args_list)


def test_main_input_errors() -> None:
    user_input = ["5", "1", "INVALID", "EXECUTED", "нет", "нет", "перевод"]

    with patch("builtins.input", side_effect=user_input), patch("json.load", return_value=MAIN_TEST_DATA), patch(
        "pandas.read_excel"
    ), patch("builtins.open", mock_open()), patch("builtins.print") as mock_print:
        main()
        output = "\n".join(str(call) for call in mock_print.call_args_list)
        assert "недоступен" in output.lower()


def test_main_empty_results() -> None:
    with patch("builtins.input", side_effect=["1", "PENDING", "нет", "нет", "кредит"]), patch(
        "json.load", return_value=MAIN_TEST_DATA
    ), patch("builtins.open", mock_open()), patch("builtins.print") as mock_print:
        main()

        # Получаем весь вывод
        output = "\n".join(str(call.args[0]) for call in mock_print.call_args_list if call.args)

        # Проверяем наличие сообщения о пустом результате
        assert "Всего банковских операций в выборке: 0" in output
        assert "Распечатываю итоговый список транзакций:" in output
