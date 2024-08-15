#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : __init__.py
# Author        : Sun YiFan-Movoid
# Time          : 2024/1/30 21:16
# Description   : 
"""
from .version import RUN, VERSION
from .main import RobotBasic, RobotBasicConfig
from .decorator import robot_log_keyword, do_until_check, wait_until_stable, do_when_error, check_parameters_type, always_true_until_check
from .error import RfError


class RobotFrameworkBasic(RobotBasic):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
