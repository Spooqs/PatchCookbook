# Patch File Structure

## Pseudo-code Schema

```json
{
    "%%device" : {
        "%%category" : [
            {
                "name" : "string",
                "description" : "string",
                "device" : "%%device",
                "category" : "%%category",
                "recipe" : {
                    "%%generic_slot" : {
                        "slot_name" : "%%orig_slot_name",
                        "slot_label" : "%%slot_label",
                        "text" :: "%instructions"
                    },
                    ...
                }
            },
            { ... }, ...
        ]
    }
}
```

## Discussion

### %%device

`%%device` is the "target" device that will be used to craft the sound. This is
taken from the `device` setting in the recipe file. Currently, the only target
device is "operator".

This is normalized to all lower case.

The value associated with the device key is a dictionary where the keys are the
category (instrument type) and the values are the patches for that category.

### %%category

This is the "instrument type" of the patch - e.g. "Lead, Bass, Pad, etc". This
is taken from the `category` setting in the recipe file.

This is normalized to first letter capitalized - e.g. "Lead", not "lead" and
not "LEAD".

The value associated with the category key is an array of patches. The array
items are sorted on the `name` property of the entry.

### patches (category items)

An object of with the following keys:
- device 
- category 
- name : a sshort string identifier
- description : a long string
- recipe : an object discussed below.

All data is taken from the corresponding fields in the recipe file. The
capitaliztion of the device and category fields are normalized as discussed
above. All other values are taken as-is from recipe file.

### recipe and %%slot

The slots available will depend on the device. For operator, the slots are:
- osc_a
- osc_b
- osc_c
- osc_d
- filter
- pitch
- lfo
- main

The %%generic_slot is of the form "slot1", "slot2", etc.

All slot keys are guaranteed to be present in the recipe object. Any that were
not specified by the recipe file will be set to thw string "Off".
