# Recipes

## Syntax

Recipes are simple INI style files. There are two sections
that are required - patch and recipe. No other sections are allowed.
Below is an annotated example

```ini
[patch]
# This section must be first. This  contains meta information about the patch.

# Which device is the "target" - the device that will be used to create the
# sound. Currently the only valid entry is 'operator'
device : operator

# What category or "style" is the sound (eg bass, lead, pad, etc)
# Note that this value will be normalized to first letter capitalized.
category : Lead

# The name for the patch. This will be presented to the user as a
# part of the menu. Duplicate names inside a category is not allowed.
name : Groovy Lead

# A short description of the sound
description : A Lead sound that is really groovy.

[recipe]
# The second required section. This contains the instructions that will be
# shown to the users in the slots on the cookbook ui.
# The list of keys below are the only ones that are allowed
# If you don't need to put something in a particular slot, you can either
# leave the rght side blank or just not include the key.
osc_a : A should be set to something
osc_b : B should be set to something
osc_c : Long multiline
     instructions are possible, but the second and following
     lines need to be indented. A blank line or a non indented
     line terminates the multiline
# blanks are fine. It will show up as "Off" in the UI
osc_d : 
# filter : Commented out also acts as blank
lfo : As a guide, these instructions should be broad guidelines "use a low
    pass" rather specific "Add a low pass filter at 700Hz"
pitch : The order of the slot keys doesn't matter.
main :  And a step to right
```

## Getting it included

### Pull Request

This is the perferable method. Clone the repo, add the file into the recipe
directory, and then raise a PR.

If that doesn't mean anything to you, then you can :

### Open an Issue

[Open request issue](https://github.com/Spooqs/OperatorCookbook/issues) and
attach your proposed recipe to the it.
