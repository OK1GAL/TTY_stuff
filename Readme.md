# Set of sloppy TTY tools<br/>
I've writen this set of tools to use CH340 USB to UART converter with old baudot teletypes.<br/>
<br/>
## demezerace.py<br/>
This script takes in ascii art and removes unnecesar columns at the begining of the file.<br/>
In czech mezera is space => demezerace => remove spaces.<br/>
<br/>
## fileprint.py<br/>
Takes text file, converts it to baudot and sends it to TTY.<br/>
Argumensts are tty port, baudrate, file path, print text on tape, text to print on tape<br/>
example command: `python3 fileprint.py /dev/ttyUSB0 50 arts/test.txt 1 TEST`<br/>
<br/>
## listports.py<br/>
prints all availaable tty ports<br/>
<br/>
## loopback.py<br/>
Self explanatory.<br/>
<br/>
## reformat.py<br/>
Removes ilegal characters from ascii art.<br/>
Vocabulary is not complete!<br/>
<br/>
## tape_test.py<br/>
Used for debbuging of tape printing<br/>
<br/>
## timeestimate.py<br/>
Estimates the time it takes to print an ascii art on 50 baud tty.<br/>
<br/>
## tty_functions.py<br/>
Basicaly TTY library.<br/>
<br/>
<br/>
Maybe it will be useful to someone.<br/>
<br/>
All arts are borrowed from here: `http://artscene.textfiles.com/rtty/`<br/>