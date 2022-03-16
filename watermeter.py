#!/usr/bin/env python3

import time
import pigpio
from pushover import pushover

# inspiration from: https://www.raspberrypi.org/forums/viewtopic.php?t=243193
# install GPIO library with:
#   sudo apt-get install pigpio python-pigpio python3-pigpio
#   sudo systemctl enable pigpiod
#   sudo systemctl start pigpiod

# make the following connections:
#   meter connected to GND and GPIO w/ 1K into GPIO, 10K pullup to 3.3V

POTABLE_METER_GPIO = 23
IRRIGATION_METER_GPIO = 24
SECURITY_GPIO = 25

INTERVAL=3

# init GPIO
pi = pigpio.pi()
if not pi.connected:
    exit()
# debounce inputs
pi.set_glitch_filter(POTABLE_METER_GPIO,1000)
pi.set_glitch_filter(IRRIGATION_METER_GPIO,1000)
pi.set_glitch_filter(SECURITY_GPIO,1000)

potable_cb = pi.callback(POTABLE_METER_GPIO)
irrigation_cb = pi.callback(IRRIGATION_METER_GPIO)
security_cb = pi.callback(SECURITY_GPIO)

while True:
    potable_now = potable_cb.tally()
    irrigation_now = irrigation_cb.tally()
    security_now = security_cb.tally()
    print('PRESSED: {0} (pot)/{1} (irr)/{2} (sec) times'.format(potable_now, irrigation_now, security_now))
    time.sleep(INTERVAL)

## build message and notify
#notice = '<font color="#ff0000">CRITICAL!</font> Water leak detected in the pump house (ADC: {0})'.format(leak_value)
#print(notice)
#pushover(app='water_leak', message=notice, title='**ALERT** Water Leak **ALERT**',
#         users='r_and_j', priority=1, html=True)
