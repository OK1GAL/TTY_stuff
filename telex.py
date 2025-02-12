#sloppily writen by OK1GAL 2024
import serial
from time import sleep
import sys

ser = serial.Serial('/dev/ttyUSB0', 9600)

""" path = input("input txt file path:  ") """

hello = "START\n\n"
""" 
print("opening document:"+str(path)) """

path = sys.argv[1]

file = open(path, 'r')
text = ''
text = file.read()

count = len(text)
#for i in range(0, len(text)):  
#    if(text[i] != 0x03):  
#        count = count + 1;  

textbytes = ''
textbytes = bytearray()

textbytes.extend(map(ord,text))

print(count)
print(text)
print(textbytes)

sendbytes = ''

ser.reset_input_buffer()
sleep(0.5)
ser.write(b'\x02')

while ser.read() != b'\x06' :
    sleep(0.0001)


for i in range(0,count):
    #print(str(textbytes[i]))
    print(i)
    print(textbytes[i])

    sendbytes = bytearray()
    sendbytes.extend(map(ord,text[i]))
    #sendbytes = bytes(text[i])
    print(sendbytes)
    ser.write(sendbytes)
    while ser.read() != b'\x06':
        sleep(0.0001);
    #sleep(0.05);
ser.write(b'\x0a')
ser.write(b'\x03')
ser.close()
file.close()
    
