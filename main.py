from stock_paragraph import *
from fill_data_class import *
from functools import reduce
from utils import *
import re
import os
import docx


DEBUG = True
SAVE_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', "Документы из программы")


client_fio = FIO(debug=DEBUG)
client_birth_date = Date(_type='2', debug=DEBUG)
client_birth_place = JustString(_type='birth_place', debug=DEBUG)
clien_seria_nomer = SeriaNomer(debug=DEBUG)
client_data_vidachi = Date(_type='1', debug=DEBUG)
client_kem_vidan = JustString(_type='kem_vidan', debug=DEBUG)
client_kod_kem_vidan = FacilityCode(debug=DEBUG)
client_registration_index = AdrIndex(_type='1', debug=DEBUG)
cliend_registration_adress = JustString(_type='registration_adress', debug=DEBUG)
client_fact_index = AdrIndex(_type='2', debug=DEBUG)
client_fact_adress = JustString(_type='fact_adress', debug=DEBUG)
client_telephone = Telephone(debug=DEBUG)

paragraph_amount = int(get_input(
    re.compile(r"^\d"),
    message_ask="Сколько вариантов акций покупаем?",
    message_error="Нужно число ввести обычное числo"
    ))

paragraphs = [StockParagraph(debug=DEBUG) for _ in range(paragraph_amount)]
summary_paragraphs = reduce(lambda a, b: a + f"\n{b}", [x.text for x in paragraphs])

dkp = docx.Document('docs/dkp.docx')
doc_dict_replace(dkp, fill_data.token_book)
insert_before_token(dkp, StockParagraph.PARAGRAPH_TOKEN, summary_paragraphs)
dkp.save(os.path.join(SAVE_PATH, f"{fill_data.token_book['#!fio_initials!#']} ДКП.docx"))
del dkp

raspiska = docx.Document('docs/raspiska.docx')
doc_dict_replace(raspiska, fill_data.token_book)
raspiska.save(os.path.join(SAVE_PATH, f"{fill_data.token_book['#!fio_initials!#']} РАСПИСКА.docx"))
del raspiska

print('Проверь совпадение пола! Слова по типу: зарегестрирован, зарегестрирована...\n')
input("Программу можно закрыть, расписка и ДКП созданы. Сделать анкету и распоряжение для регистратора?\nНажмите Enter для продолжения.")

for stock_variant in paragraphs:
    current_case_dict = merge_two_dicts(fill_data.token_book, stock_variant.token_book)
    anketa_path, rasp_path = stock_variant.AO.registrator.documents
    anketa = docx.Document(anketa_path)
    doc_dict_replace(anketa, current_case_dict)
    anketa.save(os.path.join(SAVE_PATH, f"{fill_data.token_book['#!fio_initials!#']} АНКЕТА.docx"))
    del anketa

    rasp = docx.Document(rasp_path)
    doc_dict_replace(rasp, current_case_dict)
    rasp.save(os.path.join(SAVE_PATH, f"{fill_data.token_book['#!fio_initials!#']} РАСПОРЯЖЕНИЕ.docx"))
    del rasp

if DEBUG:
    for k, v in fill_data.token_book.items():
        print(f"{k} : {v}")
    print()
    for text in paragraphs:
        print(text.text)
        print(f"{text.stock_itogo_literally}")
        print(text.stock_itogo)
