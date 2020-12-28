from stock_paragraph import Registrator, AOobject


BASIC_NAMES = [
    'Владимир',
    'Александр',
    "Евгений",
    "Аркадий",
    "Иван"
    ]
BASIC_PATRONIMS = [
    "Владимирович",
    "Александрович",
    "Евгеньевич",
    "Аркадьевич",
    "Иванович"
    ]
BASIC_SURENAMES = [
    "Владимиров",
    "Александров",
    "Шевченко",
    "Штейн",
    "Алёхин"
    ]

REGISTRATOR_LIST = [
    Registrator(
        registrator_name='НРК "РОСТ"',
        registrator_docs=['anketa_rost.docx', 'rasp_rost.docx']
        ),
    Registrator(
        registrator_name='ДРАГА',
        registrator_docs=['anketa_draga.docx', 'rasp_draga.docx']
        ),
    Registrator(
        registrator_name='СТАТУС',
        registrator_docs=['anketa_status.docx', 'rasp_status.docx']
        ),
    Registrator(
        registrator_name='ВТБ',
        registrator_docs=['anketa_vtb.docx', 'rasp_vtb.docx']
        ),
    Registrator(
        registrator_name='НОВЫЙ РЕГИСТРАТОР',
        registrator_docs=['anketa_new_registrator.docx', 'rasp_new_registrator.docx']
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
