import json
import logging
from typing import Any, List

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs/utils.log',
                    filemode='w')

logger = logging.getLogger('utils')


def get_financial_operation(file_path: str) -> List[Any]:
    """Возвращает данные о финансовых транзакциях"""
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            result = json.load(json_file)
            logger.info("Загрузка данных в файл: %s", file_path)
            if not result:
                logger.warning("Загрузка данных не удалась")
                return []
            return result
    except json.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return []
    except FileNotFoundError as ex:
        logging.error(f"Произошла ошибка: {ex}")
        return []


if __name__ == "__main__":
    path_to_file = "../data/operations.json"
    operations = get_financial_operation(path_to_file)
    print(operations)
