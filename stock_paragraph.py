from num2string import num2text
import re
from utils import *


MSG_STOCK_AMOUNT_ASK = "Введите колчиество покупаемых акций.\nПример: 123445"
MSG_STOCK_AMOUNT_ERROR = "Данные введены неправильно, повторите ввод."
REGEX_STOCK_AMOUNT = re.compile(r"^\d+$")

MSG_STOCK_TYPE = "Какого типа акции покупаем?"


class AOstocks:
    def __init__(self, AOtype, registrator, reg_codes):
        self.AOtype = AOtype
        self.registrator = registrator
        self.AOreg_codes = reg_codes



class StockParagraph:
    def __init__(self):
        self.stock_amount = get_input(REGEX_STOCK_AMOUNT, MSG_STOCK_AMOUNT_ASK, MSG_STOCK_AMOUNT_ERROR)
        self.stock_amount_literally = num2text(self.stock_amount)
        print("Тип самих акций:\n1: обыкновенные\n2: привилегированные")
        print("Также можно так:\nпустая строка : обыкновенные\nстрока с чем-то : привилегированные")
        stock_type = input()
        if stock_type == '1' or stock_type == "":
            stock_type = "обыкновенные"
        elif stock_type == '2':
            stock_type = "привилегированные"
        else:
            stock_type = "привилегированные"
        
