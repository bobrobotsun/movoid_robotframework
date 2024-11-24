#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : __init__.py
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/21 1:29
# Description   : 
"""
from .assertion import ActionAssertion
from .calculate import ActionCalculate
from .config import ActionConfig


class Action(ActionAssertion, ActionCalculate):
    pass
