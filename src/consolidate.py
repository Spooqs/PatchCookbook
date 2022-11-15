#!/usr/bin/env python

import argparse
import hjson
import json
import os

class Consolidator:
    def __init__(self, output_file) :
        self.output = output_file
        self.consolidated = {}


    def _transform_data(self, data) :
        """
        Add {data} to {consolidated}
        '"""

        if data['device'] not in self.consolidated :
            self.consolidated[data['device']] = {}

        device = self.consolidated[data['device']] 

        if data['category'] not in device :
            device[data['category']] = []

        category = device[data['category']]

        # need to check uniqueness here
        new_data = {
                "name" : data["name"],
                "desc" : data['description'],
                "steps" : [ { "order" : k, "instruction" : v } for k,v in enumerate(data['steps'])]
            }

        category.append(new_data)

        return True

    def consolidate(self, input_file_name) :

        print(f'LOG: processing {input_file_name}')
        data = hjson.load(open(input_file_name, "r"))
        self._transform_data(data)

    def write_data(self) :
        self.output.write(json.dumps(self.consolidated, indent=2))


# ===== MAIN ======================
parser = argparse.ArgumentParser()
parser.add_argument("--output", help="path and file for the output")
parser.add_argument("input", metavar="IN", type=str, nargs="+", help="path and file for the input")

args = parser.parse_args()

if not args.output :
    print("ERROR: --output not given on command line")
    exit(20)

out_file = None

try :
    out_file = open(args.output, "w");
except Exception as e :
    print(f"ERROR: Could not open {args.output} for writing : {e=}")
    exit(30)

if not out_file :
    print(f"ERROR: Could not open {args.output} for writing")
    exit(30)

c = Consolidator(out_file)

for i in args.input :
    if not os.path.exists(i) :
        print(f'ERROR: path {i} does not exist')
        exit(40)

    if os.path.isfile(i) :
        c.consolidate(i)
    elif os.path.isdir(i) :
        for toppath, _, filenames in os.walk(i) :
            print(f'LOG : toppath = {toppath}')
            for f in filenames :
                print(f'LOG : file = {f}')
                # only process if not a hidden file and looks like hjson
                if f[0] != '.' and os.path.splitext(f)[1] == '.hjson' :
                    c.consolidate(os.path.join(toppath, f))

    else :
        print(f'ERROR: unknown path type (not file or dir {i}')
        exit(40)

c.write_data()

