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
from typing import Dict, Any, List

from ..common import BasicCommon
from ..decorator import robot_log_keyword


class ConfigItem:
    def __init__(self, value: Any, source: str):
        self._value: Any = value
        self._root: str = source
        self._source: str = source

    def __getitem__(self, item):
        return self._value

    @property
    def value(self) -> Any:
        return self._value

    @property
    def source(self) -> str:
        return self._source

    @property
    def root(self) -> str:
        return self._root

    def update(self, value=None, source=None):
        self._value = self._value if value is None else value
        self._source = self._source if source is None else source

    def inherit(self, source: str) -> 'ConfigItem':
        temp = ConfigItem(self._value, self._source)
        temp.update(source=source)
        return temp


class Config:

    def __init__(self, json_file: str = None, print_func=None):
        self._path = Path('config.json')
        self._ori: Dict[str, Dict[str, Any]] = {}
        self._now: Dict[str, ConfigItem] = {}
        self._label_list: List[str] = []
        self.init(json_file)
        self.print = print if print_func is None else print_func

    def __getitem__(self, item):
        return self._now[item].value

    def init(self, json_file: str = None):
        self._path = self._path if json_file is None else Path(json_file)
        self.read()

    def write(self):
        temp_dict = {_k: _v for _k, _v in self._ori.items() if not _k.startswith('$')}
        with self._path.open(mode='w') as f:
            json.dump(temp_dict, f, default=lambda x: x.value)
        temp_path = self._path.parent / f'${self._path.name}'
        with temp_path.open(mode='w') as f:
            json.dump(self._ori, f, default=lambda x: x.value)

    def read(self):
        if not self._path.is_file():
            self._path.touch()
            self._path.write_text('{}')
        with self._path.open(mode='r') as f:
            config_text = f.read()
            config_dict = json.loads(config_text)
        self.ori_init(config_dict)
        self._now = {}
        self._label_list = []

    def ori_init(self, config_dict: Dict[str, Dict[str, Any]]):
        self._ori = {}
        for i, v in config_dict.items():
            if i.startswith('$'):
                continue
            else:
                self.ori_update_label(i, v, file=False)
        self.write()

    def ori_update_label(self, label: str, kv_dict: Dict[str, Any], override=True, file=True):
        label_now = f'${label}'
        self._ori[label] = {}
        self._ori[label_now] = {}
        for i, v in kv_dict.items():
            self._ori[label][i] = v
            if i == '__inherit__':
                v_now = f'${v}'
                if v in self._ori and v_now in self._ori:
                    for j, w in self._ori[v_now].items():
                        if override:
                            self._ori[label_now][j] = w.inherit(label)
                        else:
                            self._ori[label_now].setdefault(j, w.inherit(label))
                else:
                    raise KeyError(f'config "{label}" try to inherit "{v}" which does not exist.')
            else:
                self._ori[label_now][i] = ConfigItem(v, label)
        if file:
            self.write()

    def now_use_label(self, label, override=True):
        label_now = f'${label}'
        if label in self._ori and label_now in self._ori:
            self._label_list.append(label)
            for i, v in self._ori[label_now].items():
                if override:
                    self._now[i] = v
                else:
                    self._now.setdefault(i, v)

    def now_clear(self):
        self._now = {}
        self._label_list = []

    def show_now_value(self):
        for i, v in self._now.items():
            self.print(f'{i} : {v.value} [from {v.source} & root {v.root}]')

    def show_now_list(self):
        self.print(f'now config contains :[{",".join(self._label_list)}]')

    def config_use_suite_case_list(self, override=True, clear=False):
        suite_case_now = f'${self.__suite_case_label}'
        if self.__suite_case_label not in self._ori:
            self.__config_ori_update(self.__suite_case_label, {})
        suite_case_key = self.get_suite_case_str()
        if suite_case_key not in self._config_ori[suite_case_now]:
            self.config_update_key(suite_case_key, [], self.__suite_case_label)
        self.config_use_label(*self._config_ori[suite_case_now][suite_case_key].value, override=override, clear=clear)


class BasicConfig(BasicCommon):
    __suite_case_label = '__suit_case__'

    def __init__(self):
        super().__init__()
        self._config_config = Config(print_func=self.print)
        self.set_robot_variable('config', self._config_config)

    @robot_log_keyword
    def config_init(self, json_file: str = None):
        self._config_config.init(json_file)

    @robot_log_keyword
    def config_use_label(self, *labels, override=True, clear=False):
        if clear:
            self._config_config.now_clear()
        for label in labels:
            self._config_config.now_use_label(label, override=override)

    @robot_log_keyword
    def config_show_now_value(self):
        self._config_config.show_now_value()

    @robot_log_keyword
    def config_show_now_list(self):
        self._config_config.show_now_list()

    @robot_log_keyword
    def config_use_suite_case_list(self, override=True, clear=False):
        suite_case_now = f'${self.__suite_case_label}'
        if self.__suite_case_label not in self._config_ori:
            self.__config_ori_update(self.__suite_case_label, {})
        suite_case_key = self.get_suite_case_str()
        if suite_case_key not in self._config_ori[suite_case_now]:
            self.config_update_key(suite_case_key, [], self.__suite_case_label)
        self.config_use_label(*self._config_ori[suite_case_now][suite_case_key].value, override=override, clear=clear)
