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
import googlemaps.geocoding
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
                query = store.csv_name + ' ' + str(store.csv_address)
                response = self._get_place(query)
                logging.debug('response: ' + str(response))

                if response and response['status'] == 'OK':
                    logging.info('response status OK')

                    results = response['results']
                    results_length = len(results)

                    if results_length == 1:
                        logging.debug(str(results[0]))
                        logging.info('csv_name + csv_address:\t\t ' + query)
                        logging.info('google_name + google_address:\t ' + results[0]['name'] + ' '+ results[0]['formatted_address'])
                        self._handle_place_response(results[0], store)

                    elif results_length > 1:
                        logging.info('ambiguous response')
                        logging.info('csv_name + csv_address: ' + query)

                        # TODO do for loop below functionally and conditionally
                        print('csv_name + csv_address: ' + query)
                        print('google_name + google_addresses: ')
                        for index, result in enumerate(results): # TODO display to console
                            print('\t' + str(index+1) + ') ' + str(result))
                            logging.info(str(index + 1) + 'google_address: ' + str(result))

                        idx_selected = self._handle_ambiguous_results(results_length)

                        if idx_selected >= 0 and idx_selected < results_length:
                            logging.info('csv_name + csv_address:\t\t ' + query)
                            logging.info('google_name + google_address:\t ' + results[idx_selected]['name'] + ' '+ results[idx_selected]['formatted_address'])
                            self._handle_place_response(results[idx_selected], store)
                        else:
                            # TODO determine which line in CSV file is not place-able
                            logging.warning('no result selected for address: ' + str(query))

                    else:
                        logging.error('response with status OK should have results larger than zero')

                elif not response or response['status'] == 'ZERO_RESULTS':
                    logging.warning('empty response - no match for address: ' + query)

                else:
                    logging.error('response unknown')

            except Exception as ex:
                logging.error('exception unknown in geocode_addresses' + str(ex))

    def _handle_ambiguous_results(self, results_length):
        while True:
            selected = input("Select index of desired response (use 0 for none): ")
            try:
                selected = int(selected)
                selected = selected - 1
                if selected >= results_length:
                    logging.warning('selected result ' + str(selected) + 'outside array\'s bounds')
                else:
                    return selected
            except ValueError as ex:
                logging.warning(ex)

    def _get_geocode(self, address):
        try:
            return googlemaps.geocoding.geocode(self.google_client, address=address)
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _get_place(self, query):
        type = 'establishment'
        try:
            response = googlemaps.places.places(client=self._google_client, query=query, type=type)
            if len(response) < 1:
                raise ValueError
            return response
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _get_place_details(self, placeid):
        pass # TODO implement

    def _handle_place_response(self, result, store):
        store.google_address = result['formatted_address']
        store.google_name    = result['name']
        store.google_geocode = result['geometry']['location']
        store.google_placeid = result['id']

    def _sort_response(self, store, response):
        # todo verify dict has values, log if not
        store.google_address = response['formatted_address']
        store.google_geocode = response['geometry']['location']
        store.google_placeid = response['place_id']

