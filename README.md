# RaspiDigiHamClock
Raspberry Pi powered Digital Clock for Amateur Radio using TM1637 4 digit displays

Amateur Radio Operators (aka HAM Radio) use 24 hour UTC (Universal Coordinated Time) for much of their operation.  I decided to build a digital clock using the low-cost TM1637 4 digit displays and a Raspberry Pi Zero W instead of just a GUI clock. (Hardware is fun!)

The TM1637 driven display has four  7 segment leds with a center colon “:” between two sets of digits. It requires two wires to drive the display plus 5V + and Ground for a total of 4 wires. 

For this particular project, I wanted the Raspi to get its time from NTP (Network Time Protocol) servers via the Internet.  I am planning another version of this clock to run on an Arduino Uno and a Real-Time Clock module, for when no WiFi is available and for more portable operation. 

I also wanted the clock to show the Local Time in 12hr and 24hr formats as well as UTC in 12hr and 24hr formats.  The software is designed to let you use just UTC 24hr (typical hams) or different times on up to 4 different displays. 

You can also set the TIME ZONE that you would like to use instead of default Local time.  So each of the four displays could show a different time zone and in 12hr or 24hr format. 

This project does require soldering connectors or wires onto the Pi and/or the tm1637 modules. 

See [RaspiDigiHamClock.pdf](RaspiDigiHamClock.pdf) for full details.


