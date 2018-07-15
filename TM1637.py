# TM1637.py
# Version 1.00

import RPi.GPIO as GPIO
from time import sleep

PATTERN = b'\0\x86\x22\0\0\0\0\x02\0\0\0\0\x04\x40\x80\x52\x3f\x06\x5b\x4f\x66\x6d\x7d\x07\x7f\x6f\0\0\0\x48\0\0\x5d\x77\x7c\x39\x5e\x79\x71\x3d\x76\x30\x0e\x70\x38\x55\x54\x3f\x73\x67\x50\x2d\x78\x3e\x36\x6a\x49\x6e\x1b\x39\x64\x0f\x23\x08\x20\x77\x7c\x58\x5e\x79\x71\x3d\x74\x10\x0c\x70\x30\x55\x54\x5c\x73\x67\x50\x2d\x78\x1c\x36\x6a\x49\x6e\x1b\0\x30\0\x41'

class FourDigit:
    '''
    Abstraction of the 4 digit 7-segment display based on the TM1637 display driver.
    7-bit ASCII characters are mapped as close as possible to the 7 display segments. If a 
    character cannot be mapped, the digit is cleared.
    '''

    myData = [0,0,0,0]
    
    @staticmethod
    def getDisplayableChars():
        '''
        Returns a string with all displayable characters taken from PATTERN dictionary.
        @return: The character set that can be displayed
        '''
        s = "<SPACE>"
        k = 33
        while k < 127:
            ch = chr(k)
            if TM1637.PATTERN[ch] != 0:
                s = s + ch
            k += 1
        return  s

    @staticmethod
    def toHex(intValue):
        '''
        Returns a string with hex digits from given number (>0, any size).
        @param number: the number to convert (must be positive)
        @return: string of hex digits (uppercase), e.g. 0xFE
        '''
        return '%02x' % intValue

    @staticmethod
    def toBytes(intValue):
        '''
        Returns a list of four byte values [byte#24-#31, byte#16-#23, byte#8-#15, byte#0-#7] of given integer.
        @param number: an integer
        @return: list with integers of 4 bytes [MSB,..., LSB]
        '''
        byte0 = intValue & 0xff
        byte1 = (intValue >> 8) & 0xff
        byte2 = (intValue >> 16) & 0xff
        byte3 = (intValue >> 24) & 0xff
        return [byte3, byte2, byte1, byte0]

    @staticmethod
    def toInt(hexValue):
        '''
        Returns an integer from given hex string
        @param number: a string with the number to convert, e.g. "FE" or "fe" or "0xFE" or "0XFE"
        @return: integer number
        '''
        return int(hexValue, 16)
    
    # ------------------- Constructor ---------------------------------        
    def __init__(self, dio = 38, clk = 40, lum = 4):
        '''
        Creates a display instance that uses the two given GPIO pins for data (dio, default: 38) and 
        clock (clk, default: 40).
        It is set to the given luminosiy (0..9, default: 4)
        '''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.clk = clk
        self.dio = dio
        self.lum = lum
        self.colon = False
        self.startPos = 0
        self.text = None
        GPIO.setup(clk, GPIO.OUT)
        GPIO.setup(dio, GPIO.OUT)
        GPIO.output(clk, 0)
        GPIO.output(dio, 0)

    # ------------------- Public methods ---------------------------------        
    def erase(self):
        '''
        Clears the display (all digits are turned off).
        '''
        self.colon = False
        self.show("    ")

    def show(self, text, pos = 0):
        '''
        Displays 4 characters of the given text. The text is considered to be prefixed and postfixed by spaces
        and the 4 character window is selected by the text pointer pos that determines the character displayed at the
        leftmost digit, e.g. (_: empty):
        showText("AbCdEF") -> AbCd
        showText("AbCdEF", 1) -> bCdE
        showText("AbCdEF", -1) ->_AbC
        showText("AbCdEF", 4) -> EF__
        @param text: the text to display (string or integer)
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        '''
        self.startPos = pos
        self.pos = pos
        self.text = str(text)  # digits to chars
        if len(self.text) < 4:
            self.text = "%-4s" % self.text
        self._cropText()
        
    def scroll(self, text):
        '''
        Starts scrolling the text to the left and blocks until all characters have passed by.
        '''
        self.show(text)
        sleep(1.5)
        while self.toLeft() > 0:
            sleep(1)
        sleep(1)    
            
    def toRight(self):
        '''
        Scrolls the current text one step to the left by decreasing the text pointer.
        @return: the number of characters hidden, but remaining to be displayed at the left (>=0); -1, if error
        '''
        if self.text == None:
            return -1
        self.pos -= 1    
        self._cropText()
        return max(0, 4 + self.pos)

    def toLeft(self):
        '''
        Scrolls the current text one step to the left by increasing the text pointer.
        @return: the number of characters hidden, but remaining to be displayed at the right (>=0); -1, if error
        '''
        if self.text == None:
            return -1
        self.pos += 1    
        self._cropText()
        nb = len(self.text) - self.pos
        return max(0, nb)

    def toStart(self):
        '''
        Shows the text at the start position by setting the text pointer to its start value.
        '''
        if self.text == None:
            return -1
        self.pos = self.startPos    
        self._cropText()
       
    def setLuminosity(self, lum):
        '''
        Sets the brightness of the display.
        @param luminosity the brightness (0..9, 0: invisible)
        '''
        self.lum = lum

    def setColon(self, enable):        
        '''
        Enables/disables the colon in the middle of the screen.
        @param enable if True, the colon is shown in all subsequent text operations
        '''
        self.colon = enable
        
    # ------------------- end of public methods ---------------------------------        

    def _cropText(self):
        n = len(self.text)
        data = [' '] * (n + 8)
        for i in range(n):
            data[i + 4] = self.text[i]
        start = max(0, self.pos + 4)
        start = min(start, len(data) - 4)
        end = min(start + n, len(data))
        data = self._toSegment(data[start:end])
        self._prepare(0x40)    
        self._writeByte(0xC0)
        for i in range(4):
            self._writeByte(data[i])
        self._commit()
        
    def _writeByte(self, data):
        for i in range(8):
            GPIO.output(self.clk, 0)
            sleep(0.0001)
            if data & 0x01:
                GPIO.output(self.dio, 1)
            else:
                GPIO.output(self.dio, 0)
            sleep(0.0001)
            data = data >> 1
            GPIO.output(self.clk, 1)
            sleep(0.0001)

        GPIO.output(self.clk, 0)
        GPIO.output(self.dio, 1)
        GPIO.output(self.clk, 1)
        # wait for ACK, no need to set pin as input
        while GPIO.input(self.dio) == 1:
            sleep(0.001)
        sleep(0.001)
    
    def _toSegment(self, text):
        data = []
        msb = 0
        if self.colon:
            msb = 0x80
        for c in text:
            if ord(c) < 32 or ord(c) > 127:
                c = " "
            data.append(ord(PATTERN[ord(c) - 32]) + msb)
        return data

    def _start(self):
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)
        sleep(0.0001)
        GPIO.output(self.dio, 0) 
        GPIO.output(self.clk, 0) 
        sleep(0.0001)
    
    def _stop(self):
        GPIO.output(self.clk, 0) 
        GPIO.output(self.dio, 0) 
        sleep(0.0001)
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)
        sleep(0.0001)
        
    def _prepare(self, addr):        
        self._start()
        self._writeByte(addr)
        self._stop()
        self._start()

    def _commit(self):
        self._stop()
        self._start()
        self._writeByte(0x88 + self.lum)
        self._stop() 
