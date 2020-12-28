import re
from utils import *
from consts import *
import random


class fill_data:
    token_book = {
        "#!date_literally!#": get_date(variant=0).capitalize(),
        "#!date_variant1!#": get_date(variant=1),
        "#!date_variant2!#": get_date(variant=2),
        }

    def __init__(self, data_string=None, debug=False):
        self.msg_before_input = ""
        if not data_string:
            data_string = input(self.msg_before_input)
        self._debug = debug
        self.source = data_string
        self.filled_with_debug = False
        if self._debug:
            self.fill_with_debug()
            self.filled_with_debug = True

        self.exact = None
        self.data = {}
        pass

    @staticmethod
    def add(tokeninfo):
        if isinstance(tokeninfo, dict):
            for k, v in tokeninfo.items():
                fill_data.token_book[k] = v
        elif (isinstance(tokeninfo, tuple) or isinstance(tokeninfo, list)) and len(tokeninfo) == 2:
            key, value = tokeninfo
            fill_data.token_book[key] = value

    def fill_fields(self):
        raise NotImplementedError

    def fill_with_debug(self):
        raise NotImplementedError

    def __repr__(self):
        return self.source

    def check_correct(self):
        raise NotImplementedError

    def decline_input(self):
        print(f"Данные введены неверно. {self.source}")
        raise TypeError


class FIO(fill_data):
    REGEX_FIO_TEMPLATE = re.compile(r'^[А-я]{3,}\s+[А-я]{3,}\s+[А-я]{3,}$')
    REGEX_FIO_PART_TEMPLATE = re.compile(r'[А-я]{3,}')

    def __init__(self, *args, **kwargs):
        self.exact = True
        self.msg_before_input = f'''Введите полное ФИО.
         Пример: Иванов Иван Иванович\n'''
        print(self.msg_before_input)
        super().__init__(*args, **kwargs)

        if self.filled_with_debug:
            return
        self.surename = "####"
        self.name = '####'
        self.patronim = "#####"
        if not re.match(FIO.REGEX_FIO_TEMPLATE, self.source):
            self.decline_input()
            return
        self.surename, self.name, self.patronim = re.findall(
            FIO.REGEX_FIO_PART_TEMPLATE,
            self.source
            )
        self.fill_fields()

    def fill_fields(self):
        fio_list = [self.surename, self.name, self.patronim]
        fill_data.add({
            '#!fio_full!#': " ".join(fio_list),
            '#!fio_initials!#': f"{self.surename} {self.name[0]}. {self.patronim[0]}."
        })
        fill_data.add({f"#!fio_full{i}!#": x for i, x in enumerate(fio_list)})

    def fill_with_debug(self):
        self.surename = random.choice(BASIC_SURENAMES)
        self.name = random.choice(BASIC_NAMES)
        self.patronim = random.choice(BASIC_PATRONIMS)
        self.fill_fields()


class SeriaNomer(fill_data):
    REGEX_PASSPORT_SERIA_NOMER_TEMPLATE = re.compile(r"\d{4}\s*\d{6}$")

    def __init__(self, *args, **kwargs):
        self.exact = True
        self.msg_before_input = f'''Введите серию и номер паспорта.
        Пример: 1234123456, 1234 123456\n'''
        print(self.msg_before_input)
        super().__init__(*args, **kwargs)

        if self.filled_with_debug:
            return
        self.seria_nomer = "##########"
        if not re.match(
            SeriaNomer.REGEX_PASSPORT_SERIA_NOMER_TEMPLATE,
            self.source
                ):
            self.decline_input()
            return
        self.seria_nomer = "".join(re.findall(r"\d", self.source))
        self.fill_fields()

    def fill_fields(self):
        fill_data.add({
            "#!seria_nomer!#": self.seria_nomer,
            "#!seria_nomer_0!#": self.seria_nomer[:4],
            "#!seria_nomer_1!#": self.seria_nomer[4:],
        })
        fill_data.add({f"#!seria_nomer{i}": x for i, x in enumerate(self.seria_nomer)})

    def fill_with_debug(self):
        self.seria_nomer = "".join([str(random.randint(0, 9)) for i in range(10)])
        self.fill_fields()


class Date(fill_data):
    REGEX_DIGIT_FROM_DATE_TEMPLATE = re.compile(r'\d+')
    REGEX_DATE_TEMPLATE = re.compile(r'\d+\D\d+\D\d+$')
    MESSAGES = {
        "1": "Введите дату выдачи паспорта.\nПример: 12.12.2012 или даже так 2.6.94",
        "2": "Введите дату рождения.\nПример: 12.12.2012 или даже так 2.6.94",
    }
    TYPE_TOKEN = {
        '1': '#!data_vidachi!#',
        '2': "#!birth_date!#"
    }

    def __init__(self, _type, *args, **kwargs):
        '''
        _type
        1 : Date of issue
        2 : Date of birth
        '''
        self.msg_before_input = Date.MESSAGES[_type]
        print(Date.MESSAGES[_type])
        self._type = _type
        self._token = Date.TYPE_TOKEN[_type]
        super().__init__(*args, **kwargs)

        if self.filled_with_debug:
            return
        if not re.match(
            Date.REGEX_DATE_TEMPLATE,
            self.source
                ):
            self.decline_input()
            return
        self.date_numbers = re.findall(
            Date.REGEX_DIGIT_FROM_DATE_TEMPLATE,
            self.source
            )
        self.fill_fields()

    def fill_fields(self):
        for i, number in enumerate(self.date_numbers[:1]):
            if len(number) < 2:
                self.date_numbers[i] = "0" + number
        if len(self.date_numbers[2]) < 4:
            year = int(self.date_numbers[2])
            if year < 20:
                year += 2000
            else:
                year += 1900
            self.date_numbers[2] = str(year)
        fill_data.add({Date.TYPE_TOKEN[self._type]: '.'.join(self.date_numbers)})
        # Посимвольно добавить дату с токенами birth_date0,1,2... или data_vidachi0,1,2 и тд
        fill_data.add({put_substring(Date.TYPE_TOKEN[self._type], str(i), Date.TYPE_TOKEN[self._type].find("!#")): x for i, x in enumerate(".".join(self.date_numbers))})

    def fill_with_debug(self):
        self.date_numbers = [
            str(random.randint(1, 32)),
            str(random.randint(1, 13)),
            str(random.randint(1, 2021))
        ]
        self.fill_fields()


class AdrIndex(fill_data):
    MESSAGES = {
        '1': 'Индекс регистрации.\nПример: 123987',
        '2': 'Индекс фактического места проживания.\nПример: 123987\nЕсли пусто, то будет записан индекс регистрации',
    }
    REGEX_ADRESS_INDEX_TEMPLATE = re.compile(r"\d{6}$")

    def __init__(self, _type, *args, **kwargs):
        self.exact = True
        self._type = _type
        self.msg_before_input = AdrIndex.MESSAGES[_type]
        # print(AdrIndex.MESSAGES[_type])
        print(self.msg_before_input)
        super().__init__(*args, **kwargs)

        if self.filled_with_debug:
            return
        self.index = "######"
        if not re.match(
            SeriaNomer.REGEX_ADRESS_INDEX_TEMPLATE,
            self.source
                ):
            self.decline_input()
            return
        self.index = self.source
        self.fill_fields()

    def fill_fields(self):
        fill_data.add({"#!registration_index!#": self.index})
        fill_data.add({f"#!registration_index{i}!#": x for i, x in enumerate(self.index)})

    def fill_with_debug(self):
        self.index = ''
        for _ in range(6):
            self.index += str(random.randint(0, 10))
        self.fill_fields()


class FacilityCode(fill_data):
    REGEX_FACILITY_CODE_TEMPLATE = re.compile(r'\d{3}-\d{3}')

    def __init__(self, *args, **kwargs):
        self.exact = True
        self.msg_before_input = f"""Код подразделения, где выдан паспорт\nПример: 730-123"""
        print(self.msg_before_input)
        super().__init__(*args, **kwargs)

        if self.filled_with_debug:
            return
        self.code = "###-###"
        if not re.match(
            SeriaNomer.REGEX_ADRESS_INDEX_TEMPLATE,
            self.source
                ):
            self.decline_input()
            return
        self.code = self.source

    def fill_fields(self):
        fill_data.add({'#!kod_kem_vidan!#': self.code})
        fill_data.add({f'#!kod_kem_vidan{i}!#': x for i, x in enumerate(self.code)})

    def fill_with_debug(self):
        self.code = ""
        for _ in range(2):
            for _ in range(3):
                self.code += str(random.randint(0, 10))
            self.code += "-"
        self.code = self.code[:7]
        self.fill_fields()


class JustString(fill_data):
    MESSAGES = {
        "kem_vidan": "Кем выдан паспорт.\nПросто строка, что введешь, то и вставит в документ.",
        "registration_adress": "Адрес регистрации.\nПросто строка, что введешь, то и вставит в документ",

        }
    TYPE_TOKEN = {
        'kem_vidan': '#!kem_vidan!#',
        'registration_adress': "#!registration_adress!#"
    }

    def __init__(self, _type, *args, **kwargs):
        self.exact = False
        self._type = _type
        self.msg_before_input = JustString.MESSAGES[_type]
        print(JustString.MESSAGES[_type])
        super().__init__(*args, **kwargs)
        if self.filled_with_debug:
            return
        self.content = self.source
        self.fill_fields()

    def fill_fields(self):
        fill_data.add({JustString.TYPE_TOKEN[self._type]: self.content})

    def fill_with_debug(self):
        self.content = ""
        for _ in range(random.randint(4, 12)):
            for _ in range(random.randint(3, 10)):
                self.content += random.choice("ЯЧСМИТЬБЮФЫВАПРОЛДЖЭЙЦЙУКЕН12334567890")
            self.content += " "
        fill_data.add({JustString.TYPE_TOKEN[self._type]: self.content})
