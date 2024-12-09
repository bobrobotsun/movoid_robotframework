#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : test_common
# Author        : Sun YiFan-Movoid
# Time          : 2024/12/9 12:47
# Description   : 
"""
from RobotFrameworkBasic import RobotFrameworkBasic, robot_log_keyword, always_true_until_check


class Test_function_var:
    rf = RobotFrameworkBasic()

    def test_01_var_get(self):
        assert self.rf.var_get(1) == 1
        assert self.rf.var_get('1') == '1'

    def test_02_var_get_key(self):
        assert self.rf.var_get_key({1: 2}, 1) == 2
        assert self.rf.var_get_key([3, 1, 8], 0) == 3
        assert self.rf.var_get_key([3, 1, 8], 2) == 8
        try:
            self.rf.var_get_key({'a': 666}, 'b')
        except KeyError:
            pass
        else:
            raise AssertionError
        try:
            self.rf.var_get_key((2, 3, 4), 3)
        except KeyError:
            pass
        else:
            raise AssertionError

    def test_03_var_get_attr(self):
        self.rf.var_get_attr({1: 2}, 'keys')
        try:
            self.rf.var_get_attr({'a': 666}, 'bbbb')
        except AttributeError:
            pass
        else:
            raise AssertionError
        try:
            self.rf.var_get_attr((2, 3, 4), '_init_')
        except AttributeError:
            pass
        else:
            raise AssertionError
