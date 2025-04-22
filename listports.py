#sloppily writen by OK1GAL 2024
import sys
import signal
import platform
current_platform = platform.system()

if current_platform == "Windows":
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
else:
    if current_platform == "Linux":
        import glob
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        print("no TTY for you, use normal platform\n")
        sys.exit()

for port in sorted(ports):
    print("{}".format(port))


def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)