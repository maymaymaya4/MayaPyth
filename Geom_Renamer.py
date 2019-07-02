"""
This is a utility to add suffixes to objects based on the object type.
This helps keep our scene tidy and organized.
"""

from maya import cmds

#long s.t. full path is given, list all selected
selection = cmds.ls(selection=True, long=True)

# This will give us back a list of the paths of all the objects we have selected
print selection

#if nothing selected, list every object in the outliner (dag)
if len(selection) == 0:
    selection = cmds.ls(long=True, dag=True)

# Can run into an issue where rename a parent before a child, causing the path to the child to change.
# Sort by length and reverse it so longest first st rename children before renaming parents
selection.sort(key=len, reverse=True)

for obj in selection:

    # name is grandparent|parent|child
    # just want child, sosplit using the | character 
    shortName = obj.split('|')[-1] 

    print "Before rename: ", shortName

    # If object is a transform, check if it has a shape below it
    #listRelatives fetches children of obj, if none set children var to empty list 
    children = cmds.listRelatives(obj, children=True) or []

    if len(children) == 1: #this is in case it is a transform, not the shape 
        child = children[0] #shape is the child of a transform, so now have the shape
        objType = cmds.objectType(child)
    else: #assuming no children 
        # Else get the object type of the current object (the parent). If no children, already have the shape
        objType = cmds.objectType(obj) 


    if objType == "mesh":
        suffix = 'geo'
    elif objType == "joint":
        suffix = 'jnt'
    elif objType == 'camera':
        print "Skipping camera"
        continue
    else:
        suffix = 'grp'

    newName = shortName+"_"+suffix

    # Rename the obj to the new name with the suffix
    cmds.rename(obj, newName)
    print "After rename: ", newName

