#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : config
# Author        : Sun YiFan-Movoid
# Time          : 2024/4/24 0:31
# Description   : 
"""
import json
from pathlib import Path

from ..common import BasicCommon


class ConfigItem:
    def __init__(self, value, source):
        self._value = value
        self._source = source

    @property
    def value(self):
        return self._value

    @property
    def source(self):
        return self._source

    def update(self, value, source=None):
        self._value = value
        self._source = self._source if source is None else source


class Config:
    def __init__(self, config_file: str):
        self._path = Path(config_file)
        if not self._path.is_file():
            self._path.touch()
        with self._path.open(mode='r') as f:
            config_text = f.read()
            config_dict = json.loads(config_text)
        self._ori = config_dict
        self._now = {}

    def __getitem__(self, item):
        return self._now[item].value

    def update(self, *labels, override=True, clear=False):
        if clear:
            self._now.clear()
        for label in labels:
            if label in self._ori:
                for i, v in self._ori[label].items():
                    if i in self._now:
                        if override:
                            self._now[i].update(v, label)
                    else:
                        self._now[i] = ConfigItem(v, label)


class BasicConfig(BasicCommon):
    def __init__(self):
        super().__init__()
        self._config_path = Path('config.json')
        self._config_ori = {}
        self._config_now = {}
        self._config_label_list = []

    def config_init(self, json_file: str):
        self._config_path = Path(json_file)
        if not self._config_path.is_file():
            self._config_path.touch()
        with self._config_path.open(mode='r') as f:
            config_text = f.read()
            config_dict = json.loads(config_text)
        self._config_ori = config_dict
        self._config_now = {}
        self._config_label_list = []

    def config_update(self, *labels, override=True, clear=False):
        if clear:
            self._config_now.clear()
            self._config_label_list = []
        for label in labels:
            if label in self._config_ori:
                self._config_label_list.append(label)
                for i, v in self._config_ori[label].items():
                    if i in self._config_now:
                        if override:
                            self._config_now[i].update(v, label)
                    else:
                        self._config_now[i] = ConfigItem(v, label)

    def config_update_single(self, label, key, value, ori=True):
        self._config_now[key] = ConfigItem(value, label)
        if ori:
            self._config_ori[label][key] = value
            with self._config_path.open(mode='w') as f:
                json.dump(self._config_ori, f)
