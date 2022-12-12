#! env python

import logging
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, required=True, help="path and file for the output")
parser.add_argument("--input", type=str, required=True, help="path and file for the input")
parser.add_argument('--simple', default=False, action='store_true')
parser.add_argument('--no-simple', dest='simple', action='store_false')
parser.add_argument("replacement", metavar="key=value", type=str, nargs="+", help="Replacement strings")

args = parser.parse_args()

######
# Generate the replacement map
#

repl_map = {}
for r in args.replacement :
    k, v = r.split('=')
    repl_map[k] = v

### 
# Read the input

in_file = None
try :
    in_file = open(args.input, "rb")
except Exception as e :
    print(f"ERROR: Could not open {args.input} for reading : {e=}")
    exit(30)

if not in_file :
    print(f"ERROR: Could not open {args.input} for reading")
    exit(30)


file_header = ''
if not args.simple :
    file_header = in_file.read(32)

file_data = in_file.read()

in_file.close()


#####
# replace

#
# There has to be a way to do this as a single pass,
# but this at least proves the concept
#
for k,v in repl_map.items() :
    source = f'@{k}@'.encode('UTF-8') 
    target = v.encode('UTF-8')
    file_data = file_data.replace(source, target)

out_file = None
try :
    out_file = open(args.output, "wb")
except Exception as e :
    print(f"ERROR: Could not open {args.output} for writing : {e=}")
    exit(30)

if not out_file :
    print(f"ERROR: Could not open {args.output} for reading")
    exit(30)

#######
# The header is 32 bytes. The last 4 bytes are a length field for the rest of the data
# in little-endian order
#

if not args.simple :
    file_header = file_header[0:28] + int(len(file_data)).to_bytes(4, byteorder="little")
    out_file.write(file_header)

out_file.write(file_data)

