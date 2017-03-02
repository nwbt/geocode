#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import unittest

from src.clientele import Clientele
from src.store import Store


def setUpModule():
    pass


def tearDownModule():
    pass


class ClassClienteleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.clientele = Clientele()

    def tearDown(self):
        self.clientele = None

    def test_1(self):
        """ """

        # arrange
        print(hex(id(self.clientele)))
        clients = self.clientele.client_list
        print(hex(id(clients)))

        store1 = Store()
        store2 = Store()
        store3 = Store()

        store2.google_placeid = store1.google_placeid = 'ChIJawlhKwWbm1QR6vt0assdQKw'
        store3.google_placeid = '99fb064f2e56c0acd9cbecca555518d638c7dbb2'

        # act
        clients.append(store1)
        clients.append(store2)
        clients.append(store3)

        original_length = len(self.clientele.client_list)

        self.clientele.eliminate_duplicates()

        updated_length = len(self.clientele.client_list)

        # assert
        self.assertLess(updated_length, original_length, 'duplicate removal failed')

    def test_2(self):
        """ """

        # arrange
        print(hex(id(self.clientele)))
        clients = self.clientele.client_list
        print(hex(id(clients)))

        store1 = Store()
        store2 = Store()

        store1.google_placeid = '99fb064f2e56c0acd9cbecca555518d638c7dbb2'

        # act
        clients.append(store1)
        clients.append(store2)

        original_length = len(self.clientele.client_list)

        self.clientele.eliminate_duplicates()

        updated_length = len(self.clientele.client_list)

        # assert
        self.assertLess(updated_length, original_length, 'empty placeid removal failed')
