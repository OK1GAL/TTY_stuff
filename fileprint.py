import serial
import threading
import sys

# Baudot control codes
LTRS = 0b11111
FIGS = 0b11011

# Correct lookup tables
LETTERS_TO_BAUDOT = {
    'A': 0b00011, 'B': 0b11001, 'C': 0b01110, 'D': 0b01001, 'E': 0b00001,
    'F': 0b01101, 'G': 0b11010, 'H': 0b10100, 'I': 0b00110, 'J': 0b01011,
    'K': 0b01111, 'L': 0b10010, 'M': 0b11100, 'N': 0b01100, 'O': 0b11000,
    'P': 0b10110, 'Q': 0b10111, 'R': 0b01010, 'S': 0b00101, 'T': 0b10000,
    'U': 0b00111, 'V': 0b11110, 'W': 0b10011, 'X': 0b11101, 'Y': 0b10101,
    'Z': 0b10001, ' ': 0b00100, '\n': 0b00010, '\r': 0b01000
}

FIGURES_TO_BAUDOT = {
    '1': 0b10111, '2': 0b10011, '3': 0b00001, '4': 0b01010, '5': 0b10000,
    '6': 0b10101, '7': 0b00111, '8': 0b00110, '9': 0b11000, '0': 0b10110,
    '-': 0b00011, "'": 0b11101, '!': 0b01111, '&': 0b11111, '#': 0b11011,
    '(': 0b11100, ')': 0b01110, ':': 0b01100, ',': 0b01100, '?': 0b00101,
    '+': 0b01101, '/': 0b11010, '=': 0b01001, '.': 0b11110, ' ': 0b00100,
    '\n': 0b00010, '\r': 0b01000
}

# Reverse maps for decoding
BAUDOT_TO_LETTERS = {v: k for k, v in LETTERS_TO_BAUDOT.items()}
BAUDOT_TO_FIGURES = {v: k for k, v in FIGURES_TO_BAUDOT.items()}

current_shift = 'LTRS'

def char_to_baudot(c):
    global current_shift
    c = c.upper()
    if c in LETTERS_TO_BAUDOT:
        if current_shift != 'LTRS':
            current_shift = 'LTRS'
            return [LTRS, LETTERS_TO_BAUDOT[c]]
        return [LETTERS_TO_BAUDOT[c]]
    elif c in FIGURES_TO_BAUDOT:
        if current_shift != 'FIGS':
            current_shift = 'FIGS'
            return [FIGS, FIGURES_TO_BAUDOT[c]]
        return [FIGURES_TO_BAUDOT[c]]
    else:
        return []

def baudot_to_char(code, shift):
    return BAUDOT_TO_LETTERS.get(code) if shift == 'LTRS' else BAUDOT_TO_FIGURES.get(code, '?')

def read_thread(ser):
    shift = 'LTRS'
    while True:
        byte = ser.read(1)
        if not byte:
            continue
        code = ord(byte) & 0b11111
        if code == LTRS:
            shift = 'LTRS'
        elif code == FIGS:
            shift = 'FIGS'
        else:
            char = baudot_to_char(code, shift)
            if char:
                sys.stdout.write(char)
                sys.stdout.flush()

def main():
    port = "/dev/ttyUSB0"
    baudrate = 50

    ser = serial.Serial(port=port,baudrate=baudrate, bytesize=5, parity='N', stopbits=1, timeout= 0.1)

    print(f"\nConnected to {port} @ {baudrate} baud (5N2)")
    print("Type to send. Press ESC to quit.\n")

    threading.Thread(target=read_thread, args=(ser,), daemon=True).start()

    try:
        while True:
            c = sys.stdin.read(1)
            if c == '\x1b':
                break
            for code in char_to_baudot(c):
                ser.write(bytes([code]))
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("\nDisconnected.")

if __name__ == "__main__":
    main()
