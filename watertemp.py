#!/usr/bin/env python3
import glob
import time
from pushover import pushover

# 1-wire tutorial followed here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

# enable 1-wire with raspi-config

# make the following connections:
#   DS18B20 DATA    -> RPi GPIO 4, 4.7kOhm pullup resistor
#   DS18B20 VDD     -> RPi 3.3V
#   DS18B20 GND     -> RPi GND


# temp sensor info
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

INTERVAL = 15 # interval in seconds between sensor checks
TEMP_THRESHOLD = 38 # in Farenheit


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_f():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f


temp_reported = False

while True:

    # read temperature
    temp_value = read_temp_f()
    print('TEMP: {:.1f}\xb0F'.format(temp_value))

    # check to see if the temperature dropped below the threshold
    if temp_value < TEMP_THRESHOLD:
        # if this temperature drop is unreported
        if not temp_reported:
            # build message and notify
            notice = '<font color="#ff0000">CRITICAL!</font> Pump house temperature freeze warning: {:.1f}*F'.format(temp_value)
            print(notice)
            pushover(app='water_temp', message=notice, title='**ALERT** Pump House Freeze **ALERT**',
                     users='r_and_j', priority=1, html=True)

        # set this temperature drop as reported
        temp_reported = True
    else:
       # reset the "temp reported" flag
       temp_reported = False

    time.sleep(INTERVAL)
