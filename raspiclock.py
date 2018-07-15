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

# Debug mode 0/1
DEBUG = config.getint('CLOCK', 'debug')

if DEBUG: print "Initializing..."

# Number of TM1637 modules
NUM_MODS = config.getint('CLOCK', 'num_modules')

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
    if tmz[x].lower() == 'local':
	tmz[x] = TZ

# 12/24 Hour
mil = []
mil.append(config.get('CLOCK', 'HR1'))
mil.append(config.get('CLOCK', 'HR2'))
mil.append(config.get('CLOCK', 'HR3'))
mil.append(config.get('CLOCK', 'HR4'))

# Brightness
l = config.getint('CLOCK', 'LUM')

# Initialize 4 modules, even if not all are avail
# This uses the GPIO BOARD PINS (1 thru 40)
d = []
d.append(config.getint('CLOCK', 'DIO1'))
d.append(config.getint('CLOCK', 'DIO2'))
d.append(config.getint('CLOCK', 'DIO3'))
d.append(config.getint('CLOCK', 'DIO4'))

c = []
c.append(config.getint('CLOCK', 'CLK1'))
c.append(config.getint('CLOCK', 'CLK2'))
c.append(config.getint('CLOCK', 'CLK3'))
c.append(config.getint('CLOCK', 'CLK4'))

disp = []
for x in range(0,NUM_MODS):
    disp.append(FourDigit(dio=d[x],clk=c[x],lum=l))

showColon = True

if DEBUG: print "Number of modules = "+str(NUM_MODS)

if DEBUG: print "Starting clock loop..."


# DISPLAY TIME ON ONE MODULE
def displayTM(disp,tim,hrs,colon):
    if DEBUG: print "displayTM()"
    hour = tim.tm_hour
    minute = tim.tm_min
    if hrs == '12':
        hour = (tim.tm_hour % 12) or 12
    disp.show("%02d%02d" %(hour, minute))
    disp.setColon(colon)


# MAIN LOOP
while True:
    for x in range(0,NUM_MODS):
	if DEBUG: print "Module#"+str(x+1)
	# Get Current Time for desired timezone
	cur=time.time()
	os.environ["TZ"]=tmz[x]
	time.tzset()
	ct = time.localtime(cur)
    	displayTM(disp[x],ct,mil[x],showColon)

    time.sleep(0.5)
    showColon = not showColon

