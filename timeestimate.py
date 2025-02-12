#sloppily writen by OK1GAL 2024

from time import sleep

def maxSirka(cesta):
  sirka = 0
  with open(cesta) as f:
    for line in f:
      s = len(line)
      if s > sirka: sirka = s
  return sirka

path = input("input txt file path:  ")

hello = "START\n\n"

print("opening document:"+str(path))

file = open(path, 'r')
text = ''
text = file.read()

file.close()
count = len(text)
#for i in range(0, len(text)):  
#    if(text[i] != 0x03):  
#        count = count + 1;  

textbytes = ''
textbytes = bytearray()

textbytes.extend(map(ord,text))


print("number of chars: ")
print(count)
print(text)
timems = (count*120)
times = timems/1000
timem = times/60

print("Estimated time: ")
print(timem)

print(maxSirka(path))

    
