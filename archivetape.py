import tty_functions as tty
import sys
import serial
import signal

port_path = sys.argv[1]
baudrate = sys.argv[2]
file_path = sys.argv[3]

#                         0            1            2  3             4 5
#example command: python3 fileprint.py /dev/ttyUSB0 50 arts/test.txt 1 TEST
#arguments:
#1: serial port path or ID
#2: baud rate
#3: text file path

tty.open_tty_port(port_path,baudrate)

while()

text = ''
with open(file_path,'x') as file:
    print()


def signal_handler(signal, frame):
  tty.ser.flush()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)