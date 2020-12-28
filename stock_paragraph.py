from num2string import num2text
import re
from utils import *
from consts import REGISTRATOR_LIST, AO_LIST

MSG_JUST_STRING_ASK = 'Обычная строка, введите хоть что-то.'
MSG_JUST_STRING_ERROR = 'Нужно ввести хоть что-нибудь.'

MSG_STOCK_AMOUNT_ASK = "Введите колчиество покупаемых акций.\nПример: 123445"
MSG_STOCK_AMOUNT_ERROR = "Данные введены неправильно, повторите ввод."
REGEX_STOCK_AMOUNT = re.compile(r"^\d+$")

MSG_STOCK_PRICE_ACK = 'По сколько покупаем за акцию?\nПримеры: 1, 1.33, 36.5\n'
MSG_STOCK_PRICE_ERROR = "Неправильно введена цена, смотри на примеры и повтори ввод!"
REGEX_STOCK_PRICE = re.compile(r'^\d+\.*\d*$')

MSG_STOCK_TYPE = "Какого типа акции покупаем?"


class Registrator:
    def __init__(self, registrator_name, registrator_docs):
        self.name = registrator_name
        self.documents = registrator_docs


class AOobject:
    def __init__(self, AOtype=None, registrator=None, reg_codes=None):
        if not AOtype:
            print('Введите название АО')
            self.name = get_input(re.compile(r'.+'), MSG_JUST_STRING_ASK, MSG_JUST_STRING_ERROR)
        if not registrator:
            while True:
                print("Выберите регистратор для данного из списка")
                for i, regr in enumerate(REGISTRATOR_LIST, 1):
                    print(f"{i} : {regr.name}")
                chose = input('Какой из них?\n')
                try:
                    self.registrator = REGISTRATOR_LIST[int(chose) - 1]
                    print(f"Выбран регистратор: {self.registrator.name}")
                    break
                except IndexError:
                    print("Нужно ввест номер из приведенного списка!")
        if not reg_codes:
            print('Введите регистрационный код акций, которые покупаем')
            self.reg_codes = [get_input(re.compile(r'.+'), MSG_JUST_STRING_ASK, MSG_JUST_STRING_ERROR)]


class StockParagraph:
    def __init__(self):
        self.stock_amount = get_input(REGEX_STOCK_AMOUNT, MSG_STOCK_AMOUNT_ASK, MSG_STOCK_AMOUNT_ERROR)
        self.stock_amount_literally = num2text(int(self.stock_amount))
        self.stock_type_input()
        self.AO_input()
        self.AOreg_code_input()
        self.stock_price_input()
        self.stock_itogo_input()

    def stock_type_input(self):
        print("Тип самих акций:\n1: обыкновенные\n2: привилегированные")
        print("Также можно так:\nпустая строка : обыкновенные\nстрока с чем-то : привилегированные")
        stock_type = input()
        if stock_type == '1' or stock_type == "":
            stock_type = "обыкновенные"
        elif stock_type == '2':
            stock_type = "привилегированные"
        else:
            stock_type = "привилегированные"
        self.stock_type = stock_type

    def AO_input(self):
        print()
        for i, AO in enumerate(AO_LIST, 1):
            print(f"{i} : {AO.name}")

        input_data = input("Либо номер из списка, либо название АО, которого нет.")
        try:
            self.AO = AO_LIST[int(input_data)]
            self.customAO = False
        except ValueError:
            self.AO = AOobject()
            self.customAO = True

    def AOreg_code_input(self):
        while True:
            try:
                if self.customAO:
                    self.AOreg_code = self.AO.reg_codes[0]
                    break
                else:
                    AOreg_code_index = 0 if self.stock_type == "обыкновенные" else 1
                    self.AOreg_code = self.AO.reg_codes[AOreg_code_index]
                    break
            except IndexError:
                print(f"У {self.AO.name} нет акций, типа {self.stock_type}\Повторите ввод")

    def stock_price_input(self):
        self.stock_price_str = get_input(REGEX_STOCK_PRICE, MSG_STOCK_PRICE_ACK, MSG_STOCK_PRICE_ERROR)
        self.stock_price_float = float(self.stock_price_str)
        self.stock_price_rub = int(self.stock_price_float)
        self.stock_itogo = float()
        self.stock_price_kopeek = int(100*(self.stock_price_float - self.stock_price_rub))

    def stock_itogo_input(self):
        self.stock_itogo = int(self.stock_price_float * self.stock_amount) + 1
        self.stock_itogo_literally = num2text(int(self.stock_itogo))
