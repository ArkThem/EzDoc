from num2string import num2text
import re
import random
from fill_data_class import fill_data
from utils import *


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
        else:
            self.name = AOtype
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
        else:
            self.registrator = registrator
        if not reg_codes:
            print('Введите регистрационный код акций, которые покупаем')
            self.reg_codes = [get_input(re.compile(r'.+'), MSG_JUST_STRING_ASK, MSG_JUST_STRING_ERROR)]
        else:
            self.reg_codes = reg_codes


class StockParagraph:
    itogo = 0
    itogo_literally = ""
    PARAGRAPH_TOKEN = '#!stock_paragraph!#'

    def __init__(self, debug=False):
        self.token_book = {}
        self.debug = debug
        if debug:
            self.stock_amount = str(random.randint(3, 15000))
        else:
            self.stock_amount = get_input(REGEX_STOCK_AMOUNT, MSG_STOCK_AMOUNT_ASK, MSG_STOCK_AMOUNT_ERROR)
        self.stock_amount_literally = num2text(int(self.stock_amount))
        self.add({
            '#!stock_amount!#': self.stock_amount,
            '#!stock_amount_literally!#': self.stock_amount_literally
            })
        self.stock_type_input()
        self.AO_input()
        self.AOreg_code_input()
        self.stock_price_input()
        self.stock_itogo_input()
        self.text = f'''               - {self.stock_amount} ({self.stock_amount_literally}) штук {self.stock_type} акций {self.AO.name}, регистрационный номер {self.AOreg_code}. Стоимость одной акции по Договору составляет {self.stock_price_rub} руб. {self.stock_price_kopeek} коп.'''
        self.add({
            '#!stock_type!#': self.stock_type,
            '#!AOtype!#': self.AO.name,
            '#!AOreg_code!#': self.AOreg_code,
            '#!stock_itogo!#': str(self.stock_itogo),
            '#!stock_itogo_literally!#': self.stock_itogo_literally,
        })

    def stock_type_input(self):
        if self.debug:
            self.stock_type = random.choice(["обыкновенные","привилегированные"])
            # self.add({'#!stock_type!#': self.stock_type})
            return
        print("Тип самих акций:\n1: обыкновенные\n2: привилегированные")
        print("Также можно так:\nпустая строка : обыкновенные\nстрока с чем-то : привилегированные")
        stock_type = input("\n")
        if stock_type == '1' or stock_type == "":
            stock_type = "обыкновенные"
        elif stock_type == '2':
            stock_type = "привилегированные"
        else:
            stock_type = "привилегированные"
        self.stock_type = stock_type
        # self.add({'#!stock_type!#': self.stock_type})

    def AO_input(self):
        if self.debug:
            self.AO = random.choice(AO_LIST)
            # self.add({'#!AOtype!#': self.AO.name})
            self.customAO = False
            return
        print()
        for i, AO in enumerate(AO_LIST, 1):
            print(f"{i} : {AO.name}")

        input_data = input("Либо номер из списка, либо название АО, которого нет.\n")
        try:
            self.AO = AO_LIST[int(input_data)]
            # self.add({'#!AOtype!#': self.AO.name})
            self.customAO = False
        except ValueError:
            self.AO = AOobject()
            # self.add({'#!AOtype!#': self.AO.name})
            self.customAO = True

    def AOreg_code_input(self):
        if self.debug:
            self.AOreg_code = random.choice(self.AO.reg_codes)
            # self.add({'#!AOreg_code!#': self.AOreg_code})
            return
        while True:
            try:
                if self.customAO:
                    self.AOreg_code = self.AO.reg_codes[0]
                    # self.add({'#!AOreg_code!#': self.AOreg_code})
                    break
                else:
                    AOreg_code_index = 0 if self.stock_type == "обыкновенные" else 1
                    self.AOreg_code = self.AO.reg_codes[AOreg_code_index]
                    # self.add({'#!AOreg_code!#': self.AOreg_code})
                    break
            except IndexError:
                print(f"У {self.AO.name} нет акций, типа {self.stock_type}\Повторите ввод")

    def stock_price_input(self):
        if self.debug:
            self.stock_price_str = str(round(random.random(), 2)*float(random.randint(1, 10000)))
        else:
            self.stock_price_str = get_input(REGEX_STOCK_PRICE, MSG_STOCK_PRICE_ACK, MSG_STOCK_PRICE_ERROR)
        self.stock_price_float = float(self.stock_price_str)
        self.stock_price_rub = int(self.stock_price_float)
        self.stock_price_kopeek = int(100*(self.stock_price_float - self.stock_price_rub))

    def stock_itogo_input(self):
        self.stock_itogo = int(self.stock_price_float * int(self.stock_amount)) + 1
        self.stock_itogo_literally = num2text(int(self.stock_itogo))
        # self.add({
        #     '#!stock_itogo!#': str(self.stock_itogo),
        #     '#!stock_itogo_literally!#': self.stock_itogo_literally,
        #     })
        StockParagraph.itogo += self.stock_itogo
        StockParagraph.itogo_literally = num2text(StockParagraph.itogo)
        fill_data.add({
            '#!final_price_rub!#': str(StockParagraph.itogo),
            '#!final_price_literally!#': StockParagraph.itogo_literally,
            '#!final_price_kopeek!#': '0'
            })

    def add(self, tokeninfo):
        if isinstance(tokeninfo, dict):
            for k, v in tokeninfo.items():
                self.token_book[k] = v
        elif (isinstance(tokeninfo, tuple) or isinstance(tokeninfo, list)) and len(tokeninfo) == 2:
            key, value = tokeninfo
            self.token_book[key] = value


REGISTRATOR_LIST = [
    Registrator(
        registrator_name='НРК "РОСТ"',
        registrator_docs=['docs/anketa_rost.docx', 'docs/rasp_rost.docx']
        ),
    Registrator(
        registrator_name='ДРАГА',
        registrator_docs=['docs/anketa_draga.docx', 'docs/rasp_draga.docx']
        ),
    Registrator(
        registrator_name='СТАТУС',
        registrator_docs=['docs/anketa_status.docx', 'docs/rasp_status.docx']
        ),
    Registrator(
        registrator_name='ВТБ',
        registrator_docs=['docs/anketa_vtb.docx', 'docs/rasp_vtb.docx']
        ),
    Registrator(
        registrator_name='НОВЫЙ РЕГИСТРАТОР',
        registrator_docs=['docs/anketa_new_registrator.docx', 'docs/rasp_new_registrator.docx']
        ),
]

AO_LIST = [
    # 1
    AOobject(
        AOtype='Акционерноe общество "ЛОМО"',
        registrator=REGISTRATOR_LIST[1],
        reg_codes=['1-02-00074-A', "2-02-00074-A"]
    ),
    # 2
    AOobject(
        AOtype='Публичное акционерное общество "Ростелеком""',
        registrator=REGISTRATOR_LIST[3],
        reg_codes=['1-01-00124-A', '2-01-00124-A']
    ),
    # 3
    AOobject(
        AOtype='Публичное акционерное общество "Горно-металлургическая компания "Норильский никель"',
        registrator=REGISTRATOR_LIST[0],
        reg_codes=['1-01-40155-F']
    ),
    # 4
    AOobject(
        AOtype='Публичное акционерное общество "Полюс"',
        registrator=REGISTRATOR_LIST[0],
        reg_codes=['1-01-55192-E']
    ),
    # 5
    AOobject(
        AOtype='Публичное акционерное общество "Газпром"',
        registrator=REGISTRATOR_LIST[1],
        reg_codes=['1-02-00028-A']
    ),
    # 6
    AOobject(
        AOtype='Публичное акционерное общество "Сбербанк России"',
        registrator=REGISTRATOR_LIST[2],
        reg_codes=['1-03-01481-B', '2-03-01481-B']
    ),
    # 7
    AOobject(
        AOtype='Ленское золотодобывающее публичное акционерное общество "Лензолото"',
        registrator=REGISTRATOR_LIST[0],
        reg_codes=['1-02-40433-N', '2-02-40433-N']
    ),
    # 8
    AOobject(
        AOtype='Публичное акционерное общество "Россети Ленэнерго"',
        registrator=REGISTRATOR_LIST[0],
        reg_codes=['1-01-00073-A', '2-01-00073-A']
    ),
    # 9
    AOobject(
        AOtype='Публичное акционерное общество "Территориальная генерирующая компания №1"',
        registrator=REGISTRATOR_LIST[1],
        reg_codes=['1-01-03388-D']
    ),
    # 10
    AOobject(
        AOtype='Публичное акционерное общество энергетики и электрификации "Мосэнерго"',
        registrator=REGISTRATOR_LIST[1],
        reg_codes=['1-01-00085-A']
    ),
]
