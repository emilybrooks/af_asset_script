import argparse
from textwrap import wrap
import struct

parser=argparse.ArgumentParser(description="Converts RGB5A3 palettes from Animal Crossing to RGB5A1 for Animal Forest.")
parser.add_argument("palette")
args=parser.parse_args()

noSpaces = args.palette.replace(" ", "")
gcPal = int(noSpaces, 16).to_bytes(len(noSpaces)//2, 'big')
n64Pal = ""

for short in struct.iter_unpack(">H", gcPal):
    short = short[0]
    alphaBit = short >> 15

    if alphaBit:
        short = short << 1 & 0xFFFF
        n64Pal += f"{short + 1:04X}"
    else:
        # Its not possible to determine what the n64 data originally was because R G and B were clipped from 5 bits to 4 bits
        n64Pal += "XXXX"
    
    n64Pal += " "

print(n64Pal)
