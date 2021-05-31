# Helicoidify - turn an edge loop into four partial helicoid threads!
# * make sure to select the object to run the script on
# * make sure selected object has "apply object transform" operation performed

import bpy
import mathutils
import math

QUARTER_TURN = math.pi / 2

# min/max of edge loops to use as helicoid in mm
minHeight = 3.9
maxHeight = 6.1

# height and angle-length of each thread
threadHeight = 4.0
threadAngle = 60.0 * (math.pi / 180.0)

# get the counter clockwise angle 
def vectorAngle(dir):
    dir2D = dir.copy()
    dir2D.z = 0.0
    angle = -math.atan2(dir2D.x, dir2D.y)
    if (dir2D.x > 0.0): return math.tau + angle
    return angle

def getOffsetFromQuarter(angle):
    quarterNumber = math.floor(angle / QUARTER_TURN)
    return angle - (quarterNumber * QUARTER_TURN)

# vertices from the selected object, the object with a loop of verts to helicoidify
vertices = bpy.context.object.data.vertices

aabbMin = mathutils.Vector((math.inf, math.inf, math.inf))
aabbMax = mathutils.Vector((-math.inf, -math.inf, -math.inf))

# figger out item's dimms and center
for vertex in vertices:
    aabbMin.x = min(aabbMin.x, vertex.co.x)
    aabbMin.y = min(aabbMin.y, vertex.co.y)
    aabbMin.z = min(aabbMin.z, vertex.co.z)
    aabbMax.x = max(aabbMax.x, vertex.co.x)
    aabbMax.y = max(aabbMax.y, vertex.co.y)
    aabbMax.z = max(aabbMax.z, vertex.co.z)

aabbMid = aabbMin + aabbMax
aabbMid *= 0.5

print("aabb min: " + str(aabbMin))
print("aabb max: " + str(aabbMax))
print("aabb mid: " + str(aabbMid))

for vertex in vertices:
    coord = vertex.co
    if (coord.z < minHeight or maxHeight < coord.z): continue
    angle = vectorAngle(coord - aabbMid)
    angleOffset = getOffsetFromQuarter(angle)
    if (angleOffset > threadAngle): continue
    heightChange = (angleOffset / threadAngle) * threadHeight
    coord.z += heightChange
    
