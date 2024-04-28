#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : common
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/13 12:04
# Description   : 
"""
import base64
import json

from robot.libraries.BuiltIn import BuiltIn

from .decorator import robot_log_keyword
from .error import RfError
from .version import VERSION

if VERSION:
    from robot.api import logger


class BasicCommon:
    def __init__(self):
        super().__init__()
        self.built = BuiltIn()
        self.warn_list = []
        self.output_dir = getattr(self, 'output_dir', None)

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

    @robot_log_keyword
    def get_robot_variable(self, variable_name: str, default=None):
        return self.built.get_variable_value("${" + variable_name + "}", default)

    @robot_log_keyword
    def set_robot_variable(self, variable_name: str, value):
        self.built.set_global_variable("${" + variable_name + "}", value)

    @robot_log_keyword
    def analyse_json(self, value):
        """
        change json str to a python value or do not change it
        :param value: a json str or anything
        :return: a python value or value itself
        """
        self.print(f'try to change str to variable:({type(value).__name__}):{value}')
        re_value = value
        if isinstance(value, str):
            try:
                re_value = json.loads(value)
            except json.decoder.JSONDecodeError:
                re_value = value
        return re_value

    @robot_log_keyword
    def analyse_self_function(self, function_name):
        """
        find a function by name or do not change it
        :param function_name: function name(str) or a function(function)
        :return: target function or param itself
        """
        if isinstance(function_name, str):
            if hasattr(self, function_name):
                function = getattr(self, function_name)
            else:
                raise RfError(f'there is no function called:{function_name}')
        elif callable(function_name):
            function = function_name
            function_name = function.__name__
        else:
            raise RfError(f'wrong function:{function_name}')
        return function, function_name

    @robot_log_keyword
    def set_to_dictionary(self, ori_dict, key, value):
        """
        set a value to a dict.
        :param ori_dict: target dict
        :param key: target key
        :param value: value to be set
        :return: None
        """
        ori_dict[key] = value

    def always_true(self):
        return True

    @robot_log_keyword
    def get_suite_case_str(self, join_str: str = '-', suite: bool = True, case: bool = True):
        """
        获取当前的suit、case的名称
        :param join_str: suite和case的连接字符串，默认为-
        :param suite: 是否显示suite名
        :param case: 是否显示case名，如果不是case内，即使True也不显示
        :return: 连接好的字符串
        """
        sc_list = []
        if suite:
            sc_list.append(self.get_robot_variable('SUITE NAME'))
        if case:
            temp = self.get_robot_variable('TEST NAME')
            if temp is not None:
                sc_list.append(self.get_robot_variable('TEST NAME'))
        return join_str.join(sc_list)

    @robot_log_keyword
    def log_show_image(self, image_path: str):
        with open(image_path, mode='rb') as f:
            img_str = base64.b64encode(f.read()).decode()
            self.print(f'<img src="data:image/png;base64,{img_str}">', html=True)
