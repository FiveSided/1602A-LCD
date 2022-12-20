# 1602A
A small library built to run simple functions on the 1602A liquid crystal display

The 160A library is a small library developed by https://github.com/FiveSided.<br>
this library is built to run basic functions on the 1602A LCD<br>

============== Setup ===============
Below are constants you should hookup beforehand
VSS = GND
VDD = Power(5v)
A = Power(5v)
K = GND
V0 (contrast) = GND through a potentiometer or resistor (2kΩ works well)
========== Initialization ==========
lcd4b(db = [], rs = #, en = #)
when creating an lcd4b object, the databus or db keyword is to be assigned a list containing the order of GPIO PIN NUMBERS connected from databuses 4 to 7
the rs keyword is to be assigned the gpio pin number connected to the register select of the LCD
the en keyword is to be assigned the gpio pin number connected to the enable of the LCD
this library does not support reading from cgram or ddram, therefore the rw input on the LCD is to be grounded
============ Functions =============
Write(message) : writes a given string from the cursor's current position
Write_hex(hexa) : writes the character corresponding to the given hexadecimal
move(row, colum) : moves the cursor to the given row and colum
home() : returns the cursor to row 0, colum 0
second_line(): moves the cursor to row 1, colum 0
clear() : clears the display
scroll(delay) : initiates a scroll thread which shifts the display to the left with the given delay
toggle_scroll(state) : pauses or continues scrolling according to the boolean given (True/False)
create_custom(bitmap) : creates a custom charactor when given a bitmap as a list. The bit map must be 5x8 and the 1602A supports 8 charactors at a time.
                        #[!!]home() is called afterwards to exit cgram[!!] Smiley bitmap example: ['00000','00000','01010','00000','10001','01110','00000','00000']
Write_custom(index) : writes the custom character in the given index between 0-7
cursor(state) : enables the visual cursor according to the given boolean (True/False)
cursor_blinking(state) : enables cursor blinking according to the given boolean (True/False)
Instruct(hexadecimal) : sends the given hexadecimal to the LCD as an instruction (functions can be found @ https://www.openhacks.com/uploadsproductos/eone-1602a1.pdf)
execute_hex(hexadecimal) : manages the databuses and enable pin to execute the given hexadecimal to the LCD
