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


class ConfigItem:
    def __init__(self, value: Any, source: str):
        self._value: Any = value
        self._root: str = source
        self._source: str = source

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


class BasicConfig(BasicCommon):
    __suit_case_label = '__suit_case__'

    def __init__(self):
        super().__init__()
        self._config_path = Path('config.json')
        self._config_ori: Dict[str, Dict[str, Any]] = {}
        self._config_now: Dict[str, ConfigItem] = {}
        self._config_label_list: List[str] = []
        self.set_robot_variable('config', self._config_now)

    def config_init(self, json_file: str):
        self._config_path = Path(json_file)
        if not self._config_path.is_file():
            self._config_path.touch()
        with self._config_path.open(mode='r') as f:
            config_text = f.read()
            config_dict = json.loads(config_text)
        self.__config_ori_init(config_dict)
        self._config_now.clear()
        self._config_label_list = []

    def __config_ori_init(self, config_dict: Dict[str, Dict[str, Any]]):
        self._config_ori = {}
        for i, v in config_dict.items():
            if i.startswith('$'):
                continue
            else:
                self.__config_ori_update(i, v, file=False)

    def __config_ori_update(self, label: str, kv_dict: Dict[str, Any], override=True, file=True):
        label_now = f'${label}'
        self._config_ori[label] = {}
        self._config_ori[label_now] = {}
        for i, v in kv_dict.items():
            self._config_ori[label][i] = v
            if i == '__inherit__':
                v_now = f'${v}'
                if v in self._config_ori and v_now in self._config_ori:
                    for j, w in self._config_ori[v_now].items():
                        if override:
                            self._config_ori[label_now][j] = w.inherit(label)
                        else:
                            self._config_ori[label_now].setdefault(j, w.inherit(label))
                else:
                    raise KeyError(f'config "{label}" try to inherit "{v}" which does not exist.')
            else:
                self._config_ori[label_now][i] = ConfigItem(v, label)
        if file:
            self.__config_write_file()

    def __config_write_file(self):
        temp_dict = {_k: _v for _k, _v in self._config_ori.items() if not _k.startswith('$')}
        with self._config_path.open(mode='w') as f:
            json.dump(temp_dict, f)

    def config_use_label(self, *labels, override=True, clear=False):
        if clear:
            self._config_now.clear()
            self._config_label_list = []
        for label in labels:
            label_now = f'${label}'
            if label in self._config_ori and label_now in self._config_ori:
                self._config_label_list.append(label)
                for i, v in self._config_ori[label_now].items():
                    if override:
                        self._config_now[i] = v
                    else:
                        self._config_now.setdefault(i, v)

    def config_update_key(self, key, value, label=None, ori=True):
        self._config_now[key] = ConfigItem(value, label)
        if ori:
            self._config_ori[label][key] = value
            with self._config_path.open(mode='w') as f:
                json.dump(self._config_ori, f)

    def config_show_now_value(self):
        for i, v in self._config_now.items():
            self.print(f'{i} : {v.value} [from {v.source} & root {v.root}]')

    def config_show_now_list(self):
        self.print(f'now config contains :[{",".join(self._config_label_list)}]')

    def config_use_suit_case_list(self, override=True, clear=False):
        suit_case_now = f'${self.__suit_case_label}'
        if self.__suit_case_label in self._config_ori and suit_case_now in self._config_ori:
            suit_case_key = self.get_suit_case_str()
            self._config_ori[suit_case_now].setdefault(suit_case_key, [])
            if suit_case_key in self._config_ori[suit_case_now]:
                self.config_use_label(*self._config_ori[suit_case_now][suit_case_key], override=override, clear=clear)

