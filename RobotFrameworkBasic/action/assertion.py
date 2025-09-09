#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : assertion
# Author        : Sun YiFan-Movoid
# Time          : 2024/11/18 23:15
# Description   : 
"""
import math

from movoid_function import decorate_class_function_exclude

from ..decorator import robot_log_keyword, robot_no_log_keyword
from ..basic import Basic


@decorate_class_function_exclude(robot_log_keyword)
class ActionAssertion(Basic):
    assert_logic_arg = ('not', 'and', 'or')
    assert_operate_arg = ('is', 'is not', 'not is', 'isinstance', 'instance', 'subclass', 'issubclass', 'in', 'not in', 'in not', '=', '==', '!=', '>', '>=', '<', '<=', '<>', '><')

    def __init__(self):
        super().__init__()

    @robot_no_log_keyword
    def _assert_text(self, error_text, *args, error_format=None):
        if isinstance(error_format, str):
            for index, var in enumerate(args):
                error_format = error_format.replace(f'{{{index}}}', str(var))
            error_text = error_format
        return error_text

    def assert_equal(self, var1, var2, var_type=None, error_text=None, error_format=None):
        error_text = self._assert_text(
            str(error_text) if error_text else f'{var1} == {var2}',
            var1, var2,
            error_format=error_format)
        real_var1, var_type_str1 = self.convert_value_to(var1, var_type, return_type_str=True)
        real_var2, var_type_str2 = self.convert_value_to(var2, var_type, return_type_str=True)
        if var_type_str1 is None or var_type_str2 is None:
            self.print(f'try to assert >{real_var1}<({type(real_var1).__name__}) == >{real_var2}<({type(real_var2).__name__})')
        else:
            self.print(f'try to assert >{real_var1}< == >{real_var2}<')
        assert real_var1 == real_var2, error_text

    def assert_not_equal(self, var1, var2, var_type=None, error_text=None, error_format=None):
        error_text = self._assert_text(
            str(error_text) if error_text else f'{var1} == {var2}',
            var1, var2,
            error_format=error_format)
        real_var1, var_type_str1 = self.convert_value_to(var1, var_type, return_type_str=True)
        real_var2, var_type_str2 = self.convert_value_to(var2, var_type, return_type_str=True)
        if var_type_str1 is None or var_type_str2 is None:
            self.print(f'try to assert >{real_var1}<({type(real_var1).__name__}) != >{real_var2}<({type(real_var2).__name__})')
        else:
            self.print(f'try to assert >{real_var1}< != >{real_var2}<')
        assert real_var1 != real_var2, error_text

    def assert_equal_float(self, var1, var2, digit=3, error_text=None, error_format=None):
        digit = int(digit)
        real_var1 = round(float(var1), digit)
        real_var2 = round(float(var2), digit)
        error_text = self._assert_text(
            str(error_text) if error_text else f'{real_var1} == {real_var2}',
            var1, var2,
            error_format=error_format)
        self.print(f'try to assert >{real_var1}< == >{real_var2}<')
        assert real_var1 == real_var2, error_text

    def assert_not_equal_float(self, var1, var2, digit=3, error_text=None, error_format=None):
        digit = int(digit)
        real_var1 = round(float(var1), digit)
        real_var2 = round(float(var2), digit)
        error_text = self._assert_text(
            str(error_text) if error_text else f'{real_var1} != {real_var2}',
            var1, var2,
            error_format=error_format)
        self.print(f'try to assert >{real_var1}< != >{real_var2}<')
        assert real_var1 != real_var2, error_text

    def assert_calculate(self, *args, check_logic='all', error_text=None, error_format=None):
        """
        检查计算结果是否满足计算条件
        :param args: 一个变量、一个符号的模式进行输入
        :param check_logic: all就是所有判定条件都要满足；其他就是只要一个判定条件满足即可
        :param error_text: 错误时的error文字，否则直接打印公式
        :param error_text: 错误时的error文字，否则直接打印公式
        :raise AssertionError: 判定失败后raise
        """
        cal_list = [_ for _ in args]
        error_text = self._assert_text(
            str(error_text) if error_text else ' '.join([str(_) for _ in cal_list]),
            *args,
            error_format=error_format)
        result_list = []
        if len(cal_list) == 0:
            raise ValueError('nothing input')
        temp_value = self.convert_value_to_number(cal_list.pop(0))
        while True:
            self.print(temp_value, *cal_list)
            if len(cal_list) <= 1:
                break
            else:
                operate = cal_list.pop(0)
                if operate in ('abs',):
                    temp_value = abs(temp_value)
                else:
                    cal_value = self.convert_value_to_number(cal_list.pop(0))
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
                    elif operate in ('==', '='):
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
            assert all(result_list), error_text
        else:
            self.print(f'has one True: {result_list}')
            assert any(result_list), error_text

    def assert_true(self, var1, error_format=None):
        """转bool后，是否为True"""
        error_text = self._assert_text(
            f'{var1} should be True',
            var1,
            error_format=error_format)
        assert bool(var1), error_text

    def assert_false(self, var1, error_format=None):
        """转bool后，是否为True"""
        error_text = self._assert_text(
            f'{var1} should be False'
            , var1
            , error_format=error_format)
        assert not bool(var1), error_text

    def assert_is_none(self, var1, error_format=None):
        """判断是否是None"""
        error_text = self._assert_text(
            f'{var1} should be None'
            , var1
            , error_format=error_format)
        assert var1 is None, error_text

    def assert_is_not_none(self, var1, error_format=None):
        """判断是否是None"""
        error_text = self._assert_text(
            f'{var1} should not be None'
            , var1
            , error_format=error_format)
        assert var1 is not None, error_text

    def assert_is_true(self, var1, error_format=None):
        """判断是否是True"""
        error_text = self._assert_text(
            f'{var1} should True'
            , var1
            , error_format=error_format)
        assert var1 is True, error_text

    def assert_is_not_true(self, var1, error_format=None):
        """判断是否不是True"""
        error_text = self._assert_text(
            f'{var1} should not be True'
            , var1
            , error_format=error_format)
        assert var1 is not True, error_text

    def assert_is_false(self, var1, error_format=None):
        """判断是否是False"""
        error_text = self._assert_text(
            f'{var1} should be False'
            , var1
            , error_format=error_format)
        assert var1 is False, error_text

    def assert_is_not_false(self, var1, error_format=None):
        """判断是否不是False"""
        error_text = self._assert_text(
            f'{var1} should not be False'
            , var1
            , error_format=error_format)
        assert var1 is not False, error_text

    def assert_in(self, var1, var2, error_format=None):
        """判断是否in"""
        self.print(f'{var1} in {var2}')
        error_text = self._assert_text(
            f'{var1} should in {var2}'
            , var1
            , error_format=error_format)
        assert var1 in var2, error_text

    def assert_not_in(self, var1, var2, error_format=None):
        """判断是否not in"""
        self.print(f'{var1} not in {var2}')
        error_text = self._assert_text(
            f'{var1} is None'
            , var1
            , error_format=error_format)
        assert var1 not in var2, error_text

    def assert_is(self, var1, var2, error_format=None):
        """判断是否is"""
        self.print(f'{var1} is {var2}')
        error_text = self._assert_text(
            f'{var1} is None'
            , var1
            , error_format=error_format)
        assert var1 is var2, error_text

    def assert_is_not(self, var1, var2, error_format=None):
        """判断是否not is"""
        self.print(f'{var1} is not {var2}')
        error_text = self._assert_text(
            f'{var1} is None'
            , var1
            , error_format=error_format)
        assert var1 is not var2, error_text

    def assert_isinstance(self, var1, var2, error_format=None):
        """判断是否isinstance"""
        self.print(f'isinstance({var1}, {var2})')
        error_text = self._assert_text(
            f'should isinstance({var1}, {var2})'
            , var1
            , error_format=error_format)
        assert isinstance(var1, var2), error_text

    def assert_not_isinstance(self, var1, var2, error_format=None):
        """判断是否not isinstance"""
        self.print(f'not isinstance({var1}, {var2})')
        error_text = self._assert_text(
            f'should not isinstance({var1}, {var2})'
            , var1
            , error_format=error_format)
        assert not isinstance(var1, var2), error_text

    def assert_issubclass(self, var1, var2, error_format=None):
        """判断是否issubclass"""
        self.print(f'issubclass({var1}, {var2})')
        error_text = self._assert_text(
            f'should issubclass({var1}, {var2})'
            , var1
            , error_format=error_format)
        assert issubclass(var1, var2), error_text

    def assert_not_issubclass(self, var1, var2, error_format=None):
        """判断是否not issubclass"""
        self.print(f'not issubclass({var1}, {var2})')
        error_text = self._assert_text(
            f'should not issubclass({var1}, {var2})'
            , var1
            , error_format=error_format)
        assert not issubclass(var1, var2), error_text

    def analyse_logic(self, *args):
        if len(args) == 3:
            if args[1] in self.assert_operate_arg:
                operate = args[1]
                if operate == 'is':
                    re_value = args[0] is args[2]
                elif operate in ('is not', 'not is'):
                    re_value = args[0] is not args[2]
                elif operate == 'in':
                    re_value = args[0] in args[2]
                elif operate in ('in not', 'not in'):
                    re_value = args[0] not in args[2]
                elif operate in ('instance', 'isinstance'):
                    re_value = isinstance(args[0], args[2])
                elif operate in ('subclass', 'issubclass'):
                    re_value = issubclass(args[0], args[2])
                elif operate in ('=', '=='):
                    re_value = args[0] == args[2]
                elif operate in ('!=', '<>', '><'):
                    re_value = args[0] != args[2]
                elif operate == '>':
                    re_value = args[0] > args[2]
                elif operate == '>=':
                    re_value = args[0] >= args[2]
                elif operate == '<':
                    re_value = args[0] < args[2]
                elif operate == '<=':
                    re_value = args[0] <= args[2]
                else:
                    raise SyntaxError(f'unknown operator: {operate}')
            else:
                raise SyntaxError(f'unknown operator: {args[1]}')
        elif len(args) == 1:
            re_value = bool(args[0])
        else:
            raise SyntaxError(f'unknown structure: {args}')
        return re_value

    def assert_logic(self, *args, error_text=None, error_format=None):
        """
        使用逻辑not、and、or和判断符号，进行bool值的判断
        :param args: 所有的变量、计算符号、逻辑符号
        :param error_text: 错误文本，如果不填，判断失败时，会显示原始公式
        """
        error_text = str(error_text) if error_text else ' '.join([str(_) for _ in args])
        error_text = self._assert_text(
            str(error_text) if error_text else ' '.join([str(_) for _ in args])
            , *args
            , error_format=error_format)
        logic_list = []
        temp_list = []
        for i in args:
            if i in self.assert_logic_arg:
                if temp_list:
                    logic_list.append(temp_list)
                    temp_list = []
                logic_list.append(i)
            else:
                temp_list.append(i)
        else:
            if temp_list:
                logic_list.append(temp_list)
        self.print(f'{logic_list} :combine all value and operator to')
        for i, v in enumerate(logic_list):
            if isinstance(v, list):
                logic_list[i] = self.analyse_logic(*v)
        self.print(f'{logic_list} :calculate all operator')
        i = 0
        while i < len(logic_list):
            v = logic_list[i]
            if v == 'not':
                if i == len(logic_list) - 1:
                    raise SyntaxError('"not" cannot be the last arg')
                temp = logic_list[i + 1]
                if temp == 'not':
                    logic_list = logic_list[:i]
                elif isinstance(temp, bool):
                    logic_list = [*logic_list[:i], not temp, *logic_list[i + 2:]]
                else:
                    raise SyntaxError(f'{temp} should not be after "not"')
                self.print(f'{logic_list} : analyse "not" index of {i}')
            i += 1
        i = 0
        while i < len(logic_list):
            v = logic_list[i]
            if v == 'and':
                if i == 0 or i == len(logic_list) - 1:
                    raise SyntaxError('"and" cannot be the first or last arg')
                temp1 = logic_list[i - 1]
                temp2 = logic_list[i + 1]
                if isinstance(temp1, bool) and isinstance(temp2, bool):
                    logic_list = [*logic_list[:i - 1], temp1 and temp2, *logic_list[i + 2:]]
                else:
                    raise SyntaxError(f'both {temp1} and {temp2} should be bool')
                self.print(f'{logic_list} : analyse "and" index of {i}')
            i += 1
        i = 0
        while i < len(logic_list):
            v = logic_list[i]
            if v == 'or':
                if i == 0 or i == len(logic_list) - 1:
                    raise SyntaxError('"or" cannot be the first or last arg')
                temp1 = logic_list[i - 1]
                temp2 = logic_list[i + 1]
                if isinstance(temp1, bool) and isinstance(temp2, bool):
                    logic_list = [*logic_list[:i - 1], temp1 or temp2, *logic_list[i + 2:]]
                else:
                    raise SyntaxError(f'both {temp1} and {temp2} should be bool')
                self.print(f'{logic_list} : analyse "or" index of {i}')
            i += 1
        if len(logic_list) == 1:
            assert logic_list[0], error_text
        else:
            raise SyntaxError(f'{logic_list} :too many values last.check if it lack operator.')
