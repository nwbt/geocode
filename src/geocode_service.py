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
import googlemaps.exceptions
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
        self.clients_w_response = list()
        place_ids = set()

        for store in self.list_of_clients:
            try:
                query = store.csv_name + ' ' + str(store.csv_address)
                response = self._get_places(query)
                logging.debug('response: ' + str(response))

                if response and response['status'] == 'OK':
                    logging.info('response status OK')

                    results = response['results']
                    logging.debug(str(results))
                    results_length = len(results)

                    if results_length == 1:
                        result = results[0]
                        self._handle_result(place_ids, query, result, store)

                    elif results_length > 1:
                        logging.info('ambiguous response')
                        logging.info('csv_name + csv_address: ' + query)

                        print('\ncsv_name + csv_address:\n\t1) ' + str(store.csv_name) + ' | ' + str(store.csv_address))
                        print('\ngoogle_name + google_addresses: ')

                        # TODO do for loop below functionally and conditionally
                        for index, result in enumerate(results):
                            print('\t' + str(index+1) + ') ' + results[index]['name'] + ' | ' + results[index]['formatted_address'])
                            logging.info(str(index+1) + ') google_address: ' + str(result))

                        idx_selected = self._handle_ambiguous_results(results_length)

                        if idx_selected >= 0 and idx_selected < results_length:
                            result = results[idx_selected]
                            self._handle_result(place_ids, query, result, store)

                        else: # TODO allow manual search here
                            self._remove_from_list(query=query, level=logging.INFO, reason='result ambiguous and none selected')

                    else:
                        self._remove_from_list(query=query, level=logging.ERROR, reason='response status OK but zero results')

                elif not response or response['status'] == 'ZERO_RESULTS': # TODO allow manual search here
                    self._remove_from_list(query=query, reason='response status ZERO_RESULTS, no match')

                else:
                    self._remove_from_list(query=query, level=logging.ERROR, reason='response status unknown')

            except Exception as ex:
                self._remove_from_list(level=logging.ERROR, reason='unknown error during API request/response', exception=ex)

        return self.clients_w_response

    def _handle_result(self, place_ids, query, result, store):
        logging.info('csv_name + csv_address:\t\t ' + query)
        logging.info('google_name + google_address:\t ' + result['name'] + ' ' + result['formatted_address'])

        if self._is_duplicate(place_ids, query, result):
            self._remove_from_list(query=query, reason="duplicate", store=store)
        elif self._is_closed(result):
            self._remove_from_list(query=query, reason="permanently closed", store=store)
        else:
            self._handle_places_result(result, store)
            response = self._get_place_details(store.place_id)
            self._handle_place_details_result(response['result'], store)
            place_ids.add(store.place_id)
            self.clients_w_response.append(store)

    def _is_closed(self, result):
        if 'permanently_closed' in result and result['permanently_closed'] is True:
            return True
        else:
            return False

    # def _remove_from_list(self, idx, store=None, level=logging.WARNING, reason='', query='', exception=None):
    def _remove_from_list(self, level=logging.WARNING, **kwargs):
        logging.log(level, msg='reason: ' + kwargs.get('reason', '') + '|' + 'query: ' + kwargs.get('query', '')
                               + '|' + str(kwargs.get('exception', '')))

        f = open('output/stores_not_added.log', 'a', newline='\n')
        store = kwargs.get('store')
        if store:
            f.write(store.csv_name + ' | ' + str(store.csv_address) + ' | ' + kwargs.get('reason', '') + '\n')
        else:
            f.write(kwargs.get('query', '') + ' | ' + kwargs.get('reason', '') + '\n')
        f.close()

    def _handle_ambiguous_results(self, results_length):
        while True:
            selected = input("Select index of desired response (use 0 for none): ")
            try:
                selected = int(selected)
                selected = selected - 1
                if selected >= results_length or selected < -1:
                    logging.warning('selected result ' + str(selected) + 'outside array\'s bounds')
                else:
                    return selected
            except ValueError as ex:
                logging.warning(ex)

    def _is_duplicate(self, placeids, query, result):
        if result['place_id'] in placeids:
            logging.info('duplicate entry: ' + query)
            return True
        else:
            return False

    def _get_place_details(self, place_id):
        try:
            response = googlemaps.places.place(client=self.google_client, place_id=place_id)
            if not response or len(response) < 1:
                raise ValueError
            return response
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _get_places(self, query):
        type = 'establishment'
        try:
            response = googlemaps.places.places(client=self.google_client, query=query, type=type)
            if not response or len(response) < 1:
                raise ValueError
            return response
        except googlemaps.exceptions.TransportError as ex:
            logging.error(ex)
        except googlemaps.exceptions.ApiError as ex:
            logging.critical(ex)
            raise ex

    def _handle_place_details_result(self, result, store):
        store.url = result.get('url', None)
        store.website = result.get('website', None)
        store.adr_address = result.get('adr_address', None)
        store.formatted_phone_number = result.get('formatted_phone_number', None)

    def _handle_places_result(self, result, store):
        store.formatted_address = result.get('formatted_address', None)
        store.name    = result.get('name', None)
        store.location = result.get('geometry', None).get('location', None)
        store.place_id = result.get('place_id')

