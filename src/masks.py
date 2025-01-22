import re


def get_mask_card_number(card: str) -> str:
    """Маскирует номер банковской карты"""
    card = re.sub(r"[-.\/ ]", "", card)
    if len(card) != 16 or not card.isdigit():
        return ""
    else:
        return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    account_number = re.sub(r"[-.\/ ]", "", account_number)
    if "Счет" in account_number:
        return f"Счет **{account_number[-4:]}"
    elif len(account_number) != 16 or not account_number.isdigit():
        return ""
    else:
        return f"**{account_number[-4:]}"


if __name__ == "__main__":
    card_number_input = input("Введите карту: ")
    print(get_mask_card_number(card_number_input))
    account_number_input = input("Введите счет: ")
    print(get_mask_account(account_number_input))
