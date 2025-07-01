import os
from dotenv import load_dotenv
from unittest.mock import patch
from src.external_api import get_transaction_amount

load_dotenv()

api = os.getenv("API_KEY")


test_transactions = [
    {"operationAmount": {"currency": {"code": "USD"}, "amount": "100.0"}},
    {"operationAmount": {"currency": {"code": "RUB"}, "amount": "200.0"}},
]

mock_response_usd_to_rub = {"result": 7500.0}


def test_get_transaction_amount():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_usd_to_rub
        results = list(get_transaction_amount(test_transactions))
        assert results == [7500.0, 200.0], f"Expected [7500.0, 200.0], but got {results}"
        expected_api_key = api
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": expected_api_key},
            params={"amount": 100.0, "from": "USD", "to": "RUB"},
        )


if __name__ == "__main__":
    test_get_transaction_amount()
