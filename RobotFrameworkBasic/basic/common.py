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

from movoid_config import Config
from movoid_function import replace_function, decorate_class_function_exclude

from robot.libraries.BuiltIn import BuiltIn

from ..decorator import robot_no_log_keyword, robot_log_keyword
from ..error import RfError
from ..version import VERSION

if VERSION:
    from robot.api import logger


@decorate_class_function_exclude(robot_log_keyword)
class BasicCommon:
    def __init__(self):
        super().__init__()
        self.built = BuiltIn()
        self.warn_list = []
        self.output_dir = getattr(self, 'output_dir', None)
        self._robot_variable = {}
        self._robot_config = Config()
        self.robot_config_init()
        if VERSION:
            self.replace_builtin_print()

    if VERSION:
        print_function = {
            'DEBUG': logger.debug,
            'INFO': logger.info,
            'WARN': logger.warn,
            'ERROR': logger.error,
        }

        @robot_no_log_keyword
        def print(self, *args, html=False, also_console=None, level='INFO', sep=' ', end='\n', file=None, flush=True, log=False):
            if log:
                self.log(*args, html=html, also_console=also_console, level=level, sep=sep, end=end, file=file, flush=flush)
            else:
                level = str(level).upper()
                also_console = self._robot_config.print_console if also_console is None else bool(also_console)
                print_text = str(sep).join([str(_) for _ in args])
                print_text_end = print_text + str(end)
                if file is None:
                    logger.write(print_text, level=level, html=html)
                elif file == sys.stdout:
                    logger.write(print_text, html=html)
                elif file == sys.stderr:
                    logger.error(print_text, html=html)
                else:
                    file.write(print_text_end)
                    if flush:
                        file.flush()
                if also_console:
                    if level in ('WARN', 'ERROR'):
                        # stream = sys.__stderr__
                        pass
                    else:
                        stream = sys.__stdout__
                        stream.write(print_text_end)
                        stream.flush()

        def get_robot_variable(self, variable_name: str, default=None):
            return self.built.get_variable_value("${" + variable_name + "}", default)

        def set_robot_variable(self, variable_name: str, value):
            self.built.set_global_variable("${" + variable_name + "}", value)

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
        @robot_no_log_keyword
        def print(self, *args, html=False, also_console=None, level='INFO', sep=' ', end='\n', file=None, flush=True, log=False):  # noqa
            if log:
                self.log(*args, html=html, also_console=also_console, level=level, sep=sep, end=end, file=file, flush=flush)
            else:
                level = str(level).upper()
                if file is None and level == 'ERROR':
                    file = sys.__stderr__
                print(*args, sep=sep, end=end, file=file, flush=flush)

        def get_robot_variable(self, variable_name: str, default=None):
            return self._robot_variable.get(variable_name, default)

        def set_robot_variable(self, variable_name: str, value):
            self._robot_variable[variable_name] = value

        def get_suite_case_str(self, join_str: str = '-', suite: bool = True, case: bool = True, suite_ori: str = ''):  # noqa
            sc_list = []
            if suite:
                sc_list.append('suite')
            if case:
                sc_list.append('case')
            return join_str.join(sc_list)

    @robot_no_log_keyword
    def replace_builtin_print(self):
        replace_function(print, self.print)

    @robot_log_keyword
    def log(self, *args, html=False, also_console=None, level='INFO', sep=' ', end='\n', file=None, flush=True):
        self.print(*args, html=html, also_console=also_console, level=level, sep=sep, end=end, file=file, flush=flush, log=False)

    @robot_no_log_keyword
    def debug(self, *args, html=False, also_console=None, sep=' ', end='\n', file=None, flush=True, log=False):
        self.print(*args, html=html, also_console=also_console, level='DEBUG', sep=sep, end=end, file=file, flush=flush, log=log)

    @robot_no_log_keyword
    def info(self, *args, html=False, also_console=None, sep=' ', end='\n', file=None, flush=True, log=False):
        self.print(*args, html=html, also_console=also_console, level='INFO', sep=sep, end=end, file=file, flush=flush, log=log)

    @robot_no_log_keyword
    def warn(self, *args, html=False, also_console=None, sep=' ', end='\n', file=None, flush=True, log=False):
        self.print(*args, html=html, also_console=also_console, level='WARN', sep=sep, end=end, file=file, flush=flush, log=log)

    @robot_no_log_keyword
    def error(self, *args, html=False, also_console=None, sep=' ', end='\n', file=None, flush=True, log=False):
        self.print(*args, html=html, also_console=also_console, level='ERROR', sep=sep, end=end, file=file, flush=flush, log=log)

    def analyse_json(self, value):
        """
        获取当前的内容并以json转换它
        :param value: 字符串就进行json转换，其他则不转换
        :return:
        """
        self.print(f'try to change str to variable:({type(value).__name__}):{value}')
        re_value = value
        if isinstance(value, str):
            try:
                re_value = json.loads(value)
            except json.decoder.JSONDecodeError:
                re_value = value
        return re_value

    def convert_value_to(self, var, var_type=None, return_type_str=False):
        """
        将当前变量转换为相应的类型
        :param var: 变量
        :param var_type: 类型，可以是字符串，但是字符串仅限str、float、int、bool、eval、json
        :param return_type_str: 返回转换的类型符号
        :return:
        """
        if isinstance(var_type, type):
            var_type_str = var_type.__name__
        else:
            var_type_str = str(var_type)
        if var_type is None:
            re_value = var
            var_type_str = None
        elif var_type_str in ('str',):
            re_value = str(var)
        elif var_type_str in ('float',):
            re_value = float(var)
        elif var_type_str in ('int',):
            re_value = int(var)
        elif var_type_str in ('bool',):
            re_value = bool(var)
        elif var_type_str in ('eval',):
            re_value = eval(var) if isinstance(var, str) else var
        elif var_type_str in ('json',):
            re_value = json.loads(var) if isinstance(var, str) else var
        elif isinstance(var_type, type):
            re_value = var_type(var)
        else:
            self.print(f'we do not know what is: {var_type}')
            var_type_str = None
            re_value = var
        if return_type_str:
            return re_value, var_type_str
        else:
            return re_value

    def convert_value_to_number(self, value):
        """
        获取当前的内容并转换为number
        :param value: 字符串就转换为int或float
        :return:
        """
        self.print(f'try to change str to variable:({type(value).__name__}):{value}')
        re_value = value
        if not isinstance(value, (int, float)):
            try:
                temp_value = int(value)
                if temp_value == float(value):
                    re_value = temp_value
            except ValueError:
                try:
                    re_value = float(value)
                except:
                    raise ValueError(f'cannot convert {value} to a number')
            except:
                raise ValueError(f'cannot convert {value} to a number')
        return re_value

    def analyse_self_function(self, function_name):
        """
        尝试将函数名转换为自己能识别的函数
        :param function_name: str（函数名）、function（函数本身）
        :return: 返回两个值：函数、函数名
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

    @staticmethod
    def always_true():
        return True

    def log_show_image(self, image_path: str):
        with open(image_path, mode='rb') as f:
            img_str = base64.b64encode(f.read()).decode()
            self.print(f'<img src="data:image/png;base64,{img_str}">', html=True)

    def robot_check_param(self, param_input: object, param_style: Union[str, type], default=None, error=True):
        """
        检查参数是否符合要求
        :param param_input:实际输入的参数
        :param param_style: 参数类型，可以使用字符串或者直接输入类
        :param default: 默认值。如果是None，那么会使用默认值
        :param error: 当参数不符且转换失败时，是否报错。如果False，那么将不报错，并使用默认值
        :return: 转换后的参数
        """
        if param_input is None:
            print(f'input is None,so we use default >{default}<')
            change_input = default
        else:
            change_input = param_input
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
        if type(change_input).__name__ == param_style_str:
            print('style is correct, we do not change it.')
            return change_input
        print(f'try to change <{change_input}> to {param_style}')
        try:
            if param_style_str in ('str',):
                re_value = str(change_input)
            elif param_style_str in ('int',):
                re_value = int(change_input)
            elif param_style_str in ('float',):
                re_value = float(change_input)
            elif param_style_str in ('bool',):
                if change_input in ('true',):
                    re_value = True
                elif change_input in ('false',):
                    re_value = False
                else:
                    print(f'>{change_input}< is not a traditional bool, we use forced conversion.')
                    re_value = bool(change_input)
            else:
                re_value = eval(f'{param_style_str}({change_input})')
        except Exception as err:
            error_text = f'something wrong happened when we change <{change_input}> to <{param_style_str}>:\n{traceback.format_exc()}'
            if error:
                self.error(error_text)
                raise err
            else:
                print(error_text)
                print(f'we use default value:<{default}>({type(default).__name__})')
                re_value = default
        return re_value

    @robot_no_log_keyword
    def robot_config_init(self):
        self._robot_config.add_rule('print_console', 'bool', default=False)
        self._robot_config.init(None, 'movoid_robotframework.ini', False)

    @robot_no_log_keyword
    def debug_teardown(self, function, args, kwargs, re_value, error, trace_back, has_return):
        if error:
            self.error(self.get_suite_case_str(), function.__name__, args, kwargs, error)
        if has_return:
            return re_value
