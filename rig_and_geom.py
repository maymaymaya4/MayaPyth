#Create Geometry and a Simple Rig

from maya import cmds

cube = cmds.polyCube()


# <type 'list'>
print type(cube)  #[name_of_object, name_of_node_creating_object]


# just the cube object
transform = cube[0]

circle_ = cmds.circle()
circle = circle_[0]

# Parent the cube under the circle
cmds.parent(transform, circle)

# lock the cube's controls
cmds.setAttr(transform+'.translate', lock=True)
cmds.setAttr(transform+".rotate", lock=True)
cmds.setAttr(transform+'.scale', lock=True)

# Leave circle selected
cmds.select(circle)

