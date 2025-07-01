import json
import re
from collections import Counter
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: List[Dict[str, Any]] = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


transactions = load_transactions("../data/operations.json")


def process_bank_search(transactions: List[Dict], search_str: str) -> List[Dict]:
    """Ищет транзакции по подстроке в описании."""
    if not search_str.strip():
        return []

    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]


import re
from typing import Dict, List


def process_bank_operations(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    category_counts = {}

    for category in categories:
        # Ищем точное слово или часть слова (с учётом границ слов)
        pattern = re.compile(rf"(?i)\b{re.escape(category)}\w*")
        count = 0

        for transaction in transactions:
            description = transaction.get("description", "")
            if pattern.search(description):
                count += 1

        if count > 0:
            category_counts[category] = count

    return category_counts
