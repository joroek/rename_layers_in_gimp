#!/usr/bin/env python

import string
from gimpfu import *

def rename_layers(image, drawable, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter):
    gimp.progress_init("Renaming layers")

    # start undo group
    pdb.gimp_undo_push_group_start(image)

    layerList = image.layers
    # iterate through the layers
    for layer in layerList:
        itterate(layer, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter, None)

    # end undo group
    pdb.gimp_undo_push_group_end(image)

def itterate(layer, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter, parent):
    layer.name = rename(layer.name, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter, parent)
    if isinstance(layer, gimp.GroupLayer):
        for child in layer.children:
            itterate(child, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter, layer.name)

def rename(name, caseMode, spaceMode, spaceSubstitute, poundMode, poundSubstitute, parentMode, parentDelimiter, parent):    
    if caseMode == 1: name = name.upper()
    elif caseMode == 2: name = name.lower()
    elif caseMode == 3: name = name.capitalize() 
    else: name = name
    if spaceMode: name = spaceSubstitute.join(name.split())
    if poundMode: name = name.replace("#", poundSubstitute)
    if parentMode and parent: name = parent + parentDelimiter + name
    return name


register(
    "python_fu_rename_layers",
    "Rename All Layers",
    "Rename all layers in the image based on a limited set of configurable parameters. Uses gimpfu, and hence a normal Layer (not a GroupLayer) must be focused to avoid 'TypeError: can't pickle GroupLayer objects'.",
    "u/joroek",
    "u/joroek",
    "2019",
    "<Image>/Image/_Rename All Layers...",
    "*",      # accept all images.
    [
        (PF_RADIO, "caseMode", "How do you want to handle case?: ", 0, (("Keep as is", 0),("Make UPPER CASE", 1),("Make lower case", 2),("Capitalize", 3))),
        (PF_BOOL, "spaceMode", "Repace whitespace?: ", False),
        (PF_STRING, "spaceSubstitute", "Whitespace replacement String: ", ""),
        (PF_BOOL, "poundMode", "Repace pound sign (#)?: ", False),
        (PF_STRING, "poundSubstitute", "Pound replacement String: ", ""),
        (PF_BOOL, "parentMode", "Include parents name in child name: ", False),
        (PF_STRING, "parentDelimiter", "Parent delimiter: ", "")
    ],
    [],
    rename_layers)

main()