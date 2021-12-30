#!/usr/bin/env python3

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from pushover import pushover

# SPI library pulled from: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
# install with:
# sudo apt-get install python3-pip
# sudo pip3 install adafruit-mcp3008

# 1-wire tutorial followed here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

# enable SPI and 1-wire with raspi-config

# make the following connections:
#   MCP3008 VDD     -> RPi 3.3V
#   MCP3008 VREF    -> RPi 3.3V
#   MCP3008 AGND    -> RPi GND
#   MCP3008 DGND    -> RPi GND
#   MCP3008 CLK     -> RPi SCLK
#   MCP3008 DOUT    -> RPi MISO
#   MCP3008 DIN     -> RPi MOSI
#   MCP3008 CS/SHDN -> RPi CE0

# The leak detection ropes are each connected as a voltage divider with 2Mohm to ground, and the rope to 3.3V
LEAK1_CHANNEL = 0 # water pump
LEAK2_CHANNEL = 3 # irrigation
LEAK_THRESHOLD = 200 # scale of 0-1023


# The pressure sensor is an analog sensor with a range of 0-5 psi
PRESSURE_CHANNEL = 1

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# interval in seconds between sensor checks
INTERVAL = 15


leak1_reported = False
leak2_reported = False

while True:
    # read leak detection ropes
    leak1_value = mcp.read_adc(LEAK1_CHANNEL)
    leak2_value = mcp.read_adc(LEAK2_CHANNEL)
    print('LEAK1: {}'.format(leak1_value))
    print('LEAK2: {}'.format(leak2_value))

    ### LEAK 1 ###
    # check to see if the leak readings exceed the threshold
    if leak1_value > LEAK_THRESHOLD:
        # if this leak is unreported
        if not leak1_reported:
            # build message and notify
            notice = '<font color="#ff0000">CRITICAL!</font> Water leak detected near pump and filters (ADC: {0})'.format(leak1_value)
            print(notice)
            pushover(app='water_leak', message=notice, title='**ALERT** Water Leak **ALERT**',
                     users='r_and_j', priority=1, html=True)

        # set this leak as reported
        leak1_reported = True
    else:
       # reset the "leak reported" flag
       leak1_reported = False

    ### LEAK 2 ###
    # check to see if the leak readings exceed the threshold
    if leak2_value > LEAK_THRESHOLD:
        # if this leak is unreported
        if not leak2_reported:
            # build message and notify
            notice = '<font color="#ff0000">CRITICAL!</font> Water leak detected near irrigation valves (ADC: {0})'.format(leak2_value)
            print(notice)
            pushover(app='water_leak', message=notice, title='**ALERT** Water Leak **ALERT**',
                     users='r_and_j', priority=1, html=True)

        # set this leak as reported
        leak2_reported = True
    else:
       # reset the "leak reported" flag
       leak2_reported = False

    time.sleep(INTERVAL)
