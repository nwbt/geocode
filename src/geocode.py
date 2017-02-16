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

    gcs = GoogleGeocodeService(app_settings.api_key, clientele.client_list)

    gcs.geocode_addresses()

    write_json_to_file(app_settings.output_file, clientele.to_list_of_dicts())

def build_clientele_from_csv_file(file):
    clientele = None

    try:
        with open(file, encoding='latin-1') as csvfile:
            dialect = None
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

    def __init__(self, api_key=None, store_list=None):
        if api_key:
            self.api_key = api_key
        if store_list:
            self.list_of_clients = store_list

    @property
    def google_client(self):
        return self._client

    @google_client.setter
    def google_client(self, client):
        if type(client) is googlemaps.client.Client:
            self._client = client
        else:
            raise TypeError

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        self.google_client = googlemaps.client.Client(key=api_key)

    def geocode_addresses(self):
        for idx, store in enumerate(self.list_of_clients):
            address = str(store.address_from_csv)
            geocode_response = self.geocode_address(address)
            response_length = len(geocode_response)
            if response_length < 1:
                logging.error('response empty, address=' + str(store.address_from_csv))
            elif response_length == 1:
                self._sort_response(store, geocode_response[0])
            else:
                logging.warning('ambiguous request, multiple responses, address:' + str(store.address_from_csv))
                for i in geocode_response:
                    logging.warning(str(i))

    def geocode_address(self, address):
        try:
            return googlemaps.geocoding.geocode(self.google_client, address=address)
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _sort_response(self, store, response):
        # todo verify dict has values, log if not
        store.address_from_google = response['formatted_address']
        store.geocode = response['geometry']['location']


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
