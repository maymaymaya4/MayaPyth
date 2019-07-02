#from earlier renamer, refactored into callable functions

from maya import cmds


#key: objType, value: suffix
SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
}

DEFAULT = "grp"


def rename(selection=False):
    """
    Renames objects by adding suffixes based on the object type
    Args:
        selection (bool): Whether we should use the selection or not. Defaults to False
    Raises:
        RuntimeError: If nothing is selected
    Returns:
        list: A list of all the objects renamed
    """

    # if we should use the selection or not
    objects = cmds.ls(selection=selection, dag=True)

    #if trying to use the selection and nothing is selected
    if selection and not objects:
        raise RuntimeError("Nothing selected")

    # sort from longest to shortest so don't rename parents before children
    objects.sort(key=len, reverse=True)

    for obj in objects:

        # Get the shortname  by splitting at the last |
        shortName = obj.split('|')[-1]

        # if there are children, get their type.
        # This is in case it is a transform and not its shape
        children = cmds.listRelatives(obj, children=True) or []
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        
        # If the dictionary doesn't hold the item, it will return the default value instead
        suffix = SUFFIXES.get(objType, DEFAULT)

        if not suffix: #for camera None suffix (skip rest of the code in the for loop)
            continue

        # if it already has the suffix, skip 
        if shortName.endswith('_'+suffix):
            continue

        newName = '%s_%s' % (shortName, suffix)
        cmds.rename(shortName, newName) #renames object

        index = objects.index(obj)

        # rename in the list to return
        objects[index] = obj.replace(shortName, newName)

    return objects
