#sloppily writen by OK1GAL 2024

import sys

def demezeruj(strings, okolik):
    lines = []
    for line in strings:
        if len(line) > okolik: lines.append(line[okolik:])
        else: lines.append("\n")

    return lines

def zjisti_okolik(strings):
    difs = []

    for line in strings:
        ol = len(line)
        tl = len(line.strip())+1

        #print(f"{ol} -> {tl}")

        dif = ol - tl
        if dif > 0: difs.append(dif)

    return min(difs)
    


if __name__ == "__main__":
    cesta = sys.argv[1]

    pocet = -1
    if len(sys.argv) > 2:
        pocet = int(sys.argv[2])

    with open(cesta) as file:
        strings = file.readlines()

        if pocet == -1:
            pocet = zjisti_okolik(strings)
        #print(pocet)
        lines = demezeruj(strings, pocet)
    
    for line in lines:
        print(line, end="")
        