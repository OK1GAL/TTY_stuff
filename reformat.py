#sloppily writen by OK1GAL 2024
import sys

src = sys.argv[1]#input("input source file path:  ")
dst = sys.argv[2]#input("input destination file path:  ")


print("opening document:"+str(src))

file = open(src, 'r')

text = ''
text = file.read().replace(";",":").replace("_","-").replace('"',"'").replace('$','S').replace('#','H')


with open(dst, 'w') as f:
    f.write(text)


file.close()
    
