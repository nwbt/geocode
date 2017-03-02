#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: address Project: geocode
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import logging
import collections


class Address:
    def __init__(self, address_dict=None):
        self.street_address_1 = None
        self.street_address_2 = None
        self.city = None
        self.state = None
        self.zip = None

        if type(address_dict) is collections.OrderedDict:
            self._dict_to_address(address_dict)

        elif address_dict is not None:
            logging.error('address_dict not of type OrderedDict' + str(address_dict))
            raise TypeError

    def _dict_to_address(self, address_dict):
        l_city = address_dict['city']
        l_zip = address_dict['zip']

        if not l_city and not l_zip:
            logging.error('address should have city and/or zip')
            raise ValueError

        self.street_address_1 = address_dict['address_1']
        self.street_address_2 = address_dict['address_2']
        self.state = address_dict['state']
        self.city = l_city
        self.zip = l_zip

    def to_dict(self):
        return {
            'street_address_1': self.street_address_1,
            'street_address_2': self.street_address_2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }

    def __str__(self):
        # todo cleanup
        address =  self.street_address_1 if self.street_address_1 is not None else ''
        address += self.street_address_2 if self.street_address_2 is not None else ''
        address += self.city if self.city is not None else ''
        address += self.state if self.state is not None else ''
        address += self.zip if self.zip is not None else ''
        return address
