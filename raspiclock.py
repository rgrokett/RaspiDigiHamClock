#!/bin/python
# RaspiDigiClock using TM1637 modules
# Designed to run up to 4 modules
#
# Use the raspidigiclock.ini file to set number of 
# modules, Timezone, 12/24 hr clock
#
# When running, you should see the colon blinking once per second
#

import os
import time
from ConfigParser import SafeConfigParser
from TM1637 import FourDigit
        

# USER VARIABLES FROM .ini CONFIG FILE
config = SafeConfigParser()
config.read("/home/pi/RaspiDigiHamClock/raspiclock.ini")

# Number of TM1637 modules
NUM_MODS = config.getint('CLOCK', 'Num_modules')

# Timezones
tmz = []
tmz.append(config.get('CLOCK', 'TZ1'))
tmz.append(config.get('CLOCK', 'TZ2'))
tmz.append(config.get('CLOCK', 'TZ3'))
tmz.append(config.get('CLOCK', 'TZ4'))

# Convert 'Local' to current system timezone
with open('/etc/timezone') as f:
    TZ = f.readline().strip()
for x in range(0,NUM_MODS):
    # Get System 'Local' time zone
    if tmz[x] == 'Local':
	tmz[x] = TZ

# 12/24 Hour
mil = []
mil.append(config.get('CLOCK', 'HR1'))
mil.append(config.get('CLOCK', 'HR2'))
mil.append(config.get('CLOCK', 'HR3'))
mil.append(config.get('CLOCK', 'HR4'))

# Initialize 4 modules, even if not all are avail
# This uses the GPIO BOARD PINS (1 thru 40)
disp = []
disp.append(FourDigit(dio=38,clk=40,lum=1))
disp.append(FourDigit(dio=35,clk=37,lum=1))
disp.append(FourDigit(dio=32,clk=36,lum=1))
disp.append(FourDigit(dio=31,clk=33,lum=1))

showColon = True



# DISPLAY TIME ON ONE MODULE
def displayTM(disp,tim,hrs,colon):
    hour = tim.tm_hour
    minute = tim.tm_min
    if hrs == '12':
        hour = (tim.tm_hour % 12) or 12
    disp.show("%02d%02d" %(hour, minute))
    disp.setColon(colon)


# MAIN LOOP
while True:
    for x in range(0,NUM_MODS):
	# Get Current Time for time zone
	cur=time.time()
	os.environ["TZ"]=tmz[x]
	time.tzset()
	ct = time.localtime(cur)
    	displayTM(disp[x],ct,mil[x],showColon)

    time.sleep(0.5)
    showColon = not showColon

