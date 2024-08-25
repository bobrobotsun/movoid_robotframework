#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : calculate
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/13 13:47
# Description   : 
"""
import math
import random

from movoid_function import decorate_class_function_exclude

from ..decorator import robot_log_keyword
from ..basic import Basic


@decorate_class_function_exclude(robot_log_keyword)
class ActionCalculate(Basic):
    def __init__(self):
        super().__init__()

    def calculate_get_random(self, random_max=1, random_min=0, digit=3):
        """
        get random with a digit
        :param random_max: max
        :param random_min: min,change to max if is more than max
        :param digit: digit
        :return: a random float
        """
        random_list = [float(random_min), float(random_max)]
        random_min = min(random_list)
        random_max = max(random_list)
        digit = int(digit)
        self.print(f'try to return a random number [{random_min},{random_max}) digit is {digit}')
        random_value = random.random()
        real_value = random_value * (random_max - random_min) + random_min
        self.print(f'get random number:{real_value}')
        re_value = round(real_value, digit)
        return re_value

    @staticmethod
    def calculate_get_random_int(a, b):
        """
        get random int.use random.randint
        :param a: min or max
        :param b: min or max
        :return: random int
        """
        return random.randint(a, b)

    def calculate_average_similar(self, number1, number2, accuracy=1e-3):
        """
        计算两个数值或数组的平均值是否足够相近
        :param number1:
        :param number2:
        :param accuracy: 数小，就判定两个数值的绝对差值的相似阈值。如果数字比accuracy大，那就是两者的百分比差距阈值。只要有一个方向上满足了就是True
        :return:true or false。两者是否相近
        """
        try:
            number1 = self.analyse_json(number1)
            number2 = self.analyse_json(number2)
            accuracy = abs(float(accuracy))
            self.print(f'start to contrast two value:({number1}) vs ({number2}),accuracy is {accuracy}')
            if isinstance(number1, list):
                check1 = sum([float(_) for _ in number1]) / len(number1)
            else:
                check1 = float(number1)
            self.print(f'check1 is {check1}:{number1}')
            if isinstance(number2, list):
                check2 = sum([float(_) for _ in number2]) / len(number2)
            else:
                check2 = float(number2)
            self.print(f'check2 is {check2}:{number2}')
            if abs(check1) < accuracy or abs(check2) < accuracy:
                re_bool = abs(check2 - check1) < accuracy
            else:
                re_bool = abs(check2 / check1 - 1) < accuracy or abs(check1 / check2 - 1) < accuracy
            self.print(f'{check1} is similar to {check2}')
            return re_bool
        except Exception as err:
            self.print(f'return Fail!contrast two object <{number1}> and <{number2}> failed:{err}')
            return False

    def calculate_average_similar_in_digit(self, number1, number2, digit=3, offset_max=1.001):
        """
        计算两组数之间，在某一位之前是否完全
        :param number1: 第一组数/数组
        :param number2: 第二组数/数组
        :param digit: 小数点后位数
        :param offset_max: 允许的误差极限，如果是digit=3，offset_max=1.001，意味着允许两个数值有最多1.001e-3的差值
        :return: true or false。两者是否相近
        """
        try:
            number1 = self.analyse_json(number1)
            number2 = self.analyse_json(number2)
            digit = int(digit)
            offset_max = abs(float(offset_max))
            if isinstance(number1, list):
                check1 = sum([float(_) for _ in number1]) / len(number1)
            else:
                check1 = float(number1)
            check1 = round(check1, digit)
            self.print(f'check1 is {check1}:{number1}')
            if isinstance(number2, list):
                check2 = sum([float(_) for _ in number2]) / len(number2)
            else:
                check2 = float(number2)
            check2 = round(check2, digit)
            self.print(f'check2 is {check2}:{number2}')
            re_bool = abs(check1 - check2) <= offset_max * math.pow(10, -digit)
            return re_bool
        except Exception as err:
            self.print(f'return Fail!contrast two object <{number1}> and <{number2}> failed:{err}')
            return False

    def calculate_each_similar_in_digit(self, list1, list2, digit=3, offset_max=1.001):
        """
        计算两组数之间，在某一位之前是否完全
        :param list1: 第一组数组
        :param list2: 第二组数组
        :param digit: 小数点后位数
        :param offset_max: 允许的误差极限，如果是digit=3，offset_max=1.001，意味着允许两个数值有最多1.001e-3的差值
        :return: true or false。两者是否相近
        """
        try:
            object1 = self.analyse_json(list1)
            object2 = self.analyse_json(list2)
            digit = int(digit)
            self.print(f'start to contrast two value:({object1}) vs ({object2}),digit is {digit}')
            re_bool = True
            if isinstance(object1, list):
                for i, v in enumerate(object1):
                    object1[i] = float(v)
                if len(object1) == 1:
                    object1 = object1[0]
                    self.print(f'object1 is len 1 list ,change to float:{object1}')
            if isinstance(object2, list):
                for i, v in enumerate(object2):
                    object2[i] = float(v)
                if len(object2) == 1:
                    object2 = object2[0]
                    self.print(f'object2 is len 1 list ,change to float:{object2}')

            if isinstance(object1, list) and isinstance(object2, list):
                if len(object1) == len(object2):
                    for i, v1 in enumerate(object1):
                        v2 = object2[i]
                        if not self.calculate_average_similar_in_digit(v1, v2, digit, offset_max):
                            re_bool = False
                            break
                else:
                    self.print(f'their length {len(object1)}!={len(object2)},failed')
                    re_bool = False
            elif isinstance(object1, float) and isinstance(object2, float):
                re_bool = self.calculate_average_similar_in_digit(object1, object2, digit, offset_max)
            return re_bool
        except Exception as err:
            self.print(f'return Fail!contrast two object <{list1}> and <{list2}> failed:{err}')
            return False
