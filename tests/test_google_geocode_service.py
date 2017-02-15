#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

import unittest
import os
import googlemaps

from src.geocode import GoogleGeocodeService


def setUpModule():
    pass


def tearDownModule():
    pass


class ClassGoogleGeocodeServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.apikey = os.environ['GOOGLE_GEOCODE_API']
        self.client_address = '1600 Pennsylvania Ave NW, Washington, DC 20500'

    def tearDown(self):
        pass

    def test_valid_api_key(self):
        # arrange
        ggs = GoogleGeocodeService()
        ggs.api_key = self.apikey
        exception = None

        # act
        try:
            ggs.geocode_address(self.client_address)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsNone(exception, 'no exception should have occured')

    def test_invalid_api_key(self):
        # arrange
        ggs = GoogleGeocodeService()
        ggs.api_key = self.apikey[:-1] + 'z'
        exception = None

        # act
        try:
            ggs.geocode_address(self.client_address)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsInstance(exception, googlemaps.exceptions.ApiError, 'invalid api key should cause apierror exception')

    def test_response(self):
        # arrange
        expected_location_geometry = {'lat': 38.89767579999999, 'lng': -77.0364823}
        expected_formatted_address = '1600 Pennsylvania Ave NW, Washington, DC 20500, USA'
        ggs = GoogleGeocodeService()
        ggs.api_key = self.apikey

        # act
        response = ggs.geocode_address(self.client_address)

        # assert
        self.assertEqual(response[0]['geometry']['location'], expected_location_geometry, '')
        self.assertEqual(response[0]['formatted_address'], expected_formatted_address, '')

    def test(self):
        # arrange

        # act

        # assert
        self.assertFalse(True)
