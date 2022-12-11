#!/usr/bin/env python

import argparse
from   configparser import ConfigParser
import json
import os

class Consolidator:
    Metadata_keys = [ 'name', 'device', 'description', 'category' ]

    Recipe_keys = {
            'operator' : [ 'osc_d', 'osc_c', 'osc_b', 'osc_a', 'lfo', 'pitch', 'main', 'filter' ]
            }

    def __init__(self, output_file) :
        self.output = output_file
        self.consolidated = {}


    def _add_meta_data(self, input_file_name : str, cfg_data, json_data) :
        """
        Deal with the metadata section.
        """

        req_keys = { k : 1 for k in self.Metadata_keys }

        for ckey in cfg_data :
            if (ckey in req_keys) :
                json_data[ckey] = cfg_data[ckey]
                del req_keys[ckey]
            else :
                print(f'ERROR: invalid key `{ckey}` in metadata section')
                exit(101)

        if req_keys :
            print(f'ERROR: missing required key(s) in patch section : {list(req_keys.keys())}')
            exit(102)

        # record which file this came from.
        json_data['file'] = os.path.basename(input_file_name)

            
        device_name = json_data['device'].lower()
        json_data['device'] = device_name

        if device_name not in self.Recipe_keys :
            print(f'ERROR: unknown target device `{device_name}`')
            exit(103)

        # Add the skeleton to the correct part of the pile
        if device_name not in self.consolidated :
            self.consolidated[device_name] = {}

        device = self.consolidated[device_name]

        category_name = json_data['category'].lower().capitalize()
        json_data['category'] = category_name
        if category_name not in device :
            # note this goes into consolidated as a dict,
            # but before we output, we will transform to a list
            # This will help us validate and sort the patches
            device[category_name] =  {}

        patch_name = json_data['name']

        if patch_name not in  device[category_name] :
            device[category_name].update({patch_name : json_data})
        else :
            print(f'ERROR: duplicate patch name `{patch_name}` for `{device_name}`.`{category_name}`')
            exit(110)


    def _add_recipe(self, cfg_data, json_data) :

        slot_names = self.Recipe_keys[json_data['device']]

        recipe = {}
        for s in cfg_data :
            if s in slot_names :
                recipe[s] = { 'slot_name' : s, 'text' : cfg_data[s] }
            else :
                print(f"ERROR: invalid slot name for device {json_data['device']} : {s}")
                exit(10)

        output = {};
        for i,s in enumerate(slot_names) :
            slot_id = f"slot{i+1}"
            if s not in recipe or not recipe[s] :
                output[slot_id] = { 'slot_name' : s, 'text' : 'off' }
            else :
                output[slot_id] = recipe[s];

        json_data['recipe'] = output;

    def _transform_data(self, input_file_name : str, data : ConfigParser ) :
        """
        Add {data} to {consolidated}
        """

        new_data = {}
        for section in data :
            if section == 'patch' :
                self._add_meta_data(input_file_name, data[section], new_data)
            elif section == 'recipe' :
                self._add_recipe(data[section], new_data)
            elif section == 'DEFAULT' :
                # This is a section added by the parser. Not in love with it.
                pass
            else :
                print(f'ERROR: unknown section name "{section}"')
                exit(11)


        return True

    def consolidate(self, input_file_name) :

        print(f'LOG: processing {input_file_name}')

        cfg = ConfigParser()
        if not cfg.read(input_file_name) :
            print(f'ERROR: failure reading recipe fron file {input_file_name}')
            exit(10)
        self._transform_data(input_file_name, cfg)

    def write_data(self) :
        # need to rewrite the data a bit
        # sort the keys for the patches. dictionaries are ordered
        # by default. the json module perserves that order on export
        # hopefully m4l perserves it on load.
        for d, dv in self.consolidated.items():
            for c in dv :
                cv = dv[c]
                pnames = sorted(cv.keys())
                dv[c] = {}
                dv[c] = { p : cv[p] for p in pnames } 
        self.output.write(json.dumps(self.consolidated, indent=2))


# ===== MAIN ======================
if __name__ == "__main__" :
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
                    # only process if not a hidden file and looks like a recipe
                    if f[0] != '.' and os.path.splitext(f)[1] == '.recipe' :
                        c.consolidate(os.path.join(toppath, f))

        else :
            print(f'ERROR: unknown path type (not file or dir {i}')
            exit(40)

    c.write_data()

