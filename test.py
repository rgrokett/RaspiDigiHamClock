# Display5a.py
# Test a TM1637 4 digit iDisplay Module
# usage:
# Wire TM1637 
#	5V -- Pin 2 on Pi
#	GND-- Pin 6 
#	CLK-- Pin 40
#	DIO-- Pin 38
#
# $ python test.py
#
# Edit FourDigit() to change pins
#
#


from TM1637 import FourDigit
from time import sleep
        
d = FourDigit(dio=38,clk=40,lum=1)
d.erase()
sleep(2)
d.show("0123")
sleep(3)
d.setColon(True)
d.show("ABCD")
sleep(3)
d.setColon(False)
d.setLuminosity(7) # range 0..7
d.show("donE")
