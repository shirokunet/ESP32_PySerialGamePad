#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import time
import yaml
from common.gamepad_mp import GamePadMp
from common.serial_mp import SerilaMp
from common.set_logging import set_logging


def main():
    try:
        # get yaml config file
        ymlfile = open('config.yml')
        cfg = yaml.load(ymlfile)
        ymlfile.close()

        # logging setting
        logger_main = set_logging('main', cfg_log_level=cfg['log_level'])

        # instance setting
        gamepad_mp = GamePadMp(logger_main)
        serial_mp = SerilaMp(logger_main, port=cfg['ino_port'], baud=cfg['ino_baud'])
        logger_main.debug('GamePad: {}'.format(gamepad_mp.is_run.value))
        logger_main.debug('Serial: {}'.format(serial_mp.is_run.value))

        # z1
        console_time_z1 = time.time()

        # main loop
        while gamepad_mp.is_run.value and serial_mp.is_run.value:
            time_now = time.time()

            # update sensors
            gp_data = gamepad_mp.status_dict.copy()

            serial_mp.a_tx[0] = gp_data['jXL']
            serial_mp.a_tx[1] = gp_data['jYL']
            serial_mp.a_tx[2] = gp_data['jXR']
            serial_mp.a_tx[3] = gp_data['jYR']
            serial_mp.a_tx[4] = gp_data['bLB']
            serial_mp.a_tx[5] = gp_data['bRB']

            # debug console
            if time_now - console_time_z1 > cfg['debug_console_interval']:
                console_time_z1 = time_now
                logger_main.debug(json.dumps(gp_data))
                logger_main.debug(serial_mp.a_rx[:])
                logger_main.debug('\n')

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    gamepad_mp.close()
    logger_main.debug('End Program')


if __name__ == '__main__':
    main()
