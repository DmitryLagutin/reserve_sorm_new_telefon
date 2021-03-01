import os
from datetime import datetime
import logging
from peewee import *
import socket
import pymysql.cursors

# формат записи файла csv, который получается на выходе при генерации списка абонентов с указанием даты создания
format_filename_csv = 'abonents-{0}.csv'.format(datetime.now().strftime('%Y%m%d%H%M%S'))

# уровень логгирования по умолчанию в параметрах argparse
log_level = "INFO"

# путь до файла с итоговым сsv файлом
csv_file_path = ''

# дата, которую надо указать в таблице
date_for_table = datetime.now().date().strftime('%Y%m%d')

# путь до файла с состоянием
db_file = 'db.txt'

connection = pymysql.connect(host='@@@@@@@@@@@',
                             user='@@@@@@@',
                             password='@@@@@@',
                             db='@@@@@@',
                             cursorclass=pymysql.cursors.DictCursor)

# временные данные , p - еще не переданные Пашуковым
id_filial = 1
DVO = 1
code_ATC = 1
internal_num_defiant_A = ''
internal_num_called_A = ''
tel_num_forwarding = ''


