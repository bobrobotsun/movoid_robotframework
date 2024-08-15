#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : main
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/13 11:58
# Description   : 
"""
from .action import BasicCalculate, BasicConfig


class RobotBasic(BasicCalculate):
    pass


class RobotBasicConfig(BasicCalculate, BasicConfig):
    pass
