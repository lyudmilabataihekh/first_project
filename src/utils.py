import json
from typing import Any, List


def get_financial_operation(file_path: str) -> List[Any]:
    """Возвращает данные о финансовых транзакциях"""
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            result = json.load(json_file)
            if not result:
                return []
            return result
    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    path_to_file = "../data/operations.json"
    operations = get_financial_operation(path_to_file)
    print(operations)
