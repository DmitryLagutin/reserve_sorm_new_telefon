from helper import *
import csv
from dbi_soap_client.dbi_soap import DbiSoap
# from settings import DBI_SOAP
import settings
import logging
from datetime import datetime
from pprint import pprint

select_list = 'timefrom, duration, trunk_in, trunk_out, cause, original_numfrom, original_numto, record_id, numto'
where_trunk_sql = "(trunk_in like '60-%' or trunk_in like '70-%' or trunk_out like '60-%' or trunk_out like '70-%')"


def make_csv_account_file():
    list_csv_result = []
    buffer_data = get_buffer_data()
    table_name_from_file = None,
    record_id_from_file = None,
    date_from_file = None

    if buffer_data is None:
        print("Файл не найден")

    else:
        table_name_from_file, record_id_from_file, date_from_file = buffer_data

    if date_from_file is None:
        list_csv_all, last_record = run_sql(
            f'''select {select_list}
            from tel001{datetime.now().date().strftime('%Y%m%d')}
            where parent_id = 0
            and {where_trunk_sql}''')
        list_csv_result = list_csv_all
        if last_record is not None:
            make_buffer_data(last_record)
    else:
        if datetime.now().date() > date_from_file:
            list_csv_all_last, last_record_last = run_sql(
                f'''select {select_list}
                from {table_name_from_file}
                where record_id > {record_id_from_file}
                and parent_id = 0
                and {where_trunk_sql}''')
            list_csv_all_new, last_record_new = run_sql(
                f'''select {select_list}
                from tel001{datetime.now().date().strftime('%Y%m%d')}
                where parent_id = 0
                and {where_trunk_sql}''')
            list_csv_result.extend(list_csv_all_last)
            list_csv_result.extend(list_csv_all_new)
            if last_record_new is not None:
                make_buffer_data(last_record_new)
        elif datetime.now().date() == date_from_file:
            list_csv_all_new, last_record_new = run_sql(
                f'''select {select_list}
                from {table_name_from_file}
                where record_id > {record_id_from_file}
                and parent_id = 0
                and {where_trunk_sql}''')
            list_csv_result.extend(list_csv_all_new)
            if last_record_new is not None:
                make_buffer_data(last_record_new)
    # основная функиця, которая формирует строки csv
    if len(list_csv_result) > 0:
        with open(settings.csv_file_path + format_filename_csv, "w", encoding='cp1251', newline="\n") as file:
            csv.writer(file, delimiter='\t', quoting=csv.QUOTE_NONE).writerows(
                list_csv_result)
            logging.info(f'file {format_filename_csv} is ready. Created {len(list_csv_result)} lines')


def make_for_pavsukov_test(date_x):
    list_csv_result = []
    date_from_file = None

    if date_from_file is None:
        list_csv_all, last_record = run_sql(
            f'''select {select_list}
            from tel001{date_x.date().strftime('%Y%m%d')}
            where parent_id = 0
            and {where_trunk_sql}''')
        list_csv_result = list_csv_all
        if last_record is not None:
            make_buffer_data(last_record)
    # основная функиця, которая формирует строки csv
    if len(list_csv_result) > 0:
        with open(settings.csv_file_path + f'abonents_pavshukov_{date_x.date().strftime("%Y%m%d")}', "w",
                  encoding='cp1251', newline="\n") as file:
            csv.writer(file, delimiter='\t', quoting=csv.QUOTE_NONE).writerows(
                list_csv_result)
            logging.info(f'file {format_filename_csv} is ready. Created {len(list_csv_result)} lines')
