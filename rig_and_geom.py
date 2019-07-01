#Create Geometry and a Simple Rig

from maya import cmds

# create a cube by giving maya the polyCube command
cube = cmds.polyCube()


# <type 'list'>
print type(cube)  #[name_of_object, name_of_node_creating_object]


# just the transform, which is the first member of the list
transform = cube[0]
creator = cube[1]

circle = cmds.circle()

circle = circle[0]
# Okay so we have the circle transform (circle) and the cube's transform (transform)
# Let's parent the cube under the circle

cmds.parent(transform, circle)

# lock the cube's controls

cmds.setAttr(transform+'.translate', lock=True)
cmds.setAttr(transform+".rotate", lock=True)
cmds.setAttr(transform+'.scale', lock=True)

# Finally lets select the circle
cmds.select(circle)

