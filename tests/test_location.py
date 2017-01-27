#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

from geocode.geocode import Location
import unittest
from unittest.mock import MagicMock


def setUpModule():
    pass


def tearDownModule():
    pass


class LocationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.address = '223 W 38th St'
        cls.city = 'New York'
        cls.state = 'NY'
        cls.zip = '10018'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.location_object = None
        self.exception = None

    def tearDown(self):
        pass

    def test_location_constructor_no_args(self):
        try:
            self.location_object = Location()
        except Exception as e:
            self.exception = e

        self.assertIsInstance(self.exception, TypeError, 'Nonexistent dict should have returned TypeError')
        self.assertIsNone(self.location_object, 'Exception, in contructor, should have prevented object creation')

    def test_location_constructor_invalid_dict(self):
        invalid_dict = {}
        try:
            self.location_object = Location(invalid_dict)
        except Exception as e:
            self.exception = e

        self.assertIsInstance(self.exception, KeyError, 'Invalid dict should have returned KeyError')
        self.assertIsNone(self.location_object, 'Exception, in constructor, should have prevented object creation')

    def test_location_constructor_with_valid_object(self):
        location_dict = { 'address':self.address, 'city':self.city, 'state':self.state, 'zip':self.zip }

        try:
            self.location_object = Location(location_dict)
        except Exception as e:
            self.exception = e

        self.assertIsNone(self.exception, 'exception should not have occurred, ' + str(self.exception))
        self.assertIsNotNone(self.location_object)
        self.assertEqual(self.location_object.address, self.address, 'addresses are not the same')
        self.assertEqual(self.location_object.city, self.city, 'cities are not equal')
        self.assertEqual(self.location_object.state, self.state, 'states are not equal')
        self.assertEqual(self.location_object.zip, self.zip, 'zip codes are not equal')

    def test_location_str_method(self):
        location_dict = { 'address':self.address, 'city':self.city, 'state':self.state, 'zip':self.zip }

        try:
            self.location_object = Location(location_dict)
        except Exception as e:
            self.exception = e

        self.assertIsNone(self.exception, 'exception should not have occurred, ' + str(self.exception))

        expected_address_string = self.address + ' ' + self.city + ', ' + self.state + ' ' + self.zip
        raw_address_string = str(self.location_object)

        self.assertEqual(raw_address_string, expected_address_string, 'address strings are not the same')
