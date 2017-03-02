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
        self.google_name = None
        self.google_address = None
        self.google_geocode = None
        self.google_placeid = None

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
            'csv_address': self.csv_address.to_dict(),
            'csv_name': self.csv_name,
            'csv_phone': self.csv_phone,
            'google_address': self.google_address,
            'google_geocode': self.google_geocode,
            'google_name': self.google_name,
            'google_placeid': self.google_placeid
        }

    def __lt__(self, other):
        if type(other) is not Store:
            logging.error('comparison not possible b/c other not of type Store')
            raise TypeError

        return self.google_placeid < other.google_placeid

    def __eq__(self, other):
        if type(other) is not Store:
            logging.error('comparison not possible b/c other not of type Store')
            raise TypeError

        return self.google_placeid == other.google_placeid
