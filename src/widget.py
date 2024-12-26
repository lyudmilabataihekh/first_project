from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_data: str) -> str:
    """Обрабатывает информацию о счетах и картах"""
    if "Счет" in account_card_data:
        account_data = get_mask_account(account_card_data)
        return account_data
    else:
        card_data = get_mask_card_number(account_card_data)
        return card_data


if __name__ == '__main__':
    account_card_data_input = input("Введите тип и номер карты или счета: ")
    print(mask_account_card(account_card_data_input))
