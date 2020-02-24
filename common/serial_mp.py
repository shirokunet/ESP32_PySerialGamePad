#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import json
import logging
import serial
import serial.tools.list_ports
import time
from multiprocessing import Process, Value, Array


class SerilaMp():
    def __init__(self, logger, tx_size=6, rx_size=3, port='/dev/ttyUSB0', baud=115200, timeout=0.1):
        self._logger = logger
        self.is_run = Value(ctypes.c_bool, False)

        self._tx_size = tx_size
        self._rx_size = rx_size

        # communication variables
        self.a_tx = Array('i', [0] * self._tx_size)
        self.a_rx = Array('i', [0] * self._rx_size)

        # try to open com port
        try:
            if port == 'auto':
                use_port = self._search_com_port()
            else:
                use_port = port
            self._logger.debug('Open Serial COM Port')
            self._ser = serial.Serial(use_port, baud, timeout=timeout)
            self._ser.readline()
            # dummy message to clear buffer
            self._ser.write(b'\n')
        except:
            self._logger.error('Serial COM Port Open Error')
            return

        # start process
        self.is_run.value = True
        self._p = Process(target=self._process, args=())
        self._p.start()

    def close(self):
        self.is_run.value = False

    def _search_com_port(self):
        coms = serial.tools.list_ports.comports()
        comlist = []
        for com in coms:
            comlist.append(com.device)
        self._logger.debug('Connected COM ports: ' + str(comlist))

        if len(comlist) > 0:
            use_port = comlist[0]
            self._logger.debug('Use COM port: ' + use_port)
        else:
            use_port = False
            self._logger.debug('Could not find COM port')
        return use_port

    def _process(self):
        try:
            while self.is_run.value:
                # receive task
                string_data = self._ser.readline().decode('utf-8')
                dlist = string_data.split(',')
                if dlist[0] == '#' and len(dlist) == self._rx_size+2:
                    for i in range(0, self._rx_size):
                        self.a_rx[i] = int(dlist[i+1])
                # else:
                #     self._logger.error('--- Unexpected Rx Data ---')
                #     self._logger.error(len(dlist))
                #     self._logger.error(dlist)

                # send task
                send_msg = '#,'
                for i in range(0, self._tx_size):
                    send_msg += str(self.a_tx[i])
                    send_msg += ','
                send_msg += '\n'
                self._ser.write(send_msg.encode())

                time.sleep(0.01)
        except:
            self.is_run.value = False
        self._ser.close()

if __name__ == '__main__':
    logger_main = logging.getLogger('main')
    logger_main.setLevel(logging.DEBUG)
 
    formatter = logging.Formatter('[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger_main.addHandler(sh)

    serial_mp = SerilaMp(logger_main, tx_size=6, rx_size=3, port='/dev/ttyUSB0', baud=115200)

    try:
        counter = 0

        # z1
        console_time_z1 = time.time()

        # main loop
        while serial_mp.is_run.value:
            time_now = time.time()

            for i in range(0, 6):
                serial_mp.a_tx[i] = counter + i
            counter += 1

            # debug console
            if time_now - console_time_z1 > 0.1:
                console_time_z1 = time_now
                logger_main.debug(serial_mp.a_tx[:])
                logger_main.debug(serial_mp.a_rx[:])

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    serial_mp.close()
