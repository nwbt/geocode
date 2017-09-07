#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

import os
from setuptools import setup

setup(
    name='geocode_csv',
    version='0.2',
    description='geocode addresses in csv using google place api',
    author='Dan Catalano',
    author_email='dev@nwbt.co',
    url='https://www.nwbt.co',
    install_requires=[
        'googlemaps',
    ]
)
