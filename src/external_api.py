import os
from typing import Any, Dict, Generator, List

import requests
from dotenv import load_dotenv

from src.utils import get_financial_operation

load_dotenv()

api = os.getenv("API_KEY")
print(f"API_KEY: {api}")


def get_transaction_amount(transactions: List[Dict[str, Any]]) -> Generator[float, None, None]:
    """Конвертирует и возвращает сумму транзакции в рублях."""
    for transaction in transactions:
        if "operationAmount" in transaction:
            currency = transaction["operationAmount"]["currency"]["code"]
            amount = float(transaction["operationAmount"]["amount"])
            if currency == "RUB":
                yield amount
            else:
                url = "https://api.apilayer.com/exchangerates_data/convert"
                params = {"amount": amount, "from": currency, "to": "RUB"}
                headers = {"apikey": api}
                print(f"Requesting URL: {url} with params: {params}")
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    yield response.json()["result"]
                else:
                    print(f"Ошибка API: {response.status_code}, {response.text}")
                    return


if __name__ == "__main__":
    path_to_file = "../data/operations.json"
    operations = get_financial_operation(path_to_file)
    print(operations)
    transactions_ = list(get_transaction_amount(operations))
    for result in transactions_:
        print(result)
