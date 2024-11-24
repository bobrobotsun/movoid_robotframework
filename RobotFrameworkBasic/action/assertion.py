#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : assertion
# Author        : Sun YiFan-Movoid
# Time          : 2024/11/18 23:15
# Description   : 
"""
import json
import math

from movoid_function import decorate_class_function_exclude

from ..decorator import robot_log_keyword
from ..basic import Basic


@decorate_class_function_exclude(robot_log_keyword)
class ActionAssertion(Basic):
    def __init__(self):
        super().__init__()

    def assert_equal(self, var1, var2, var_type=None):
        if isinstance(var_type, type):
            var_type_str = var_type.__name__
        else:
            var_type_str = str(var_type)
        if var_type is None:
            real_var1 = var1
            real_var2 = var2
        elif var_type_str in ('str',):
            real_var1 = str(var1)
            real_var2 = str(var2)
        elif var_type_str in ('float',):
            real_var1 = float(var1)
            real_var2 = float(var2)
        elif var_type_str in ('int',):
            real_var1 = int(var1)
            real_var2 = int(var2)
        elif var_type_str in ('bool',):
            real_var1 = bool(var1)
            real_var2 = bool(var2)
        elif var_type_str in ('eval',):
            real_var1 = eval(var1) if isinstance(var1, str) else var1
            real_var2 = eval(var2) if isinstance(var2, str) else var2
        elif var_type_str in ('json',):
            real_var1 = json.loads(var1) if isinstance(var1, str) else var1
            real_var2 = json.loads(var2) if isinstance(var2, str) else var2
        else:
            var_type = None
            self.print(f'we do not know what is {var_type},so we do not change type of var')
            real_var1 = var1
            real_var2 = var2
        if var_type is None:
            self.print(f'try to assert >{real_var1}<({type(real_var1).__name__}) == >{real_var2}<({type(real_var2).__name__})')
        else:
            self.print(f'try to assert >{real_var1}< == >{real_var2}<')
        assert real_var1 == real_var2

    def assert_calculate(self, *args, check_logic='all'):
        """
        检查计算结果是否满足计算条件
        :param args: 一个变量、一个符号的模式进行输入
        :param check_logic: all就是所有判定条件都要满足；其他就是只要一个判定条件满足即可
        :raise AssertionError: 判定失败后raise
        """
        cal_list = [_ for _ in args]
        result_list = []
        if len(cal_list) == 0:
            raise ValueError('nothing input')
        temp_value = self.analyse_number(cal_list.pop(0))
        while True:
            self.print(temp_value, *cal_list)
            if len(cal_list) <= 1:
                break
            else:
                operate = cal_list.pop(0)
                if operate in ('abs',):
                    temp_value = abs(temp_value)
                else:
                    cal_value = self.analyse_number(cal_list.pop(0))
                    if operate == '<':
                        temp_result = temp_value < cal_value
                        self.print(f'{temp_result}: {temp_value} < {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '<=':
                        temp_result = temp_value <= cal_value
                        self.print(f'{temp_result}: {temp_value} <= {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '>':
                        temp_result = temp_value > cal_value
                        self.print(f'{temp_result}: {temp_value} > {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '>=':
                        temp_result = temp_value >= cal_value
                        self.print(f'{temp_result}: {temp_value} >= {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '==':
                        temp_result = temp_value == cal_value
                        self.print(f'{temp_result}: {temp_value} == {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '!=':
                        temp_result = temp_value != cal_list[1]
                        self.print(f'{temp_result}: {temp_value} != {cal_value}')
                        result_list.append(temp_result)
                    elif operate == '+':
                        temp_value += cal_value
                    elif operate == '-':
                        temp_value -= cal_value
                    elif operate == '*':
                        temp_value *= cal_value
                    elif operate == '/':
                        temp_value /= cal_value
                    elif operate == '//':
                        temp_value //= cal_value
                    elif operate in ('^', '**'):
                        temp_value = temp_value ** cal_value
                    elif operate in ('%', 'mod'):
                        temp_value %= cal_value
                    elif operate in ('round',):
                        temp_value = round(temp_value, cal_value)
                    elif operate in ('floor',):
                        multi = 10 ** cal_value
                        temp_value = math.floor(temp_value * multi) / multi
                    elif operate in ('ceil',):
                        multi = 10 ** cal_value
                        temp_value = math.ceil(temp_value * multi) / multi
                    elif operate == '<<':
                        temp_value = temp_value << cal_value
                    elif operate == '>>':
                        temp_value = temp_value >> cal_value
                    elif operate == '&':
                        temp_value = temp_value & cal_value
                    elif operate == '|':
                        temp_value = temp_value | cal_value
                    else:
                        raise ValueError(f'i do not know what is :{operate}')
        if check_logic == 'all':
            self.print(f'all be True: {result_list}')
            assert all(result_list)
        else:
            self.print(f'has one True: {result_list}')
            assert any(result_list)
