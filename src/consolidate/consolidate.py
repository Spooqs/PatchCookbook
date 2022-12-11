#!/usr/bin/env python

import argparse
from   configparser import ConfigParser
import json
import os

from collections import namedtuple

SlotConfig = namedtuple('SlotConfig', ['id', 'label'])

class Consolidator:
    Metadata_keys = [ 'name', 'device', 'description', 'category' ]

    Recipe_keys = {

            # this info probably belongs in an external config file
            'operator' : {
                # The key is what shows up in the .recipe file. The values
                # will show up in the patch file
                'osc_d'  : SlotConfig('slot1', 'D'   ),
                'osc_c'  : SlotConfig('slot2', 'C'   ),
                'osc_b'  : SlotConfig('slot3', 'B'   ),
                'osc_a'  : SlotConfig('slot4', 'A'   ),
                'lfo'    : SlotConfig('slot5', 'LFO' ),
                'pitch'  : SlotConfig('slot6', 'Pitch Env'  ),
                'filter' : SlotConfig('slot7', 'Filter' ),
                'main'   : SlotConfig('slot8', 'Main'   ),

            },
        }

    def __init__(self) :
        self.consolidated = {}
        # reform the Recipe data for ease of access.


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

        slot_config_data = self.Recipe_keys[json_data['device']]

        recipe = {}
        for user_slot_name in cfg_data :
            if user_slot_name in slot_config_data :
                this_config_data = slot_config_data[user_slot_name]
                text = "Off"
                if user_slot_name in cfg_data and cfg_data[user_slot_name] != "" :
                    text = cfg_data[user_slot_name]
                recipe[user_slot_name] = { 'slot_name' : user_slot_name, 'text' : text, 'slot_label' : this_config_data.label }
            else :
                print(f"ERROR: invalid slot name for device {json_data['device']} : {user_slot_name}")
                exit(10)

        output = {};
        for user_slot_name in slot_config_data :
            this_config_data = slot_config_data[user_slot_name]
            generic_slot_name = this_config_data.id
            
            # The loop above takes care of missing values for the slot. WE just
            # need to take care of missing slots.
            if user_slot_name not in recipe :
                output[generic_slot_name] = { 'slot_name' : generic_slot_name, 
                        'text' : 'off', 
                        'slot_label' : this_config_data.label }
            else :
                output[generic_slot_name] = recipe[user_slot_name]

        json_data['recipe'] = output

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

    def write_data(self, output_file) :
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
        
        output_json = { 'metadata' : { 'version' : "@VERSION_STRING@" }, 'patches' : self.consolidated }
        output_file.write(json.dumps(output_json, indent=2).encode('UTF-8'))


# ===== MAIN ======================
if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="path and file for the output")
    parser.add_argument("input", metavar="IN", type=str, nargs="+", help="path and file for the input")

    args = parser.parse_args()

    if not args.output :
        print("ERROR: --output not given on command line")
        exit(20)

    c = Consolidator()

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
            print(f'ERROR: unknown path type (`{i}` is not file or directory')
            exit(40)

    out_file = None

    try :
        # be sure to open in binary mode for windows
        out_file = open(args.output, "wb");
    except Exception as e :
        print(f"ERROR: Could not open {args.output} for writing : {e=}")
        exit(30)

    if not out_file :
        print(f"ERROR: Could not open {args.output} for writing")
        exit(30)

    c.write_data(out_file)

