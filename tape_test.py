#sloppily writen by OK1GAL 2024

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
import signal
import sys
import time

comport_number = 0
baudrate_input = 0
print("\n\nAvailable COM ports:")
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
comport_number = input("input desired COM number:")
baudrate_input = input("input desired baud rate:")
print("opening COM"+comport_number+" at "+baudrate_input+" baud")
ser = serial.Serial(port =('COM'+comport_number),baudrate=baudrate_input,bytesize=5,parity='N',stopbits=1)


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
    '-': 0b00011, "'": 0b11101, '!': 0b01111, '&': 0b11111, '#': 0b11011,
    '(': 0b11100, ')': 0b01110, ':': 0b01100, ',': 0b01011, '?': 0b00101,
    '+': 0b01101, '/': 0b11010, '=': 0b01001, '.': 0b11110, ' ': 0b00100,
    '\n':0b00010, '\r':0b01000 
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

current_mode = 'LETTERS'

def ascii_to_baudot(ascii_str):
    baudot_code = []
    global current_mode
    for char in ascii_str.upper():
        if char in LETTERS_TO_BAUDOT:
            if current_mode == 'FIGURES':
                baudot_code.append(LETTERS_SHIFT)
                current_mode = 'LETTERS'
            baudot_code.append(LETTERS_TO_BAUDOT[char])
        elif char in FIGURES_TO_BAUDOT:
            if current_mode == 'LETTERS':
                baudot_code.append(FIGURES_SHIFT)
                current_mode = 'FIGURES'
            baudot_code.append(FIGURES_TO_BAUDOT[char])
        else:
            raise ValueError(f"Character {char} cannot be converted to Baudot code")
    
    return baudot_code

# Example usage
ascii_str = "  THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 0123456789\n\r"
#print("Baudot code:", baudot_code_bytes)

#while True:
#    baudot_code = ascii_to_baudot(ascii_str)
#    baudot_code_bytes = [byte for byte in baudot_code]
#    ser.write(baudot_code_bytes)
#    time.sleep(5)
text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
i = 0
while i < len(text):
    ser.write(TAPE_ALPHABET[text[i]])
    i+=1


def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)