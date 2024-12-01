#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : test_assertion
# Author        : Sun YiFan-Movoid
# Time          : 2024/11/26 18:26
# Description   : 
"""
from RobotFrameworkBasic import RobotFrameworkBasic, robot_log_keyword, always_true_until_check

rf = RobotFrameworkBasic()


class Test_function_always_true_until_check:
    def test_assert_equal(self):
        rf.assert_equal(1, 1)
        rf.assert_not_equal(1, 2)
        try:
            rf.assert_equal(1, 2)
        except AssertionError:
            pass
        else:
            raise AssertionError
        try:
            rf.assert_not_equal(1, 1)
        except AssertionError:
            pass
        else:
            raise AssertionError

    def test_assert_equal_float(self):
        rf.assert_equal_float(1.23, 1.24, 1)
        rf.assert_not_equal_float(1.23, 1.24, 2)
        try:
            rf.assert_equal_float(1.23, 1.24, 2)
        except AssertionError:
            pass
        else:
            raise AssertionError
        try:
            rf.assert_not_equal_float(1.23, 1.24, 1)
        except AssertionError:
            pass
        else:
            raise AssertionError

    def test_assert_logic(self):
        rf.assert_logic('not', 1, '=', 1, 'and', 6, '>', 5, 'or', 'asdf', 'isinstance', str)
        rf.assert_true('1')
        rf.assert_false([])
        rf.assert_is_true(True)
        rf.assert_is_not_true(False)
        rf.assert_is_false(False)
        rf.assert_is_not_false(True)
        rf.assert_is_none(None)
        rf.assert_is_not_none(0)

        rf.assert_is(True, True)
        rf.assert_is_not(True, False)
        rf.assert_in(1, [1, 2, 3])
        rf.assert_not_in(1, [2, 3, 4])
        rf.assert_isinstance(True, bool)
        rf.assert_not_isinstance(123, str)
        rf.assert_issubclass(AssertionError, Exception)
        rf.assert_not_issubclass(str, bool)
