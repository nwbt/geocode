#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
from geocode.geocode import Client
import unittest
from unittest.mock import MagicMock

def setUpModule():
    pass


def tearDownModule():
    pass


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.name = 'store'
        cls.phone_number = '212-555-1212'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client_object = None
        self.exception = None

    def tearDown(self):
        pass

    def test_client_constructor_no_args(self):
        # todo split into multiple tests
        try:
            self.client_object = Client()
        except Exception as e:
            self.exception = e

        self.assertIsInstance(self.exception, TypeError, 'Nonexistent dict should have returned TypeError')
        self.assertIsNone(self.client_object, 'Exception, in constructor, should have prevented object creation')

    def test_client_constructor_invalid_dict(self):
        # todo split into multiple tests
        invalid_dict = {}
        try:
            self.client_object = Client(invalid_dict)
        except Exception as e:
            self.exception = e

        self.assertIsInstance(self.exception, KeyError, 'Invalid dict should have returned KeyError')
        self.assertIsNone(self.client_object, 'Exception, in constructor, should have prevented object creation')

    def test_client_constructor_with_valid_dict(self):
        # todo split into multiple tests
        client_dict = {
            'name': self.name, 'phone_number':self.phone_number, 'address':MagicMock(), 'city':MagicMock(),
            'state':MagicMock(), 'zip':MagicMock()
                            }
        try:
            self.client_object = Client(client_dict)
        except Exception as e:
            self.exception = e

        self.assertIsNone(self.exception, 'exception should not have occurred, ' + str(self.exception))
        self.assertIsNotNone(self.client_object)
        self.assertEqual(self.client_object.name, self.name, 'names are not the same')
        self.assertEqual(self.client_object.phone_number, self.phone_number, 'phone_numbers are not equal')

