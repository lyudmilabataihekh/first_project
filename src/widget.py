import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_data: str) -> str:
    """Обрабатывает информацию о счетах и картах"""
    if "Счет" in account_card_data:
        account_data = get_mask_account(account_card_data)
        return account_data
    else:
        card_data = get_mask_card_number(account_card_data)
        return card_data


def get_date(date: str) -> str:
    """Меняет формат даты"""
    formated_date = re.sub(r"[/.-]", "", date)

    year = formated_date[:4]
    month = formated_date[4:6]
    day = formated_date[6:8]

    if len(formated_date) != 8 or not formated_date.isdigit():
        return ""
    else:
        modified_format = f"{day}.{month}.{year}"
        return modified_format


if __name__ == "__main__":
    account_card_data_input = input("Введите тип и номер карты или счета: ")
    print(mask_account_card(account_card_data_input))
    date_input = input("Введите дату: ")
    print(get_date(date_input))
