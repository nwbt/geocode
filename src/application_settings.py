#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: application_settings Project: geocode
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import logging
import sys
import os

DEFAULT_LOG_LEVEL = 'WARNING'
DEFAULT_LOG_FILE = 'logs/geocode.log'
DEFAULT_LOG_MSG = '%(asctime)s|%(levelname)s|%(message)s'


class ApplicationSettings:
    def __init__(self):
        self.log_level = None
        self.log_file = None
        self.input_file = None
        self.output_file = None
        self.api_key = None

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
                    print('ERROR: could not create logfile, permission denied', file=sys.stderr)
