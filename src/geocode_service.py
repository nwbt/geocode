#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: geocode_service Project: geocode
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import googlemaps.places
import googlemaps.client
import logging


class GeocodeService:

    def __init__(self):
        pass

class GoogleGeocodeService(GeocodeService):

    def __init__(self, api_key=None, store_list=None):
        GeocodeService.__init__(self)
        if api_key:
            self.api_key = api_key
        if store_list:
            self.list_of_clients = store_list


    @property
    def google_client(self):
        return self._google_client

    @google_client.setter
    def google_client(self, google_client):
        if type(google_client) is googlemaps.client.Client:
            self._google_client = google_client
        else:
            raise TypeError

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        self.google_client = googlemaps.client.Client(key=api_key)

    def geocode_addresses(self):
        for idx, store in enumerate(self.list_of_clients):

            try:
                query = store.store_name + ' ' + str(store.address_from_csv)
                response = self._get_place(query)
                self._handle_place_response(response, store)

            except ValueError as ex:
                print(ex)

            # query = str(store.address_from_csv)
            # geocode_response = self._get_geocode(query)
            # response_length = len(geocode_response)
            # if response_length < 1:
            #     logging.error('response empty, address=' + str(store.address_from_csv))
            # elif response_length == 1:
            #     self._sort_response(store, geocode_response[0])
            # else:
            #     logging.warning('ambiguous request, multiple responses, address:' + str(store.address_from_csv))
            #     for i in geocode_response:
            #         logging.warning(str(i))
        # todo look for duplicates and filter and map these results functionally

    def _get_geocode(self, address):
        try:
            return googlemaps.geocoding.geocode(self.google_client, address=address)
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _get_place(self, query):
        try:
            response = googlemaps.places.places(client=self._google_client, query=query)
            if len(response) < 1:
                raise ValueError
            return response
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _handle_place_response(self, response, store):
        store.google_address = response['results'][0]['formatted_address']
        store.google_name = response['results'][0]['name']
        store.google_geocode = response['results'][0]['geometry']['location']
        store.google_placeid = response['results'][0]['id']


    def _sort_response(self, store, response):
        # todo verify dict has values, log if not
        store.address_from_google = response['formatted_address']
        store.geocode = response['geometry']['location']
        store.place_id = response['place_id']

