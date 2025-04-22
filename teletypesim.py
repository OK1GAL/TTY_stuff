import serial
import threading
import sys
import termios
import tty
import signal

# ANSI color codes
COLOR_TX = '\033[92m'   # green
COLOR_RX = '\033[96m'   # cyan
COLOR_RESET = '\033[0m'

# Baudot tables
LETTERS_TO_BAUDOT = {
    'A': 0b00011, 'B': 0b11001, 'C': 0b01110, 'D': 0b01001, 'E': 0b00001,
    'F': 0b01101, 'G': 0b11010, 'H': 0b10100, 'I': 0b00110, 'J': 0b01011,
    'K': 0b01111, 'L': 0b10010, 'M': 0b11100, 'N': 0b01100, 'O': 0b11000,
    'P': 0b10110, 'Q': 0b10111, 'R': 0b01010, 'S': 0b00101, 'T': 0b10000,
    'U': 0b00111, 'V': 0b11110, 'W': 0b10011, 'X': 0b11101, 'Y': 0b10101,
    'Z': 0b10001, ' ': 0b00100, '\n':0b00010, '\r':0b01000 
}

FIGURES_TO_BAUDOT = {
    '1': 0b10111, '2': 0b10011, '3': 0b00001, '4': 0b01010, '5': 0b10000,
    '6': 0b10101, '7': 0b00111, '8': 0b00110, '9': 0b11000, '0': 0b10110,
    '-': 0b00011, "'": 0b11101, '!': 0b01111, '&': 0b11111, '#': 0b11011,
    '(': 0b11100, ')': 0b01110, ':': 0b01100, ',': 0b01100, '?': 0b00101,
    '+': 0b01101, '/': 0b11010, '=': 0b01001, '.': 0b11110, ' ': 0b00100,
    '\n':0b00010, '\r':0b01000 
}

LETTERS_SHIFT = 0b11111
FIGURES_SHIFT = 0b11011

current_mode = 'LETTERS'

def ascii_to_baudot(char):
    global current_mode
    c = char.upper()
    if c in LETTERS_TO_BAUDOT:
        if current_mode == 'FIGURES':
            current_mode = 'LETTERS'
            return [LETTERS_SHIFT, LETTERS_TO_BAUDOT[c]]
        else:
            return [LETTERS_TO_BAUDOT[c]]
    elif c in FIGURES_TO_BAUDOT:
        if current_mode == 'LETTERS':
            current_mode = 'FIGURES'
            return [FIGURES_SHIFT, FIGURES_TO_BAUDOT[c]]
        else:
            return [FIGURES_TO_BAUDOT[c]]
    else:
        return []

def baudot_to_ascii(code, mode):
    if mode == 'LETTERS':
        for k, v in LETTERS_TO_BAUDOT.items():
            if v == code:
                return k
    elif mode == 'FIGURES':
        for k, v in FIGURES_TO_BAUDOT.items():
            if v == code:
                return k
    return '?'

def read_loop(ser):
    rx_mode = 'LETTERS'
    while True:
        b = ser.read()
        if not b:
            continue
        code = b[0] & 0x1F
        if code == LETTERS_SHIFT:
            rx_mode = 'LETTERS'
            continue
        elif code == FIGURES_SHIFT:
            rx_mode = 'FIGURES'
            continue
        char = baudot_to_ascii(code, rx_mode)
        sys.stdout.write(f"{COLOR_RX}{char}{COLOR_RESET}")
        sys.stdout.flush()

def write_loop(ser):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        while True:
            ch = sys.stdin.read(1)
            if ch == '\n':  # Enter pressed
                sys.stdout.write(f"{COLOR_TX}↵{COLOR_RESET}")
                sys.stdout.flush()
                print()  # Moves stdout to new line
                for byte in ascii_to_baudot('\r') + ascii_to_baudot('\n'):
                    ser.write(bytes([byte]))
            else:
                sys.stdout.write(f"{COLOR_TX}{ch}{COLOR_RESET}")
                sys.stdout.flush()
                for byte in ascii_to_baudot(ch):
                    ser.write(bytes([byte]))
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 teletypesim.py /dev/ttyUSB0 50")
        sys.exit(1)

    port = sys.argv[1]
    baud = int(sys.argv[2])

    ser = serial.Serial(port=port, baudrate=baud, bytesize=5, parity='N', stopbits=2)
    print(f"Connected to {port} at {baud} baud (5N2)")

    signal.signal(signal.SIGINT, lambda s, f: (ser.close(), sys.exit(0)))

    threading.Thread(target=read_loop, args=(ser,), daemon=True).start()
    write_loop(ser)

if __name__ == '__main__':
    main()
