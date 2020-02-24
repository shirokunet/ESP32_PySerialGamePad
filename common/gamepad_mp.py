#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
from enum import IntEnum
from lib.inputs.inputs import DeviceManager
from multiprocessing import Process, Value, Manager


class GamePadMp():
    """
    This Class is for a Logicool Gampad F310
    The switch should be D instead of X.
    The mode LED should be OFF.
    """
    def __init__(self, logger):
        self._logger = logger
        self.is_run = Value(ctypes.c_bool, False)

        # communication variables
        self._m = Manager()
        self.status_dict = self._m.dict({
            'jXL': 0, \
            'jYL': 0, \
            'jXR': 0, \
            'jYR': 0, \
            'bLB': 0, \
            'bRB': 0
        })
        self._keycode_to_name_dict = self._m.dict({
            0: 'jXL', \
            1: 'jYL', \
            2: 'jXR', \
            5: 'jYR', \
            292: 'bLB', \
            293: 'bRB'
        })

        # z1
        self._data_z1 = None

        # try to connect gamepad
        try:
            devices = DeviceManager()
            self.gp_dict_code = devices.codes['Absolute']
            self.gp_dict_code.update(devices.codes['Key'])
            self._gamepad = devices.gamepads[0]
        except:
            self._logger.error("No gamepad found.")
            return

        # start process
        self.is_run.value = True
        self._p = Process(target=self._process, args=())
        self._p.start()
        return

    def close(self):
        self.is_run.value = False

    def is_up(self, data, key):
        if self._data_z1 == None:
            self._data_z1 = data
            return False
        elif self._data_z1[key] == 0 and data[key] == 1:
            self._data_z1 = data
            return True
        else:
            self._data_z1 = data
            return False

    def get_keys_from_value(self, d, val):
        return [k for k, v in d.items() if v == val]

    def _process(self):
        try:
            while self.is_run.value:
                events = self._gamepad.read()
                for event in events:
                    if event.ev_type == 'Sync':
                        continue
                    elif event.code == 'MSC_SCAN':
                        continue
                    try:
                        key = self.get_keys_from_value(self.gp_dict_code, event.code)[0]
                        self.status_dict[self._keycode_to_name_dict[key]] = event.state
                    except:
                        self._logger.error('Could not find {} in self._keycode_to_name_dict'.format(event.code))
        except:
            self._logger.error('Close GamePad Process')
            self.is_run.value = False
