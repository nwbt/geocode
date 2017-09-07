#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import logging
import configparser
import csv
import json

from src.geocode_service import GoogleGeocodeService
from src.application_settings import ApplicationSettings
from src.clientele import Clientele

CONFIG_FILE = 'config/config.ini'


def main():
    app_settings = parse_config_file()
    clientele = build_clientele_from_csv_file(app_settings.input_file)
    gcs = GoogleGeocodeService(app_settings.api_key, clientele.client_list)
    clientele.client_list = gcs.geocode_addresses()
    write_json_to_file(app_settings.output_file, clientele.to_list_of_dicts())

def build_clientele_from_csv_file(file):
    clientele = None

    try:
        with open(file, encoding='latin-1') as csvfile:
            clientele = Clientele()

            try:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)

                try:
                    if not dialect:
                        dialect = 'excel'
                    reader = csv.DictReader(csvfile, dialect=dialect)
                    logging.debug('opened file: ' + file)
                    for idx, row in enumerate(reader):
                        logging.debug('row number:' + str(idx + 1) + ', row content:' + str(row))
                        clientele.add_client(row)

                except IOError as ex:
                    logging.critical(ex)

            except UnicodeDecodeError as ex:
                logging.critical(ex)

    except FileNotFoundError as ex:
        logging.critical(ex)

    return clientele

def parse_config_file():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)  # todo handle exceptions

    app = ApplicationSettings()

    app.log_level = config['DEFAULT']['LogLevel']
    app.log_file = config['DEFAULT']['LogFile']
    app.api_key = config['SECRET']['APIKey']
    app.input_file = config['DEFAULT']['InputFile']
    app.output_file = config['DEFAULT']['OutputFile']

    app.start_logging()
    app.verify_settings()

    return app

def write_json_to_file(output_file, json_as_str):
    with open(output_file, 'w') as file:
        json.dump(json_as_str, file)


if __name__ == '__main__':
    main()
