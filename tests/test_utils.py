import json
from unittest.mock import mock_open, patch

from src.utils import get_financial_operation


@patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1}]')
@patch('json.load')
def test_get_financial_operation(mock_load, mock_open):
    mock_load.return_value = [{"id": 1}]
    result = get_financial_operation('../data/operations.json')
    assert result == [{"id": 1}]
    mock_open.assert_called_once_with('../data/operations.json', 'r', encoding='utf-8')
    mock_load.assert_called_once()


@patch('builtins.open', new_callable=mock_open, read_data='[]')
@patch('json.load')
def test_get_financial_operation_empty(mock_load, mock_open):
    mock_load.return_value = []
    result = get_financial_operation('../data/operations.json')
    assert result == []
    mock_open.assert_called_once_with('../data/operations.json', 'r', encoding='utf-8')
    mock_load.assert_called_once()


@patch('builtins.open', new_callable=mock_open)
def test_get_financial_operation_file_not_found(mock_open):
    mock_open.side_effect = FileNotFoundError
    result = get_financial_operation('../data/operations.json')
    assert result == []


@patch('builtins.open', new_callable=mock_open, read_data='invalid json')
@patch('json.load')
def test_get_financial_operation_json_decode_error(mock_load, mock_open):
    mock_load.side_effect = json.JSONDecodeError("Expecting value", "invalid json", 0)
    result = get_financial_operation('../data/operations.json')
    assert result == []


if __name__ == "__main__":
    test_get_financial_operation()
    test_get_financial_operation_empty()
    test_get_financial_operation_file_not_found()
    test_get_financial_operation_json_decode_error()
