import csv
from typing import Any, Dict, List

import pandas as pd


def read_transactions_csv(file_path: str) -> List[Dict[str, str]]:
    """Cчитывает финансовые операции из CSV"""
    with open(file_path, encoding='utf-8') as csv_file:
        return list(csv.DictReader(csv_file))


def read_transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    """Cчитывает финансовые операции из Excel"""
    df = pd.read_excel(file_path)
    return [dict(row) for index, row in df.iterrows()]


if __name__ == "__main__":
    file_path_csv = "../data/transactions.csv"
    print(read_transactions_csv(file_path_csv))
    file_path_excel = "../data/transactions_excel.xlsx"
    print(read_transactions_excel(file_path_excel))
