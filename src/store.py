#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: store Project: geocode
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import logging
import collections

from src.address import Address


class Store:
    def __init__(self, store_dict=None):
        self.csv_address = None
        self.csv_phone = None
        self.csv_name = None

        # value from google place api
        self.name = None
        self.formatted_address = None
        self.location = None
        self.place_id = None
        self.formatted_phone_number = None
        self.adr_address = None
        self.url = None
        self.website = None
        self.city = None

        if type(store_dict) is collections.OrderedDict:
            self._dict_to_store(store_dict)
        elif store_dict is None:
            self.csv_address = Address()
        else:
            logging.error('client_dict not of type OrderedDict' + str(store_dict))
            raise TypeError

    def _dict_to_store(self, store_dict):
        self.csv_name = store_dict['store_name']
        self.csv_phone = store_dict['phone']
        self.csv_address = Address(store_dict)

    def to_dict(self):
        return {
            'name': self.name,
            'formatted_address': self.formatted_address,
            'adr_address': self.adr_address,
            'location': self.location,
            'url': self.url,
            'website': self.website,
            'formatted_phone_number': self.formatted_phone_number,
            'city': self.city,
            # 'place_id': self.place_id
        }

    def __lt__(self, other):
        if type(other) is not Store:
            logging.error('comparison not possible b/c other not of type Store')
            raise TypeError

        return self.place_id < other.google_placeid

    def __eq__(self, other):
        if type(other) is not Store:
            logging.error('comparison not possible b/c other not of type Store')
            raise TypeError

        return self.place_id == other.google_placeid
