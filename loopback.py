#sloppily writen by OK1GAL 2024
import serial

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=50, bytesize=5, parity='N', stopbits=2)

while True:
    ser.write(ser.read())