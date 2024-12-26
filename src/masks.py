def get_mask_card_number(card: str) -> str:
    """Маскирует номер банковской карты"""
    if card.isdigit():
        return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"
    else:
        return f"{card[:-12]} {card[-12:-10]}** **** {card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    if account_number.isdigit():
        return f"**{account_number[-4:]}"
    elif "Счет" in account_number:
        return f"Счет **{account_number[-4:]}"


if __name__ == '__main__':
    card_number_input = input("Введите карту: ")
    print(get_mask_card_number(card_number_input))
    account_number_input = input("Введите счет: ")
    print(get_mask_account(account_number_input))

