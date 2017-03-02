#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

import unittest
import os
import googlemaps.places
import googlemaps.client
import googlemaps.geocoding

from src.store import Store
from src.address import Address
from src import geocode_service


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
        ggs = geocode_service.GoogleGeocodeService()
        ggs.api_key = self.apikey
        exception = None

        # act
        try:
            ggs._get_geocode(self.client_address)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsNone(exception, 'no exception should have occured')

    def test_invalid_api_key(self):
        # arrange
        ggs = geocode_service.GoogleGeocodeService()
        ggs.api_key = self.apikey[:-1] + 'z'
        exception = None

        # act
        try:
            ggs._get_geocode(self.client_address)
        except Exception as ex:
            exception = ex

        # assert
        self.assertIsInstance(exception, googlemaps.exceptions.ApiError, 'invalid api key should cause apierror exception')

    def test_response(self):
        # arrange
        expected_location_geometry = {'lat': 38.89767579999999, 'lng': -77.0364823}
        expected_formatted_address = '1600 Pennsylvania Ave NW, Washington, DC 20500, USA'
        ggs = geocode_service.GoogleGeocodeService()
        ggs.api_key = self.apikey

        # act
        response = ggs._get_geocode(self.client_address)

        # assert
        self.assertEqual(response[0]['geometry']['location'], expected_location_geometry, '')
        self.assertEqual(response[0]['formatted_address'], expected_formatted_address, '')

    def test_place_api(self):
        # arrange
        store_address_02 = 'Bear 125 E Woodin Ave Chelan, WA 98816'
        store_address_01 = 'Bear Foods Wholesale 125 E Woodin Ave Chelan, WA 98817'

        # act
        client = googlemaps.client.Client(key=self.apikey, queries_per_second=10)
        p1 = googlemaps.places.places(client=client, query=store_address_01)
        print(store_address_01)
        print(p1.keys())
        # print('html_attributions: ' + str(p1['html_attributions']))
        # print('results: ' + str(p1['results'].keys()))
        for i in p1['results']:
            print(i.keys())
            print('name: ' + i['name'])
            print('geometry: ' + str(i['geometry']))
            print('id: ' + i['id'])
        print('results: ' + str(p1['results']))
        print('status:' + str(p1['status']))
        print(p1)

        # assert
        self.assertFalse(True)

    def test_store_permanently_closed(self):
        # arrange
        ggs = geocode_service.GoogleGeocodeService()
        # Sprouts 2502 Nacogdoches Rd.  San Antonio, TX
        address = Address()
        store = Store()
        store.csv_address = address

        closed_store_result = {'formatted_address': '2502 Nacogdoches Rd, San Antonio, TX 78217, United States', 'geometry': {'location': {'lat': 29.5178257, 'lng': -98.44925669999999}, 'viewport': {'northeast': {'lat': 29.51936563029149, 'lng': -98.44824016970848}, 'southwest': {'lat': 29.51666766970849, 'lng': -98.4509381302915}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '05184076b8241e2fc394f3890476358f70333be4', 'name': 'Sprouts Farmers Market - CLOSED', 'permanently_closed': True, 'photos': [{'height': 800, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111424993908416676078/photos">Sprouts Farmers Market - CLOSED</a>'], 'photo_reference': 'CoQBdwAAAKgYVcbfc312hOUfSCuf7TnYmjUl3BcJzlaTg5tQxjo7L_MvU_9w8cbNY9hwxK1dspcha6-oZHaAI8vgVC0hz8f3A5tc9a84sNP2_c4S5xK_Ug73PduNmQS96BLjR-muDVjFZbVWIuXfl8E4A8UddeUYqNLNzxDzBmeEAZblaOUeEhD-hFE0E1ay3pYMdMsmaY1pGhTebaUcCC50_W3FNVWSuW0zlVfobw', 'width': 1200}], 'place_id': 'ChIJu-eiDy31XIYRH62uZk9Q5PE', 'rating': 4.6, 'reference': 'CmRSAAAA9kWUF4PU3ktS0GjUiy-2l-QFXfucnG70dB2G0FIPvXWbTgi5ARxero3bUGzJhtr_WoaeBUcqv9bbc8UnDIwEQRF24z89z7kQpebdzLP2fjZ1CgA63RvXFM5Hh4oDKeCDEhBS9VJX5VfXwGpST_wVsQSbGhT59jKhrw5--KSyyGftH83PKtppLQ', 'types': ['grocery_or_supermarket', 'health', 'food', 'store', 'point_of_interest', 'establishment']}
        # act

        ggs._handle_places_response(closed_store_result, store)

        # assert
        self.assertIsNone(store.google_address, 'error')
        self.assertIsNone(store.google_name, 'error')
        self.assertIsNone(store.google_geocode, 'error')
        self.assertIsNone(store.google_placeid, 'error')

    def test1(self):
        # arrange
        # todo test multiple response with the following string
        # will require understanding how to unittest input command
        # 'New Leaf - Downtown 1134 Pacific Ave  Santa Cruz, CA 95060'

        # act

        # assert
        self.assertFalse(True)
