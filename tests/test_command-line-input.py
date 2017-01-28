#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import argparse
import unittest.mock
import os
import sys
import logging

from geocode import geocode
from geocode.geocode import CommandLineInput

def setUpModule():
    pass

def tearDownModule():
    pass


class CommandLineInputTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.default_api_key='resources/secrets'
        cls.default_input_file='resources/stores.csv'
        cls.default_output_file='resources/stores.json'
        cls.default_log_file=None
        cls.default_log_level=None

        cls.noArgsNamespace = argparse.Namespace(
            api_key=cls.default_api_key,
            input_file=cls.default_input_file,
            log_file=cls.default_log_file,
            log_level=cls.default_log_level,
            output_file=cls.default_output_file,
        )

        cls.argsNamespace = argparse.Namespace(
            api_key='key',
            input_file='in',
            log_file='file',
            log_level='level',
            output_file='out'
        )

        cls.emptyArgs = [
            os.path.abspath(geocode.__file__)
        ]
        cls.fullArgs = [
            os.path.abspath(geocode.__file__),
            '-i', 'in',
            '-o', 'out',
            '-k', 'key',
            '-l', 'level',
            '-f', 'file',
        ]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        sys.argv = None

    def tearDown(self):
        pass

    def test_default_values(self):
        sys.argv = self.emptyArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(args, self.noArgsNamespace, 'not equal')

    def test_defined_values(self):
        sys.argv = self.fullArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(args, self.argsNamespace, 'not equal')

    def test_log_file_no_args(self):
        sys.argv = self.emptyArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(geocode._verifyLogFile(args.log_file), geocode.DEFAULT_LOG_FILE,
                                                'log file does not match default value')

    def test_log_level_no_args(self):
        sys.argv = self.emptyArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(geocode._verifyLogLevel(args.log_level), logging.WARNING,
                                                'log level does not match default value')

    def test_log_level_invalid_args(self):
        sys.argv = self.fullArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(geocode._verifyLogLevel(args.log_level), logging.WARNING,
                         'log level does not match default value')

    def test_log_level_valid_args(self):
        self.fullArgs[self.fullArgs.index('level')] = 'debug'
        sys.argv = self.fullArgs
        args = geocode._build_argument_list(argparse.ArgumentParser())
        self.assertEqual(geocode._verifyLogLevel(args.log_level), logging.DEBUG,
                         'log level does not match default value')




