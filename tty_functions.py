#sloppily writen by OK1GAL 2024

import sys
import signal
import platform
import serial
import re
current_platform = platform.system()

if current_platform == "Windows":
    print("OS suported")
else:
    if current_platform == "Linux":
        print("OS suported")
    else:
        print("no TTY for you, use normal platform\n")
        sys.exit()


# Baudot code lookup tables
LETTERS_TO_BAUDOT = {
    'A': 0b00011, 'B': 0b11001, 'C': 0b01110, 'D': 0b01001, 'E': 0b00001,
    'F': 0b01101, 'G': 0b11010, 'H': 0b10100, 'I': 0b00110, 'J': 0b01011,
    'K': 0b01111, 'L': 0b10010, 'M': 0b11100, 'N': 0b01100, 'O': 0b11000,
    'P': 0b10110, 'Q': 0b10111, 'R': 0b01010, 'S': 0b00101, 'T': 0b10000,
    'U': 0b00111, 'V': 0b11110, 'W': 0b10011, 'X': 0b11101, 'Y': 0b10101,
    'Z': 0b10001, ' ': 0b00100, '\n':0b00010, '\r':0b01000 
}
# Corrected FIGURES_TO_BAUDOT mapping
FIGURES_TO_BAUDOT = {
    '1': 0b10111, '2': 0b10011, '3': 0b00001, '4': 0b01010, '5': 0b10000,
    '6': 0b10101, '7': 0b00111, '8': 0b00110, '9': 0b11000, '0': 0b10110,
    '-': 0b00011, "'": 0b00101, '!': 0b01111, '&': 0b11111, '#': 0b11011,
    '(': 0b01111, ')': 0b10010, ':': 0b01110, ',': 0b01100, '?': 0b11001,
    '+': 0b01101, '/': 0b11101, '=': 0b11110, '.': 0b11100, ' ': 0b00100,
    '\n':0b00010, '\r':0b01000 
}

# Inverted Baudot code lookup tables
"""
BAUDOT_TO_LETTERS = {
    0b00011: 'A', 0b11001: 'B', 0b01110: 'C', 0b01001: 'D', 0b00001: 'E',
    0b01101: 'F', 0b11010: 'G', 0b10100: 'H', 0b00110: 'I', 0b01011: 'J',
    0b01111: 'K', 0b10010: 'L', 0b11100: 'M', 0b01100: 'N', 0b11000: 'O',
    0b10110: 'P', 0b10111: 'Q', 0b01010: 'R', 0b00101: 'S', 0b10000: 'T',
    0b00111: 'U', 0b11110: 'V', 0b10011: 'W', 0b11101: 'X', 0b10101: 'Y',
    0b10001: 'Z', 0b00100: ' ', 0b00010: '\n', 0b01000: '\r'
}

BAUDOT_TO_FIGURES = {
    0b10111: '1', 0b10011: '2', 0b00001: '3', 0b01010: '4', 0b10000: '5',
    0b10101: '6', 0b00111: '7', 0b00110: '8', 0b11000: '9', 0b10110: '0',
    0b00011: '-', 0b11101: "'", 0b01111: '!', 0b11111: '&', 0b11011: '#',
    0b11100: '(', 0b01110: ')', 0b01100: ':', 0b00101: '?', 0b01101: '+',
    0b11010: '/', 0b11110: '=', 0b11110: '.', 0b00100: ' ', 0b00010: '\n',
    0b01000: '\r', 0b01011: chr(7)
}"""

# Inverted Baudot code lookup tables
BAUDOT_TO_LETTERS = {
    b'\x03': 'A', b'\x19': 'B', b'\x0E': 'C', b'\x09': 'D', b'\x01': 'E',
    b'\x0D': 'F', b'\x1A': 'G', b'\x14': 'H', b'\x06': 'I', b'\x0B': 'J',
    b'\x0F': 'K', b'\x12': 'L', b'\x1C': 'M', b'\x0C': 'N', b'\x18': 'O',
    b'\x16': 'P', b'\x17': 'Q', b'\x0A': 'R', b'\x05': 'S', b'\x10': 'T',
    b'\x07': 'U', b'\x1E': 'V', b'\x13': 'W', b'\x1D': 'X', b'\x15': 'Y',
    b'\x11': 'Z', b'\x04': ' ', b'\x02': '\n', b'\x08': '\r'
}

BAUDOT_TO_FIGURES = {
    b'\x17': '1', b'\x13': '2', b'\x01': '3', b'\x0A': '4', b'\x10': '5',
    b'\x15': '6', b'\x07': '7', b'\x06': '8', b'\x18': '9', b'\x16': '0',
    b'\x03': '-', b'\x05': "'", b'\x0F': '!', b'\x1F': '&', b'\x1B': '#',
    b'\x0F': '(', b'\x12': ')', b'\x0E': ':', b'\x0C': ',', b'\x19': '?',
    b'\x0D': '+', b'\x1D': '/', b'\x1E': '=', b'\x1C': '.', b'\x04': ' ',
    b'\x02': '\n', b'\x08': '\r'
}



TAPE_ALPHABET = {
    'A':[0b11100, 0b01110, 0b00101, 0b00101, 0b01110, 0b11100, 0b00000],
    'B':[0b11111, 0b10101, 0b10101, 0b01010, 0b00000],
    'C':[0b01110, 0b10001, 0b10001, 0b01010, 0b00000],
    'D':[0b11111, 0b10001, 0b10001, 0b01110, 0b00000],
    'E':[0b11111, 0b10101, 0b10101, 0b00000],
    'F':[0b11111, 0b00101, 0b00101, 0b00000],
    'G':[0b01110, 0b10001, 0b10101, 0b01100, 0b00000],
    'H':[0b11111, 0b00100, 0b00100, 0b11111, 0b00000],
    'I':[0b10001, 0b11111, 0b10001, 0b00000],
    'J':[0b01000, 0b10001, 0b01111, 0b00000],
    'K':[0b11111, 0b00100, 0b01010, 0b10001, 0b00000],
    'L':[0b11111, 0b10000, 0b10000, 0b10000, 0b00000],
    'M':[0b11111, 0b00010, 0b00100, 0b00100, 0b00010, 0b11111, 0b00000],
    'N':[0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111, 0b00000],
    'O':[0b01110, 0b10001, 0b10001, 0b01110, 0b00000],
    'P':[0b11111, 0b00101, 0b00101, 0b00010, 0b00000],
    'Q':[0b01110, 0b10001, 0b10001, 0b01110, 0b10000, 0b00000],
    'R':[0b11111, 0b00101, 0b01101, 0b10010, 0b00000],
    'S':[0b00010, 0b10101, 0b10101, 0b01000, 0b00000],
    'T':[0b00001, 0b00001, 0b11111, 0b00001, 0b00001, 0b00000],
    'U':[0b01111, 0b10000, 0b10000, 0b01111, 0b00000],
    'V':[0b00011, 0b01100, 0b10000, 0b01100, 0b00011, 0b00000],
    'W':[0b00011, 0b01100, 0b10000, 0b01100, 0b10000, 0b01100, 0b00011, 0b00000],
    'X':[0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b00000],
    'Y':[0b00001, 0b00010, 0b11100, 0b00010, 0b00001, 0b00000],
    'Z':[0b10011, 0b10101, 0b11001, 0b00000],
    ' ':[0b00000, 0b00000]

}
# Mode control codes
LETTERS_SHIFT = 0b11111
FIGURES_SHIFT = 0b11011

LF = 0b00010
CR = 0b01000

current_mode_tx = 'LETTERS'
current_mode_rx = 'LETTERS'


def open_tty_port(port,baudrate):
    global ser
    ser = serial.Serial(port=port,baudrate=baudrate, bytesize=5, parity='N', stopbits=2)


def ascii_to_baudot(ascii_str):
    baudot_code = []
    global current_mode_tx
    for char in ascii_str.upper():
        if char in LETTERS_TO_BAUDOT:
            if current_mode_tx == 'FIGURES':
                baudot_code.append(LETTERS_SHIFT)
                current_mode_tx = 'LETTERS'
            baudot_code.append(LETTERS_TO_BAUDOT[char])
        elif char in FIGURES_TO_BAUDOT:
            if current_mode_tx == 'LETTERS':
                baudot_code.append(FIGURES_SHIFT)
                current_mode_tx = 'FIGURES'
            baudot_code.append(FIGURES_TO_BAUDOT[char])
        else:
            raise ValueError(f"Character {char} cannot be converted to Baudot code")
    
    return baudot_code


def baudot_to_ascii_char(baudot_char):
    global current_mode_rx
    if baudot_char == b'\x1f':
        current_mode_rx = 'LETTERS'
        return ''
    elif baudot_char == b'\x1b':
        current_mode_rx = 'FIGURES'
        return ''
    elif baudot_char == LF:
        return '\n'
    else:
        if current_mode_rx == 'LETTERS':
            if baudot_char in BAUDOT_TO_LETTERS:
                return str(BAUDOT_TO_LETTERS[baudot_char])
            else:
                return ''
        elif current_mode_rx == 'FIGURES':
            if baudot_char in BAUDOT_TO_FIGURES:
                return str(BAUDOT_TO_FIGURES[baudot_char])
            else:
                return ''
            
        
def tty_input():
    global ser
    
    baudot_mesage = ser.read_until(b'\x02')
    #print(baudot_mesage)
    i = 0
    message = str('')
    while i < len(baudot_mesage):
        #currentbyte = baudot_mesage[i]
        
        #print(currentbyte)
        #print(bytes([baudot_mesage[i]]))
        message = message + baudot_to_ascii_char(bytes([baudot_mesage[i]]))
        #print(baudot_to_ascii_char(bytes([baudot_mesage[i]])))
        i+=1
    return message

def print_on_tape(text):
    text.upper()
    while i < len(text):
        if text[i] in TAPE_ALPHABET:
            ser.write(TAPE_ALPHABET[text[i]])
        i+=1
    for i in range(0,5):
        ser.write(TAPE_ALPHABET[' '])

def tty_output(text):
    global ser
    i = 0
    column = 0
    ser.write(b'\x00')
    ser.write(b'\x00')
    while i < len(text):
        if column > 62:
            column = 0
            ser.write(ascii_to_baudot('\n'))
            ser.write(ascii_to_baudot('\r'))
            ser.write(b'\x00')
            ser.write(b'\x00')
            ser.write(b'\x00')
        if text[i]=='\n':
            column = 0
        ser.write(ascii_to_baudot(text[i]))
        if text[i] == '\n':
            ser.write(ascii_to_baudot('\r'))
            ser.write(b'\x00')
            ser.write(b'\x00')
            ser.write(b'\x00')
        #print(text[i])
        i+=1
        column+=1