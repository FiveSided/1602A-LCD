#The 160A library is a small library developed by https://github.com/FiveSided.
#this library is built to run basic commands on the 1602A LCD
#============== Setup ===============
#Below are constants you should hookup beforehand
#VSS = GND
#VDD = Power(5v)
#A = Power(5v)
#K = GND
#V0 (contrast) = GND through a potentiometer or resistor (2kΩ works well)
#========== Initialization ==========
#lcd4b(db = [], rs = #, en = #)
#when creating an lcd4b object, the databus or db keyword is to be assigned a list containing the order of GPIO PIN NUMBERS connected from databuses 4 to 7
#the rs keyword is to be assigned the gpio pin number connected to the register select of the LCD
#the en keyword is to be assigned the gpio pin number connected to the enable of the LCD
#this library does not support reading from cgram or ddram, therefore the rw input on the LCD is to be grounded
#============ Functions =============
#Write(message) : writes a given string from the cursor's current position
#Write_hex(hexa) : writes the character corresponding to the given hexadecimal
#move(row, colum) : moves the cursor to the given row and colum
#home() : returns the cursor to row 0, colum 0
#second_line(): moves the cursor to row 1, colum 0
#clear() : clears the display
#scroll(delay) : initiates a scroll thread which shifts the display to the left with the given delay
#toggle_scroll(state) : pauses or continues scrolling according to the boolean given (True/False)
#create_custom(bitmap) : creates a custom charactor when given a bitmap as a list. The bit map must be 5x8 and the 1602A supports 8 charactors at a time.
                        #[!!]home() is called afterwards to exit cgram[!!] Smiley bitmap example: ['00000','00000','01010','00000','10001','01110','00000','00000']
#Write_custom(index) : writes the custom character in the given index between 0-7
#cursor(state) : enables the visual cursor according to the given boolean (True/False)
#cursor_blinking(state) : enables cursor blinking according to the given boolean (True/False)
#Instruct(hexadecimal) : sends the given hexadecimal to the LCD as an instruction (functions can be found @ https://www.openhacks.com/uploadsproductos/eone-1602a1.pdf)
#execute_hex(hexadecimal) : manages the databuses and enable pin to execute the given hexadecimal to the LCD

from machine import Pin
import utime
import _thread

class lcd4b():
    
    def __init__(self, **Pins):
        self.DataBuses = Pins['db']
        self.RS = Pins['rs']
        self.EN = Pins['en']
        
        self.custom_chars = []
        self.scrollable = False
    
        self.RS = Pin(self.RS, Pin.OUT)
        self.EN = Pin(self.EN, Pin.OUT, Pin.PULL_DOWN)
        
        for index, pinNum in enumerate(self.DataBuses):
            self.DataBuses[index] = Pin(pinNum, Pin.OUT, Pin.PULL_DOWN)
        
        self.Instruct(0x02)#set to 4-bit mode
        self.Instruct(0x0c)#display on
        self.Instruct(0x01)#clear display
        self.Instruct(0x82)#2-line mode
        self.Instruct(0x02)#return home
        
    def execute_hex(self, hexadecimal):
        self.scrollable = False
        binary = list(f'{hexadecimal:0>{8}b}')
        self.EN.value(0)
        
        for x in range(0,4):
            self.DataBuses[x].value(int(binary[3 - x]))
        
        self.EN.value(1)
        self.EN.value(0)
        
        for x in range(0,4):
            self.DataBuses[x].value(int(binary[(4 - x) + 3]))
        
        self.EN.value(1)
        self.EN.value(0)
        self.scrollable = True
        
    def Write(self, message):
        self.scrollable = False
        self.RS.value(1)
        for c in message:
            hexi = hex(ord(c))
            self.execute_hex(int(hexi))
    
    def Write_hex(self, hexidecimal):
        self.scrollable = False
        self.RS.value(1)
        self.execute_hex(hexidecimal)
    
    def Instruct(self, hexadecimal):
        self.scrollable = False
        self.RS.value(0)
        self.execute_hex(hexadecimal)
    
    def cursor(self, state):
        if state == True:
            self.Instruct(0x0e)#cursor on
        else:
            self.Instruct(0x0c)#cursor off
    
    def cursor_blinking(self, state):
        if state == True:
            self.Instruct(0x0f)#cursor blinking on
        else:
            self.Instruct(0x0e)#cursor blinking off
            
    def home(self):
        self.Instruct(0x02)#go to home
    
    def second_line(self):
        self.Instruct(0xc0)#go to line 2
        
    def clear(self):
        self.Instruct(0x01)#clear display
        
    def create_custom(self, bitarray):
        display.Instruct(0x40)#select cgram
        self.custom_chars.append(bitarray)
        
        for char_array in self.custom_chars:
            for row in char_array:
                hexa = hex(int(row, 2))
                self.Write_hex(int(hexa, 16))
        self.home()
    
    def Write_custom(self, index):
        self.Write_hex(int('0x0' + str(index), 16))
        
    def move(self, row, colum):
        if row == 0:
            self.home()
        else:
            self.second_line()
            
        for x in range(colum):
            self.Instruct(0x14)#shift cursor to the right
    
    def toggle_scroll(self, state):
        self.scrollable = state
    
    def scroll(self, delay):
        self.scrollable = True
        def scroll(hexa):
            while 1:
                utime.sleep(delay)
                if self.scrollable:
                    self.Instruct(hexa)
        
        _thread.start_new_thread(scroll, (0x18,))
