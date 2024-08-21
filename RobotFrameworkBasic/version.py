#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : version
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/12 18:05
# Description   : 
"""
import pathlib
import sys

run_file = pathlib.Path(sys.argv[0])
if run_file.stem == 'robot' and run_file.parent.name.lower() == 'scripts':
    run = 'robot'
elif run_file.name == 'run.py' and run_file.parent.name == 'robot' and run_file.parents[1].name.lower() == 'site-packages':
    run = 'robot'
else:
    run = 'python'
if run == 'robot':
    import robot

    robot_version = robot.__version__.split('.')
    if robot_version[0] in ('6', '7'):
        version = robot_version[0]
    else:
        raise ImportError(f'this can only run in robotframework 6.x or 7.x, but your version is {robot.__version__}')
else:
    version = ''

RUN = run
VERSION = version
