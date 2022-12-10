# PatchCookbook


M4L Device for displaying device patch notes and instructions

## Overview

Ever been sitting in Ableton Live trying figure out how to make a simple Reese
Bass ? Tired of switching between windows (and maybe headsets) as you try to watch a
YouTube video and tweak an operator device at the same time ?

PatchCookbook is a Max4Live (c) device that you put in the same track as the
operator and gives you guidance on how to create all sorts of sounds using
operator.

![app ui](https://github.com/Spooqs/PatchCookbook/blob/main/docs/ocb_mockup2.png)

Each of those slots will be filled with guidelines on how to configure that
section of the operator device.

## Future
- Support for other stock devices (e.g. wavetable)
- More recipes

## Got a recipe we're missing ?

See [recipe/README](recipes/README.md) for details about how to contrib

## Installing

Get the [latest release zip file](https://github.com/Spooqs/PatchCookbook/releases/latest).

Inside the zip is a directory. That directory needs to be extract into you User Library in Ableton Live. The path to the User Library can be found by going to the browser in Ableton, left clicking on the User Library and choosing "Show in Explorer".

It will take a moment for Live to update the list in the browser.

## Using

PatchCookbook is a midi affect and so must go on a midi track *before* the instrument (e.g. operator).
