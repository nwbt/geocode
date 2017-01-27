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
        cls.address = '223 W 38th St'
        cls.city = 'New York'
        cls.state = 'NY'
        cls.zip = '10018'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.empty_object = None
        self.exception = None

    def tearDown(self):
        pass

    def test_client_constructor_no_args(self):

        try:
            self.empty_object = Client()
        except TypeError as te:
            self.exception = te

        self.assertIsInstance(self.exception, TypeError, 'Nonexistent dict should have returned TypeError')
        self.assertIsNone(self.empty_object, 'Exception, in constructor, should have prevented object creation')

    def test_client_constructor_invalid_dict(self):

        empty_dict = {}
        try:
            self.empty_object = Client(empty_dict)
        except KeyError as ke:
            self.exception = ke

        self.assertIsInstance(self.exception, KeyError, 'Invalid dict should have returned KeyError')
        self.assertIsNone(self.empty_object, 'Exception, in constructor, should have prevented object creation')

    def test_client_constructor_with_valid_dict(self):

        self.client_dict = {
            'name': self.name, 'phone_number':self.phone_number, 'address':MagicMock(), 'city':MagicMock(),
            'state':MagicMock(), 'zip':MagicMock()
                            }
        client = None
        try:
            client = Client(self.client_dict)
        except Exception as e:
            pass
        self.assertIsNotNone(client)
        self.assertEqual(client.name, self.name, 'names are not the same')
        self.assertEqual(client.phone_number, self.phone_number, 'phone_numbers are not equal')

