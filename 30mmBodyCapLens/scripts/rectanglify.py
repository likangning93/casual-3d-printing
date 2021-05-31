# Rectanglify - turn a circle of some radius into a rectangle!
# * make sure to select the object to run the script on
# * make sure selected object has "apply object transform" operation performed

import bpy
import mathutils
import math

def sign(number):
    return abs(number) / number

def lineLineIntersection(p1, p2, p3, p4):
    # http://paulbourke.net/geometry/pointlineplane/
    x1 = p1.x
    x2 = p2.x
    x3 = p3.x
    x4 = p4.x
    y1 = p1.y
    y2 = p2.y
    y3 = p3.y
    y4 = p4.y
    uaNumerator = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    uaDenominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    ua = uaNumerator / uaDenominator
    if (ua < 0.0): return float('inf')
    return ua

# set radius to the radius of the circle to look for, +/- 1 mm
radius = 8.0 # mm
epsilon = 1.0 # mm

center = mathutils.Vector((0.0, 0.0, 0.0))
halfWidth = 15.0
halfHeight = 8.0

northEast = mathutils.Vector((halfWidth, halfHeight, 0.0))
northWest = mathutils.Vector((-halfWidth, halfHeight, 0.0))
southWest = mathutils.Vector((-halfWidth, -halfHeight, 0.0))
southEast = mathutils.Vector((halfWidth, -halfHeight, 0.0))

# vertices from the selected object, the object with a loop of verts to squarify
vertices = bpy.context.object.data.vertices

for vertex in vertices:
    vec2D = vertex.co.copy()
    vec2D.z = 0.0
    dist2d = vec2D - center
    if (abs(dist2d.length - radius) > epsilon): continue

    # clamp to the nearest rectangle side
    dWest = lineLineIntersection(center, vec2D, southWest, northWest)
    dEast = lineLineIntersection(center, vec2D, southEast, northEast)
    dNorth = lineLineIntersection(center, vec2D, northWest, northEast)
    dSouth = lineLineIntersection(center, vec2D, southWest, southEast)

    dMin = min(dWest, dEast, dNorth, dSouth)
    if (dMin == dWest): vec2D = dist2d * dWest + center
    elif (dMin == dEast): vec2D = dist2d * dEast + center
    elif (dMin == dNorth): vec2D = dist2d * dNorth + center
    elif (dMin == dSouth): vec2D = dist2d * dSouth + center

    vertex.co.x = vec2D.x
    vertex.co.y = vec2D.y
