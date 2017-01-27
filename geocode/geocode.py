#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import argparse


def main():
    cli = CommandLineInput();


class CommandLineInput:
    pass


class LocationService:

    def __init__(self):
        self.clientele = Clientele()


class Clientele:

    def __init__(self):
        self._client_list = []
        pass


class Client:

    def __init__(self, info=None):
        if type(info) is dict:
            self._dict_to_client(info)
        else:
            # todo log error
            raise TypeError

    def _dict_to_client(self, info):
        self.name = info['name']
        self.phone_number = info['phone_number']
        self.raw_address = Location(info)


class Location:

    def __init__(self, info=None):
        if type(info) is dict:
            self._dict_to_address(info)
        else:
            # todo log error
            raise TypeError

    def _dict_to_address(self, info):
        self.address = info['address']
        self.city = info['city']
        self.state = info['state']
        self.zip = info['zip']

    def __str__(self):
        return self.address + ' ' + self.city + ', ' + self.state + ' ' + self.zip


class GeocodeService:

    def __init__(self):
        pass


class GoogleGCService:

    def __init__(self):
        pass


if __name__ == '__main__':
    main()
