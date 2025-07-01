import csv
import json
import re
from datetime import datetime
from typing import Dict, List

import pandas as pd

from src.operations import process_bank_operations, process_bank_search


def main() -> None:
    """Производит фильтрацию транзакций по статусу, дате, рублям, описанию"""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    choice: str = input().strip()
    transactions: List[Dict] = []

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        with open("../data/operations.json", "r", encoding="utf-8") as f:
            transactions = json.load(f)

    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        with open("../data/transactions.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            transactions = list(reader)
    else:
        print("Для обработки выбран XLSX-файл.")
        df = pd.read_excel("../data/transactions_excel.xlsx")
        transactions = df.to_dict(orient="records")

    # Фильтрация по статусу
    status_options: List[str] = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input: str = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        if status_input not in status_options:
            print(f"Статус операции '{status_input}' недоступен.")
            continue
        else:
            print(f"Операции отфильтрованы по статусу '{status_input}'")
            break

    pattern: re.Pattern = re.compile(status_input, re.IGNORECASE)
    filtered_transactions: List[Dict] = [t for t in transactions if "state" in t and pattern.search(str(t["state"]))]

    def get_date(t: Dict) -> datetime:
        """Сортирует транзакции по дате"""
        date_str: str = t.get("date", "")
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
        if match:
            try:
                return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError:
                return datetime.min
        return datetime.min

    filter_by_date: str = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if filter_by_date == "да":
        sort_order: str = input("По возрастанию или по убыванию?\n").strip().lower()
        reverse: bool = sort_order == "по убыванию"
        if sort_order not in ["по возрастанию", "по убыванию"]:
            print("Некорректный ввод, сортировка по дате по умолчанию (по возрастанию).")
            reverse = False
            filtered_transactions.sort(key=get_date, reverse=reverse)

    # Сортировка по рублям
    filter_by_rub: str = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if filter_by_rub == "да" and choice == "1":
        filtered_transactions = [
            t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]
    elif filter_by_rub == "да" and (choice == "2" or choice == "3"):
        filtered_transactions = [t for t in transactions if t.get("currency_code") == "RUB"]

    # Поиск по описанию
    search_description: str = input("Введите слово для поиска в описании:\n").strip()
    if search_description:
        filtered_transactions = process_bank_search(filtered_transactions, search_description)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Итоги
    categories: List[str] = [search_description]
    result: Dict[str, int] = process_bank_operations(filtered_transactions, categories)
    count: int = next(iter(result.values())) if result else 0  # Безопасное получение первого значения
    print(f"Всего банковских операций в выборке: {count}")

    pattern_date: re.Pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    print("Распечатываю итоговый список транзакций:")
    for t in filtered_transactions:
        date_str: str = str(t.get("date", ""))
        match = pattern_date.search(date_str)
        if match:
            year, month, day = match.groups()
            dt: datetime = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            formatted_date: str = dt.strftime("%d.%m.%Y")

        description: str = t.get("description", "")
        details_str: str = ""
        if "from" in t:
            account_from: str = t["from"]
            account_to: str = t["to"]
            masked_from: str = f"{account_from[:4]} {account_from[4:6]}** **** {account_from[-4:]}"
            masked_to: str = f"{account_to[:4]} {account_to[4:6]}** **** {account_to[-4:]}"
            details_str = f"{masked_from} -> {masked_to}"
        elif "to" in t:
            details_str = t["to"]
        amount_value: str = t.get("amount", "") or t.get("operationAmount", {}).get("amount", "")
        currency: str = t.get("operationAmount", {}).get("currency", {}).get("name", "")
        print(f"{formatted_date} {description}")
        if details_str:
            print(f"{details_str}")
        print(f"Сумма: {amount_value} {currency}\n")
        if not filtered_transactions:
            print("Не найдено подходящих транзакций")
            print("Всего банковских операций в выборке: 0")
            return


if __name__ == "__main__":
    main()
