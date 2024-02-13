#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : log
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/3 14:57
# Description   : 
"""
from .version import VERSION

if VERSION:
    from robot.api import logger


class BasicLog:

    def __init__(self):
        pass

    if VERSION:
        print_function = {
            'DEBUG': logger.debug,
            'INFO': logger.info,
            'WARN': logger.warn,
            'ERROR': logger.error,
        }

        def print(self, *args, html=False, level='INFO', sep=' ', end='\n'):
            print_text = str(sep).join([str(_) for _ in args]) + str(end)
            self.print_function.get(level.upper(), logger.info)(print_text, html)
    else:
        def print(self, *args, html=False, level='INFO', sep=' ', end='\n'):
            print(*args, sep=sep, end=end)

    def debug(self, *args, html=False, sep=' ', end='\n'):
        self.print(*args, html=html, level='DEBUG', sep=sep, end=end)

    def info(self, *args, html=False, sep=' ', end='\n'):
        self.print(*args, html=html, level='INFO', sep=sep, end=end)

    def warn(self, *args, html=False, sep=' ', end='\n'):
        self.print(*args, html=html, level='WARN', sep=sep, end=end)

    def error(self, *args, html=False, sep=' ', end='\n'):
        self.print(*args, html=html, level='ERROR', sep=sep, end=end)
