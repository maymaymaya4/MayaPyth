import bpy, bmesh
import math
from mathutils import Quaternion, Vector, Euler
from pathlib import Path

min_frame = 91
max_frame = 159

def transform_points(x, y, z):
    x = -(x-35)/15
    y = -(y+106)/15
    z = (z-1847)/15
    return x, y, z

def keyframe_visibility(obj, frame):
    if frame > 0:
        obj.hide_render = True
        obj.hide = True
        obj.keyframe_insert("hide_render", frame=frame-1)
        obj.keyframe_insert("hide", frame=frame-1)

    if frame < max_frame:
        obj.hide_render = True
        obj.hide = True
        obj.keyframe_insert("hide_render", frame=frame+1)
        obj.keyframe_insert("hide", frame=frame+1)

    obj.hide_render = False
    obj.hide = False
    obj.keyframe_insert("hide_render", frame=frame)
    obj.keyframe_insert("hide", frame=frame)
    return


MOTION_FILE = bpy.path.abspath("C:/Users/masak/Documents/Development/biomechanical_eye_rendering_blender_NIna/RaytracePoints.txt")

motion_file = Path(MOTION_FILE).open('r')
frame = 0
bpy.context.scene.frame_start = 0

bm = None
mesh = None
obj = None
obj_count = 0

for line in motion_file:
    splitline = line.split()

    if len(splitline) == 2:
        # The line specifies the frame number
        frame = int(splitline[0])
        obj_count = 0

        ####### ONLY FOR TESTING
        if frame < min_frame:
            print("Skipping frame {0}".format(frame), end='\r')
            continue
        if frame > max_frame:
            break

        # update previous mesh
        if frame > min_frame:
            bm.to_mesh(mesh)
            mesh.update()
            print("Processing frame {0}, converting to curve".format(frame-1), end='\r')
            bpy.context.scene.objects.active = obj
            obj.select = True
            bpy.ops.object.convert(target='CURVE', keep_original=False)
            curve = bpy.data.curves["~Raytrace" + str(frame-1)]
            curve.bevel_depth = 0.001
            obj.data.materials.append(bpy.data.materials["RaytraceMaterial"])
            #bpy.context.active_object.material_slots[0].material = bpy.data.materials["RaytraceMaterial"]

        bpy.context.scene.frame_end = frame
        print("Processing frame {}".format(frame), end='\r')

        # Create single object containing all lines for that frame
        mesh = bpy.data.meshes.new("frame" + str(frame))
        obj = bpy.data.objects.new("~Raytrace" + str(frame), mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        scene.objects.active = obj
        obj.select = True

        bm = bmesh.new()
        bm.from_mesh(mesh)

    elif frame < min_frame:
        continue

    ######## ONLY FOR TESTING:
    #elif obj_count > 10000:
    #    continue

    elif len(splitline) == 6:
        obj_count += 1
        print("Processing frame {0}, object {1}".format(frame, obj_count), end='\r')
        x1, y1, z1, x2, y2, z2 = map(float, splitline)
        v1 = bm.verts.new(transform_points(x1, y1, z1))
        v2 = bm.verts.new(transform_points(x2, y2, z2))
        bm.edges.new((v1, v2))
        bm.to_mesh(mesh)

    else:
        #incorrect format, do nothing
        continue

# update last frame
bm.to_mesh(mesh)
mesh.update()
print("Processing frame {0}, converting to curve".format(frame-1), end='\r')
bpy.context.scene.objects.active = obj
obj.select = True
bpy.ops.object.convert(target='CURVE', keep_original=False)
curve = bpy.data.curves["~Raytrace" + str(frame-1)]
curve.bevel_depth = 0.1
obj.data.materials.append(bpy.data.materials["RaytraceMaterial"])

#keyframe visibility and render visibility
for f in range(min_frame, max_frame+1):
    obj = bpy.context.scene.objects["~Raytrace" + str(f)]
    keyframe_visibility(obj, f)

print("Processing completed")
