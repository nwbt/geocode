#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import os
import logging
import configparser
import csv
import collections
import json
import googlemaps

CONFIG_FILE = 'config/config.ini'

DEFAULT_LOG_LEVEL = 'WARNING'
DEFAULT_LOG_FILE = 'logs/geocode.log'
DEFAULT_LOG_MSG = '%(asctime)s|%(levelname)s|%(message)s'


def main():
    app_settings = parse_config_file()
    clientele = build_clientele_from_csv_file(app_settings.input_file)

    gcs = GoogleGeocodeService()
    gcs.api_key = app_settings.api_key
    gcs.clients = clientele.client_list

    gcs.client_connection()
    gcs.geocode_addresses()

    write_json_to_file(app_settings.output_file, clientele.to_list_of_dicts())

def build_clientele_from_csv_file(file):
    clientele = None
    try:
        with open(file) as csvfile:
            clientele = Clientele()
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            try:
                reader = csv.DictReader(csvfile, dialect=dialect)
                logging.debug('opened file: ' + file)
                for idx, row in enumerate(reader):
                    logging.debug('row number:' + str(idx + 1) + ', row content:' + str(row))
                    clientele.add_client(row)

            except IOError as ioe:
                logging.critical(ioe)

    except FileNotFoundError as fnfe:
        logging.critical(fnfe)

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


class Address:
    street_address_1 = None
    street_address_2 = None
    city = None
    state = None
    zip = None

    def __init__(self, info=None):
        if type(info) is collections.OrderedDict:
            self._dict_to_address(info)

        elif info is not None:
            # todo log error
            raise TypeError

    def _dict_to_address(self, info):
        city = info['city']
        zip = info['zip']

        if not city and not zip:
            # todo log error
            raise ValueError

        self.street_address_1 = info['address_1']
        self.street_address_2 = info['address_2']
        self.city = city
        self.state = info['state']
        self.zip = zip

    def to_dict(self):
        return {
            'street_address_1': self.street_address_1,
            'street_address_2': self.street_address_2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }

    def __str__(self):
        return self.street_address_1 + ' ' \
               + self.street_address_2 + ' ' \
               + self.city + ', ' \
               + self.state + ' ' \
               + self.zip


class ApplicationSettings:
    log_level = None
    log_file = None

    input_file = None
    output_file = None
    api_key = None

    def start_logging(self):
        self._verify_log_file()
        self._verify_log_level()
        logging.basicConfig(filename=self.log_file, level=self.log_level, format=DEFAULT_LOG_MSG)

    def verify_settings(self):
        self._verify_api_key_valid()
        self._verify_input_file_exists()
        self._verify_output_file_path()

    def _verify_input_file_exists(self):
        # todo check that it exists if not log error and create default
        pass

    def _verify_output_file_path(self):
        # todo check that it exists if not create path (if valid) and attempt to create file
        pass

    def _verify_api_key_valid(self):
        # todo check that it is valid & if not log error and exit
        pass

    def _verify_log_level(self):
        acceptable_log_levels = {
            'CRITICAL': logging.CRITICAL,
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING
        }

        try:
            self.log_level = acceptable_log_levels[self.log_level]
        except KeyError:
            # todo log error to stderr since logging is not enabled yet
            self.log_level = acceptable_log_levels[DEFAULT_LOG_LEVEL]

    def _verify_log_file(self):
        filename = self.log_file
        directory = os.path.dirname(filename)

        if not os.access(directory, os.F_OK | os.W_OK):

            self.log_file = DEFAULT_LOG_FILE

            if not os.path.exists(os.path.dirname(self.log_file)):
                try:
                    os.makedirs(directory)
                except PermissionError as pe:
                    # todo log error to stderr since logging is not enabled yet
                    pass


class Clientele:
    client_list = []

    def add_client(self, client_dict):
        try:
            client = Store(client_dict)
            self.client_list.append(client)
        except Exception as e:
            print(str(e))
            logging.error(e)

    def to_list_of_dicts(self):
        clientele_json = []
        for i in self.client_list:
            clientele_json.append(i.to_dict())
        return clientele_json


class GoogleGeocodeService:
    clients = None
    api_key = None

    def geocode_addresses(self):
        for idx, client in enumerate(self.clients):
            address = str(client.address_from_csv)
            geocode_response = self.geocode_address(address)
            if len(geocode_response) == 1:
                self._sort_response(client, geocode_response[0])
            else:
                # todo raise error and log
                print('uh that shouldn\'t have happened' + client.pre_full_address)

    def _sort_response(self, client, response):
        # todo verify dict has values, log if not
        client.google_address = response['formatted_address']
        client.geocode = response['geometry']['location']

    def geocode_address(self, address):
        try:
            return googlemaps.geocoding.geocode(self.client, address=address)
        except googlemaps.exceptions.ApiError as apie:
            logging.critical(apie)
            # todo may want to stop application on this type of error
            return None

    def client_connection(self):
        try:
            self.client = googlemaps.client.Client(key=self.api_key)
        except ValueError as ve:
            logging.critical(ve)
            print(ve)


class Store():
    address_from_csv = None
    address_from_google = None
    geocode = None
    phone_number = None
    store_name = None

    def __init__(self, client_dict=None):
        if type(client_dict) is collections.OrderedDict:
            self._dict_to_store(client_dict)
        elif client_dict is None:
            self.address_from_csv = Address()
        else:
            # todo log error
            raise TypeError

    def _dict_to_store(self, client_dict):
        self.store_name = client_dict['store_name']
        self.phone_number = client_dict['phone']
        self.address_from_csv = Address(client_dict)

    def to_dict(self):
        return {
            'store_name': self.store_name,
            'phone_number': self.phone_number,
            'address_components': self.address_from_csv.to_dict(),
            'google_address': self.address_from_google,
            'geocode': self.geocode
        }


if __name__ == '__main__':
    main()
