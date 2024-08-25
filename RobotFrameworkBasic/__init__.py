#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : __init__.py
# Author        : Sun YiFan-Movoid
# Time          : 2024/1/30 21:16
# Description   : 
"""
from .action import Action, ActionConfig
from .version import RUN, VERSION
from .decorator import robot_log_keyword, robot_no_log_keyword, do_until_check, wait_until_stable, do_when_error, check_parameters_type, always_true_until_check
from .error import RfError


class RobotBasic(Action):
    pass


class RobotBasicConfig(RobotBasic, ActionConfig):
    pass


class RobotFrameworkBasic(RobotBasic):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
