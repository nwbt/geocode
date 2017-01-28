#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import argparse
import os
import logging

DEFAULT_LOG_LEVEL = 'WARNING'
DEFAULT_LOG_FILE = 'logs/geocode.log'
DEFAULT_LOG_MSG = '%(asctime)s|%(levelname)s|%(message)s'

def main():
    configureLogging()

    parser = argparse.ArgumentParser()
    args = _build_argument_list(parser)
    cli = CommandLineInput(args)

def configureLogging(level=None, filename=None):
    log_file = _verifyLogFile(filename)
    log_level = _verifyLogLevel(level)
    logging.basicConfig(filename=log_file, level=log_level, format=DEFAULT_LOG_MSG)


def _build_argument_list(parser):
    if type(parser) is not argparse.ArgumentParser:
        raise TypeError

    parser.add_argument('--input_file', '-i', help='', type=str, default='resources/stores.csv')
    parser.add_argument('--output_file', '-o', help='', type=str, default='resources/stores.json')
    parser.add_argument('--api_key', '-k', help='', type=str, default='resources/secrets')
    parser.add_argument('--log_level', '-l', help='', type=str)
    parser.add_argument('--log_file', '-f', help='', type=str)

    try:
        args = parser.parse_args()
        return args
    except Exception as e:
        # todo 1) figure out what type of error is returned and 2) log error
        pass

class CommandLineInput:

    def __init__(self, namespace):
        # important to change any specifics with respect to logging first
        self.log_level = _verifyLogLevel(namespace.log_level)
        self.log_file = _verifyLogFile(namespace.log_file)

        if self.log_file != DEFAULT_LOG_FILE or self.log_level != DEFAULT_LOG_LEVEL:
            configureLogging(level=self.log_level, filename=self.log_file)

        self.input_file = _inputFile(namespace.input_file)
        self.output_file = _outputFile(namespace.output_file)
        self.api_key = _apiKey(namespace.api_key)


def _inputFile(file):
    if not os.path.exists(file):
        raise FileNotFoundError

def _apiKey(key):
    # todo verify key's success
    pass

def _outputFile(file):
    if not os.path.exists(file):
        # todo create file
        pass

def _verifyLogLevel(level=None):
    ''' verifies log level is correct and if it is not sends in a default value '''
    log_level = level
    acceptable_log_levels = {
        'CRITICAL':logging.CRITICAL,
        'DEBUG':logging.DEBUG,
        'ERROR':logging.ERROR,
        'INFO':logging.INFO,
        'WARNING':logging.WARNING
    }
    if not log_level or log_level.upper() not in acceptable_log_levels:
        log_level = DEFAULT_LOG_LEVEL
    else:
        log_level = log_level.upper()

    return acceptable_log_levels[log_level]

def _verifyLogFile(file=None):
    ''' verifies if path to desired logfile exists before logging starts '''
    filename = file

    if not filename:
        filename = DEFAULT_LOG_FILE
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    return filename

class LocationService:

    def __init__(self):
        self.clientele = Clientele()


class Clientele:

    def __init__(self):
        self._client_list = []
        pass


class Client:

    def __init__(self, info=None):
        if type(info) is dict:
            self._dict_to_client(info)
        else:
            # todo log error
            raise TypeError

    def _dict_to_client(self, info):
        self.name = info['name']
        self.phone_number = info['phone_number']
        self.raw_address = Location(info)


class Location:

    def __init__(self, info=None):
        if type(info) is dict:
            self._dict_to_address(info)
        else:
            # todo log error
            raise TypeError

    def _dict_to_address(self, info):
        self.address = info['address']
        self.city = info['city']
        self.state = info['state']
        self.zip = info['zip']

    def __str__(self):
        return self.address + ' ' + self.city + ', ' + self.state + ' ' + self.zip


class GeocodeService:

    def __init__(self):
        pass


class GoogleGCService:

    def __init__(self):
        pass


if __name__ == '__main__':
    main()
