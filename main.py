import requests
import json
from helper import *
from dbi_soap_client.dbi_soap import DbiSoap
import datetime
from main_functions import *
import csv
import logging
import argparse
import sys
from peewee import *
import settings
from datetime import timedelta

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Working with telephony SORM')
    parser.add_argument('-L', '--log-level', default=settings.log_level, help='Log level')
    parser.add_argument('-o', '--output', default=settings.csv_file_path, help='Output csv file path')

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level)
    logging.basicConfig(level=args.log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(args.log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    logging.info('Make csv file accounts run')
    # запускам основную функцию, котораяю будет создавать csv файл
    # make_csv_account_file()
    first_date = datetime(2020, 10, 1)
    for i in range(27):
        make_for_pavsukov_test(first_date + timedelta(days=i))

