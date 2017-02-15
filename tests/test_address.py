#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import collections
import unittest

from src.geocode import Address


def setUpModule():
    pass


def tearDownModule():
    pass


class ClassAddressTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.address_dict = {
            'address_1': '1600 Pennsylvania Ave NW',
            'address_2': '',
            'city': 'Washington',
            'state': 'DC',
            'zip': '20500',
        }
        # 1600 Pennsylvania Ave NW, Washington, DC 20500, USA

        self.canadian_address = {
            'address_1': '721 Government Street',
            'address_2': '',
            'city': 'Victoria',
            'state': 'British Columbia',
            'zip': 'V8W 1W5',
        }
        # 721 Government Street Victoria, British Columbia V8W 1W5

    def tearDown(self):
        pass

    def test_correctly_formatted_address(self):
        # arrange
        ordered_address_dict = collections.OrderedDict(self.address_dict)

        # act
        address = Address(ordered_address_dict)

        # assert
        self.assertEqual(self.address_dict['address_1'], address.street_address_1, 'strings not equal')
        self.assertEqual(self.address_dict['address_2'], address.street_address_2, 'strings not equal')
        self.assertEqual(self.address_dict['city'], address.city, 'strings not equal')
        self.assertEqual(self.address_dict['state'], address.state, 'strings not equal')
        self.assertEqual(self.address_dict['zip'], address.zip, 'strings not equal')

    def test_canadian_address(self):
        # arrange
        ordered_address_dict = collections.OrderedDict(self.canadian_address)

        # act
        address = Address(ordered_address_dict)

        # assert
        self.assertEqual(self.canadian_address['address_1'], address.street_address_1, 'strings not equal')
        self.assertEqual(self.canadian_address['address_2'], address.street_address_2, 'strings not equal')
        self.assertEqual(self.canadian_address['city'], address.city, 'strings not equal')
        self.assertEqual(self.canadian_address['state'], address.state, 'strings not equal')
        self.assertEqual(self.canadian_address['zip'], address.zip, 'strings not equal')

    def test_missing_key_raises_key_error(self):
        # arrange
        exception = None
        address = None
        self.address_dict.pop('address_2')
        ordered_address_dict = collections.OrderedDict(self.address_dict)

        # act
        try:
            address = Address(ordered_address_dict)
        except Exception as ex:
           exception = ex

        # assert
        self.assertIsInstance(exception, KeyError, 'type not KeyError')


    def test_city_and_zip_values_both_empty_raises_value_error(self):
        # arrange
        exception = None
        address = None
        self.address_dict['city'] = ''
        self.address_dict['zip'] = ''
        ordered_address_dict = collections.OrderedDict(self.address_dict)

        # act
        try:
            address = Address(ordered_address_dict)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsInstance(exception, ValueError, 'type not ValueError')

    def test_plain_dict_raises_type_error(self):
        # arrange
        exception = None
        address = None

        # act
        try:
            address = Address(self.address_dict)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsInstance(exception, TypeError, 'type not TypeError')

    def test_to_dict_method(self):
        # arrange
        ordered_address_dict = collections.OrderedDict(self.address_dict)
        expected_address_dict = {
            'street_address_1': self.address_dict['address_1'],
            'street_address_2': self.address_dict['address_2'],
            'city': self.address_dict['city'],
            'state': self.address_dict['state'],
            'zip': self.address_dict['zip'],
        }

        # act
        address = Address(ordered_address_dict)
        actual_address_dict = address.to_dict()

        # assert
        self.assertEqual(actual_address_dict, expected_address_dict, 'address dicts are not the same')

    def test__str__method(self):
        # arrange
        ordered_address_dict = collections.OrderedDict(self.address_dict)
        expected_address_str = self.address_dict['address_1'] + ' ' \
                               + self.address_dict['address_2'] + ' ' \
                               + self.address_dict['city'] + ', ' \
                               + self.address_dict['state'] + ' ' \
                               + self.address_dict['zip']

        # act
        address = Address(ordered_address_dict)
        actual_address_str = str(address)

        # assert
        self.assertEqual(actual_address_str, expected_address_str, 'address strings are not the same')

