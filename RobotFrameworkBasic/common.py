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
import pathlib
import sys
import traceback
from typing import Union
from movoid_function import replace_function

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
        self._robot_variable = {}
        if VERSION:
            self.replace_builtin_print()

    if VERSION:
        print_function = {
            'DEBUG': logger.debug,
            'INFO': logger.info,
            'WARN': logger.warn,
            'ERROR': logger.error,
        }

        def print(self, *args, html=False, also_console=False, level='INFO', sep=' ', end='\n', file=None):
            print_text = str(sep).join([str(_) for _ in args]) + str(end)
            if file is None:
                logger.write(print_text, level=level, html=html)
            elif file == sys.stdout:
                logger.info(print_text, html=html)
            elif file == sys.stderr:
                logger.error(print_text, html=html)
            else:
                file.write(print_text)
            if also_console:
                logger.console(print_text)

        @robot_log_keyword
        def get_robot_variable(self, variable_name: str, default=None):
            return self.built.get_variable_value("${" + variable_name + "}", default)

        @robot_log_keyword
        def set_robot_variable(self, variable_name: str, value):
            self.built.set_global_variable("${" + variable_name + "}", value)

        @robot_log_keyword
        def get_suite_case_str(self, join_str: str = '-', suite: bool = True, case: bool = True, suite_ori: str = ''):
            """
            获取当前的suit、case的名称
            :param join_str: suite和case的连接字符串，默认为-
            :param suite: 是否显示suite名
            :param case: 是否显示case名，如果不是case内，即使True也不显示
            :param suite_ori: suite名的最高suite是不是使用原名，如果设置为空，那么使用原名
            :return: 连接好的字符串
            """
            sc_list = []
            if suite:
                suite = self.get_robot_variable('SUITE NAME')
                if suite_ori:
                    exe_dir = self.get_robot_variable('EXECDIR')
                    main_suite_len = len(pathlib.Path(exe_dir).name)
                    if len(suite) >= main_suite_len:
                        suite_body = suite[main_suite_len:]
                    else:
                        suite_body = ''
                    suite_head = suite_ori
                    suite = suite_head + suite_body
                sc_list.append(suite)
            if case:
                temp = self.get_robot_variable('TEST NAME')
                if temp is not None:
                    sc_list.append(self.get_robot_variable('TEST NAME'))
            return join_str.join(sc_list)
    else:
        def print(self, *args, html=False, also_console=False, level='INFO', sep=' ', end='\n', file=None):
            print(*args, sep=sep, end=end, file=file)

        def get_robot_variable(self, variable_name: str, default=None):
            return self._robot_variable.get(variable_name, default)

        def set_robot_variable(self, variable_name: str, value):
            self._robot_variable[variable_name] = value

        def get_suite_case_str(self, join_str: str = '-', suite: bool = True, case: bool = True, suite_ori: str = ''):
            sc_list = []
            if suite:
                sc_list.append('suite')
            if case:
                sc_list.append('case')
            return join_str.join(sc_list)

    def replace_builtin_print(self):
        replace_function(print, self.print)

    def debug(self, *args, html=False, also_console=False, sep=' ', end='\n', file=None):
        self.print(*args, html=html, also_console=also_console, level='DEBUG', sep=sep, end=end, file=file)

    def info(self, *args, html=False, also_console=False, sep=' ', end='\n', file=None):
        self.print(*args, html=html, also_console=also_console, level='INFO', sep=sep, end=end, file=file)

    def warn(self, *args, html=False, also_console=False, sep=' ', end='\n', file=None):
        self.print(*args, html=html, also_console=also_console, level='WARN', sep=sep, end=end, file=file)

    def error(self, *args, html=False, also_console=False, sep=' ', end='\n', file=None):
        self.print(*args, html=html, also_console=also_console, level='ERROR', sep=sep, end=end, file=file)

    @staticmethod
    def _analyse_json(value):
        """
        analyse_json的无日志版本
        """
        re_value = value
        if isinstance(value, str):
            try:
                re_value = json.loads(value)
            except json.decoder.JSONDecodeError:
                re_value = value
        return re_value

    @robot_log_keyword
    def analyse_json(self, value):
        """
        获取当前的内容并以json转换它
        :param value: 字符串就进行json转换，其他则不转换
        :return:
        """
        self.print(f'try to change str to variable:({type(value).__name__}):{value}')
        return self._analyse_json(value)

    def _analyse_self_function(self, function_name):
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
    def analyse_self_function(self, function_name):
        """
        尝试将函数名转换为自己能识别的函数
        :param function_name: str（函数名）、function（函数本身）
        :return: 返回两个值：函数、函数名
        """
        return self._analyse_self_function(function_name)

    @staticmethod
    @robot_log_keyword
    def always_true():
        return True

    @robot_log_keyword
    def log_show_image(self, image_path: str):
        with open(image_path, mode='rb') as f:
            img_str = base64.b64encode(f.read()).decode()
            self.print(f'<img src="data:image/png;base64,{img_str}">', html=True)

    @robot_log_keyword
    def robot_check_param(self, param_str: object, param_style: Union[str, type], default=None, error=False):
        if type(param_style) is str:
            param_style_str = param_style.lower()
        elif type(param_style) is type:
            param_style_str = param_style.__name__
        else:
            error_text = f'what is <{param_style}>({type(param_style).__name__}) which is not str or type?'
            if error:
                raise TypeError(error_text)
            else:
                return default
        if type(param_str).__name__ == param_style_str:
            self.print('style is correct, we do not change it.')
            return param_str
        self.print(f'try to change <{param_str}> to {param_style}')
        try:
            if param_style_str in ('str',):
                re_value = str(param_str)
            elif param_style_str in ('int',):
                re_value = int(param_str)
            elif param_style_str in ('float',):
                re_value = float(param_str)
            elif param_style_str in ('bool',):
                if param_str in ('true',):
                    re_value = True
                elif param_str in ('false',):
                    re_value = False
                else:
                    self.print(f'{param_str} is not a traditional bool, we use forced conversion.')
                    re_value = bool(param_str)
            else:
                re_value = eval(f'{param_style_str}({param_str})')
        except Exception as err:
            error_text = f'something wrong happened when we change <{param_str}> to <{param_style_str}>:\n{traceback.format_exc()}'
            if error:
                self.error(error_text)
                raise err
            else:
                self.print(error_text)
                self.print(f'we use default value:<{default}>({type(default).__name__})')
                re_value = default
        return re_value
