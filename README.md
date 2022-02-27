# 1602A
A small library built to run simple functions on the 1602A liquid crystal display

The 160A library is a small library developed by https://github.com/FiveSided.<br>
this library is built to run simple functions surrounding the 1602A LCD<br>
========== Initialization ==========<br>
lcd4b(db = [], rs = #, en = #)<br>
when creating an lcd4b object, the databus or db keyword is to be assigned a list containing the order of gpio pin NUMBERS connected from databuses 4 to 7<br>
the rs keyword is be be assigned the gpio pin number connected to the register select of the LCD<br>
the en keyword is be be assigned the gpio pin number connected to the enable of the LCD<br>
this library does not support reading from cgram or ddram, therefore the rw input on the LCD is to be grounded<br>
============ Functions =============<br>
Write(message) : writes a given string from the cursor's current position<br>
Write_hex(hexa) : writes the character corresponding to the given hexadecimal<br>
move(row, colum) : moves the cursor to the given row and colum<br>
home() : returns to cursor to row 0, colum 0<br>
second_line(): moves to cursor to row 1, colum 0<br>
clear() : clears the display<br>
scroll(delay) : initiates a scroll thread which shifts the display to the left accroding to the given delay<br>
toggle_scroll(state) : pauses or continues scrolling according to the boolean given (True/False)<br>
create_custom(bitmap) : creates a custom charactor when given a bitmap as a list. The bit map must be 5x8 and the 1602a supports 8 charactors at a time.<br>
                        [!!]home() is called afterwards to exit cgram[!!] Smiley bitmap example: ['00000','00000','01010','00000','10001','01110','00000','00000']<br>
Write_custom(index) : writes the custom character in the given index which are indexes 0-7<br>
cursor(state) : enables the visual cursor according to the given boolean (True/False)<br>
cursor_blinking(state) : enables cursor blinking according to the given boolean (True/False)<br>
Instruct(hexadecimal) : sends the given hexadecimal to the LCD as an instruction (functions can be found @ https://www.openhacks.com/uploadsproductos/eone-1602a1.pdf)<br>
execute_hex(hexadecimal) : manages the databuses and enable pin to execute the given hexadecimal to the LCD<br>
