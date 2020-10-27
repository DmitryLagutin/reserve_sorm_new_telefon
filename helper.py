import datetime
import inspect
from peewee import *
from datetime import date
import settings
from settings import *
from pprint import pformat
import hashlib


# создаем файл, в которой будет учитываться название таблицы и record_id
def make_buffer_data(record_id):
    with open(settings.db_file, 'w') as stream:
        stream.write(f'{"tel001" + datetime.now().date().strftime("%Y%m%d")}-{record_id}')


# получаем файл, в которой будет учитываться название таблицы и record_id
def get_buffer_data():
    try:
        with open(db_file) as stream:
            s = stream.read().split('-')
            d = datetime.strptime(s[0][6:], '%Y%m%d')
            return s[0], s[1], d.date()
    except FileNotFoundError as ex:
        return None


# форматируем вид даты для передачи в csv
def format_datetime(date_x: str):
    return datetime.strftime(date_x, '%d.%m.%Y %H:%M:%S')


# выполнить sql
def run_sql(sql_str):
    list_csv_all_x = []
    list_row_x = []
    with settings.connection.cursor() as cursor:
        cursor.execute(sql_str)
        for row in cursor:
            # входящий вызов
            if str(row['trunk_in']).startswith('60-') or str(row['trunk_in']).startswith('70-'):
                call_type = 0
                type_defiant_ab = 1
                type_called_ab = 0
                trunk_in = str(row['trunk_in']).split('-')[0]
                trunk_out = trunk_in
                original_numfrom = row['original_numfrom']

                # определитель не должен быть пустым. Если ничего не прислали, пусть будет хоть что-то
                if original_numfrom == '':
                    original_numfrom = 0

                dialed_number = str(row['original_numto'])[1:]
                original_numto = '7' + str(row['original_numto'])[1:11]

            # исходящий вызов
            # с внешним миром АТС общается тоже без 8 спереди. Но раз абоненты тыкают в неё пальцами,
            # то и показывать её нужно, поэтому тут её не отрезаем
            # для маршрутизации внутри АТС используются префиксы 001 и 002
            # их видно в original_numto, но предбиллинг отрезает их в numto
            # поэтому здесь используем именно numto без original
            else:
                call_type = 1
                type_defiant_ab = 0
                type_called_ab = 1
                trunk_out = str(row['trunk_out']).split('-')[0]
                trunk_in = trunk_out

                # спецслужбы 01, 02, 03
                if str(row['numto']).startswith("0"):
                    # на 01 могут звонить люди без АОН. Поэтому всегда делаем принудительную подмену.
                    original_numfrom = 74957272424
                    dialed_number = row['numto']
                    original_numto = str(row['numto'])[:2]

                # точное время
                elif str(row['numto']).startswith("100"):
                    original_numfrom = '7' + str(row['original_numfrom'])
                    dialed_number = row['numto']
                    original_numto = 100

                # спецслужба 112
                elif str(row['numto']).startswith("112"):
                    # на 112 могут звонить только те, у кого есть АОН. Подмена не нужна.
                    original_numfrom = '7' + str(row['original_numfrom'])
                    dialed_number = row['numto']
                    original_numto = 112

                # заграница
                elif str(row['numto']).startswith("810"):
                    original_numfrom = '7' + str(row['original_numfrom'])
                    dialed_number = row['numto']
                    original_numto = str(row['numto'])[3:]

                # Россия
                else:
                    original_numfrom = '7' + str(row['original_numfrom'])
                    dialed_number = row['numto']
                    original_numto = '7' + str(row['numto'])[1:11]

            list_csv_all_x.append([settings.id_filial, format_datetime(row['timefrom']), row['duration'], call_type,
                                   settings.DVO, type_defiant_ab, type_called_ab,
                                   settings.code_ATC, trunk_in, trunk_out,
                                   row['cause'] + 600,
                                   original_numfrom,
                                   settings.internal_num_defiant_A, dialed_number, original_numto,
                                   settings.internal_num_called_A, settings.tel_num_forwarding])
            list_row_x.append(row)

    return list_csv_all_x, list_row_x[-1]['record_id'] if len(list_csv_all_x) > 0 else None


def check_none(x, return_else):
    return x if x is not None else return_else


def make_str_csv(a_dict):
    """
    Создает строку
    :param a_dict:
    :return:
    """
    try:
        list_x = []
        for item in a_dict.items():
            list_x.append(str(item[1]))
        return list_x

    except Exception as ex:
        print(str(ex))


def make_str_for_hexdigest(a_dict):
    result_str = ''
    for item in a_dict.items():
        result_str = result_str + str(item[1])

    return result_str


def modify_str_data(dict_x):
    for k, v in dict_x.items():
        if type(v) is str and '\n' in v:
            dict_x[k] = v.replace('\n', ' ')
    return dict_x
