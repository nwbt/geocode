#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: clientele Project: geocode
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import logging

from src.store import Store

class Clientele:
    def __init__(self):
        self.client_list = []

    def add_client(self, client_dict):
        try:
            client = Store(client_dict)
            self.client_list.append(client)
        except Exception as e:
            print(str(e))
            logging.error(e)

    def to_list_of_dicts(self):
        clientele_json = []
        for i in self.client_list:
            clientele_json.append(i.to_dict())
        return clientele_json

    def eliminate_duplicates(self):
        logging.info('client_list len: ' + str(len(self.client_list)))
        refined_list = self._eliminate_empty_placeid()

        logging.info('refined_list len: ' + str(len(refined_list)) + ', after removing empty placeid')
        unique_list = list(sorted(uniq(refined_list)))

        logging.info('unique_list len:' + str(len(unique_list)) + ', after removing duplicates')
        self.client_list = unique_list

    def _eliminate_empty_placeid(self):
        return list(filter(lambda x: x.google_placeid is not None, self.client_list))


def uniq(lst):
    last = Store()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item
