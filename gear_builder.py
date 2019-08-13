
import maya.cmds as cmds


def createGear(teeth=10, length=0.3):
    """
    This function will create a gear with the given parameters
    Args:
        teeth: The number of teeth to create
        length: The length of the teeth
    Returns:
        A tuple of the transform, constructor and extrude node
    """
    
    spans = teeth * 2

   
    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    
    sideFaces = range(spans * 2, spans * 3, 2)

    # clear the selection to add each face to it
    cmds.select(clear=True)

    for face in sideFaces:
        cmds.select('%s.f[%s]' % (transform, face), add=True)

    #  extrude the selected faces by the given length
    # returns value of the extrude node inside a list
    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    # return a tuple of (transform, constructor, extrude)
    return transform, constructor, extrude
   


# Modifies our constructor and extrude node to change the teeth 
def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    """
    Change the number of teeth on a gear with a given number of teeth and a given length for the teeth.
    This will create a new extrude node.
    Args:
        constructor (str): the constructor node
        extrude (str): the extrude node
        teeth (int): the number of teeth to create
        length (float): the length of the teeth to create
    """
    spans = teeth * 2

    # Tmodify its attributes instead of creating a new one
    cmds.polyPipe(constructor, edit=True,
                  subdivisionsAxis=spans)

    # list of faces to extrude as teeth
    sideFaces = range(spans * 2, spans * 3, 2)
    faceNames = []



    for face in sideFaces:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

   
    #   cmds.setAttr('extrudeNode.inputComponents', numberOfItems, item1, item2, item3, type='componentList')
    cmds.setAttr('%s.inputComponents' % (extrude),
                 len(faceNames),
                 *faceNames,
                 type="componentList")

    # cmds.setAttr('extrudeNode.inputComponents', 2, 'f[1]', 'f[2]', type='componentList'

    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length)
