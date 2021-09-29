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

# The leak detection rope is connected as a voltage divider with 2Mohm to ground, and the rope to 3.3V
LEAK_CHANNEL = 0
LEAK_THRESHOLD = 200 # scale of 0-1023


# The pressure sensor is an analog sensor with a range of 0-5 psi
PRESSURE_CHANNEL = 1

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# interval in seconds between sensor checks
INTERVAL = 15



leak_reported = False

while True:
    # read leak detection rope
    leak_value = mcp.read_adc(LEAK_CHANNEL)
    print('LEAK: {}'.format(leak_value))

    # check to see if the leak reading exceeds the threshold
    if leak_value > LEAK_THRESHOLD:
        # if this leak is unreported
        if not leak_reported:
            # build message and notify
            notice = '<font color="#ff0000">CRITICAL!</font> Water leak detected in the pump house (ADC: {0})'.format(leak_value)
            print(notice)
            pushover(app='water_leak', message=notice, title='**ALERT** Water Leak **ALERT**',
                     users='r_and_j', priority=1, html=True)

        # set this leak as reported
        leak_reported = True
    else:
       # reset the "leak reported" flag
       leak_reported = False

    time.sleep(INTERVAL)
