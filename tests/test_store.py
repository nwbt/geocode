#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

import unittest
import collections

from src.geocode import Address
from src.geocode import Store


def setUpModule():
    pass


def tearDownModule():
    pass


class ClassStoreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.store_dict = {
            'address_1': '1600 Pennsylvania Ave NW',
            'address_2': '',
            'city': 'Washington',
            'state': 'DC',
            'zip': '20500',
            'store_name': 'White House',
            'phone': '202-456-1111',
        }
        # 1600 Pennsylvania Ave NW, Washington, DC 20500, USA

        pass

    def tearDown(self):
        pass

    def test_correctly_arranged_store(self):
        # arrange
        ordered_store_dict = collections.OrderedDict(self.store_dict)

        # act
        store = Store(ordered_store_dict)
        address = Address(ordered_store_dict)

        # assert
        self.assertEqual(store.csv_name, self.store_dict['store_name'], 'store name strings are not equal')
        self.assertEqual(store.csv_phone, self.store_dict['phone'], 'phone number are not equal')
        self.assertEqual(str(store.csv_address), str(address), 'addresses are not the same')

    def test_plain_dict_raises_type_error(self):
        # arrange
        exception = None
        # act
        try:
            store = Store(self.store_dict)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsInstance(exception, TypeError, 'type not TypeError')

    def test_to_dict_method(self):
        # arrange
        ordered_store_dict = collections.OrderedDict(self.store_dict)
        address_dict = Address().to_dict()
        expected_store_dict = {
            'store_name': self.store_dict['store_name'],
            'phone_number': self.store_dict['phone'],
            'address_components' : address_dict,
            'geocode': None,
            'google_address': None,
        }

        # act
        store = Store(ordered_store_dict)
        store.csv_address = Address()
        actual_store_dict = store.to_dict()

        # asset
        self.assertEqual(actual_store_dict, expected_store_dict, 'store dicts are not the same')
