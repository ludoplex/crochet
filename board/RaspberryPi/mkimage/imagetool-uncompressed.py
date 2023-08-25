#!/usr/bin/env python

import os
import re
import sys

# Template and parameters are stored in same directory
# as this Python file
PATH=os.path.dirname(__file__)

try:
   input_image = sys.argv[1]
   output_image = sys.argv[2]
except:
   input_image = ""

# Open input (which may be stdin)
if not input_image:
   sys.stderr.write("usage : imagetool-uncompressed.py <input image> <output image>\n");
   sys.exit(0)
elif input_image == '-':
   infile = sys.stdin.buffer if sys.version_info.major == 3 else sys.stdin
else:
   infile = open(input_image, "rb")

# Open output (which may be stdout)
if not output_image or output_image == '-':
   outfile = sys.stdout.buffer if sys.version_info.major == 3 else sys.stdout
else:
   outfile = open(output_image, "wb")

with open(os.path.join(PATH, "first32k.bin"), "rb") as f:
   mem = bytearray(f.read(32768))

# Overlay boot parameters and args onto template
def load_to_mem(name, addr):
   with open(os.path.join(PATH, name)) as f:
      for l in f:
         if l.startswith('0x'):
            value = int(l, 0)
            for i in range(4):
               mem[addr] = int((value >> i * 8) & 0xff)
               addr += 1
load_to_mem("boot-uncompressed.txt", 0x00000000)
load_to_mem("args-uncompressed.txt", 0x00000100)

# Write out header
outfile.write(mem)

# Copy input image after header
while True:
   if piece := infile.read(4096):
      outfile.write(piece)

   else:
      break # end of file
# Close files
infile.close()
outfile.close()
