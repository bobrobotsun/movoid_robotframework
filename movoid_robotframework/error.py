#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : error
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/13 12:16
# Description   : 
"""


class RfError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.args = args
        self.kwargs = kwargs

    def get(self, name, default=None):
        return self.kwargs.get(name, default)

    def __getitem__(self, item):
        return self.kwargs[item]
