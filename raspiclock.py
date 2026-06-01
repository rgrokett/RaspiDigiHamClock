#!/usr/bin/env python3
# RaspiDigiClock using TM1637 modules
# Designed to run up to 4 modules
#
# Requires Python 3.11+
#
# Use the raspidigiclock.ini file to set number of 
# modules, Timezone, 12/24 hr clock
#
# When running, you should see the colon blinking once per second
#

import os
import time
from configparser import ConfigParser
from TM1637 import FourDigit

CONFIG_PATH = "/home/pi/RaspiDigiHamClock/raspiclock.ini"
MAX_MODULES = 4


def read_config(path=CONFIG_PATH):
    config = ConfigParser()
    loaded = config.read(path)
    if not loaded:
        raise RuntimeError("Unable to read config file: %s" % path)
    if not config.has_section('CLOCK'):
        raise RuntimeError("Missing [CLOCK] section in %s" % path)
    return config


def get_local_timezone():
    with open('/etc/timezone') as f:
        return f.readline().strip()


def get_clock_settings(config):
    debug = config.getint('CLOCK', 'debug')
    num_mods = config.getint('CLOCK', 'num_modules')
    if num_mods < 1 or num_mods > MAX_MODULES:
        raise ValueError("num_modules must be between 1 and %d" % MAX_MODULES)

    local_tz = get_local_timezone()
    timezones = []
    hours = []
    dio_pins = []
    clk_pins = []
    for index in range(1, num_mods + 1):
        timezone = config.get('CLOCK', 'TZ%d' % index).strip()
        if timezone.lower() == 'local':
            timezone = local_tz
        timezones.append(timezone)

        hour_format = config.get('CLOCK', 'HR%d' % index).strip()
        if hour_format not in ('12', '24'):
            raise ValueError("HR%d must be either 12 or 24" % index)
        hours.append(hour_format)

        dio_pins.append(config.getint('CLOCK', 'DIO%d' % index))
        clk_pins.append(config.getint('CLOCK', 'CLK%d' % index))

    luminosity = config.getint('CLOCK', 'LUM')
    if luminosity < 0 or luminosity > 7:
        raise ValueError("LUM must be between 0 and 7")

    return debug, num_mods, timezones, hours, luminosity, dio_pins, clk_pins


# DISPLAY TIME ON ONE MODULE
def displayTM(disp, tim, hrs, colon, debug=False):
    if debug:
        print("displayTM()")
    hour = tim.tm_hour
    minute = tim.tm_min
    if hrs == '12':
        hour = (tim.tm_hour % 12) or 12
    disp.show("%02d%02d" %(hour, minute))
    disp.setColon(colon)


def main():
    config = read_config()
    debug, num_mods, timezones, hours, luminosity, dio_pins, clk_pins = get_clock_settings(config)

    if debug:
        print("Initializing...")

    # This uses the GPIO BOARD PINS (1 thru 40).
    displays = []
    for index in range(num_mods):
        displays.append(FourDigit(dio=dio_pins[index], clk=clk_pins[index], lum=luminosity))

    if debug:
        print("Number of modules = " + str(num_mods))
        print("Starting clock loop...")

    show_colon = True

    while True:
        for index in range(num_mods):
            if debug:
                print("Module#" + str(index + 1))
            cur = time.time()
            os.environ["TZ"] = timezones[index]
            time.tzset()
            ct = time.localtime(cur)
            try:
                displayTM(displays[index], ct, hours[index], show_colon, debug)
            except OSError as exc:
                if debug:
                    print("Module#" + str(index + 1) + " error: " + str(exc))

        time.sleep(0.5)
        show_colon = not show_colon


if __name__ == '__main__':
    main()
