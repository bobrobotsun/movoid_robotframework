#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : common
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/13 12:04
# Description   : 
"""
import json

from robot.libraries.BuiltIn import BuiltIn

from .log import BasicLog
from .error import RfError
from .decorator import robot_log_keyword


class BasicCommon(BasicLog):
    def __init__(self):
        super().__init__()
        self.built = BuiltIn()
        self.warn_list = []
        self.output_dir = getattr(self, 'output_dir', None)

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
