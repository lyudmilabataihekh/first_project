import logging
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs/masks.log',
                    filemode='w')

logger = logging.getLogger('masks')


def get_mask_card_number(card: str) -> str:
    """Маскирует номер банковской карты"""
    logger.info("Обработка номера карты: %s", card)
    card = re.sub(r"[-.\/ ]", "", card)
    if len(card) != 16 or not card.isdigit():
        logger.warning("Некорректный номер карты: %s", card)
        return ""
    else:
        return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    logger.info("Обработка банковского счета: %s", account_number)
    account_number = re.sub(r"[-.\/ ]", "", account_number)
    if "Счет" in account_number:
        return f"Счет **{account_number[-4:]}"
    elif len(account_number) != 16 or not account_number.isdigit():
        logger.warning("Некорректный номер счета: %s", account_number)
        return ""
    else:
        return f"**{account_number[-4:]}"


if __name__ == "__main__":
    card_number_input = input("Введите карту: ")
    print(get_mask_card_number(card_number_input))
    account_number_input = input("Введите счет: ")
    print(get_mask_account(account_number_input))
