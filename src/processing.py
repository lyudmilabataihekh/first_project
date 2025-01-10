from typing import List, Dict


data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]


def filter_by_state(data: List[Dict[str, str]], state: str ='EXECUTED') -> List[Dict[str, str]]:
    """Принимает список словарей, опциональное значение для ключа state
        и возвращает новый список с указанным значением"""
    filtered_items = []
    for item in data:
        if item.get('state') == state:
            filtered_items.append(item)
    return filtered_items


def sort_by_date(data: List[Dict[str, str]], sorting: bool =True) -> List[Dict[str, str]]:
    """Принимает список словарей с необязательным параметром
    и возвращает новый список, отсортированный по дате"""
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=sorting)
    return sorted_data


if __name__ == "__main__":
    # Выход функции со статусом по умолчанию 'EXECUTED'
    executed_items = filter_by_state(data)
    print(executed_items)

    # Выход функции, если вторым аргументом передано 'CANCELED'
    canceled_items = filter_by_state(data, state="CANCELED")
    print(canceled_items)

    # Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
    print(sort_by_date(data))
