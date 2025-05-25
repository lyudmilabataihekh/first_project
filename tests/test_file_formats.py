from typing import Dict, List
from unittest.mock import mock_open, patch

import pandas as pd

from src.file_formats import read_transactions_csv, read_transactions_excel


def test_read_transactions_csv() -> None:
    test_data: List[Dict[str, str]] = [{"date": "2023-01-01", "amount": "100"}]
    mock_csv = "date,amount\n2023-01-01,100\n"
    with patch("builtins.open", mock_open(read_data=mock_csv)):
        with patch("src.file_formats.csv.DictReader", return_value=test_data):
            result = read_transactions_csv("../data/transactions.csv")
            assert result == test_data


def test_read_transactions_excel() -> None:
    test_data: pd.DataFrame = pd.DataFrame([{"date": "2023-01-01", "amount": "100"}])
    with patch("src.file_formats.pd.read_excel", return_value=test_data):
        result = read_transactions_excel("../data/transactions_excel.xlsx")
        assert result == [{"date": "2023-01-01", "amount": "100"}]


if __name__ == "__main__":
    test_read_transactions_csv()
    test_read_transactions_excel()
