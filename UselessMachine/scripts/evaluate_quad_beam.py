import bpy
import math

STOPPER_OFFSET = math.radians(60)
FRAME_OFFSET = 10

def compute_endpoint(beam_obj):
    length = beam_obj.scale.x
    location = beam_obj.location
    rotation = beam_obj.rotation_euler.y
    end_x = math.cos(rotation) * length + location.x
    end_z = math.sin(-rotation) * length + location.z # Z-up
    return end_x, end_z

def circle_intersect(p0, p1, r0, r1, ref_pos):
	""" returns nearest point in circle-circle intersection to ref_pos """
	# http://paulbourke.net/geometry/circlesphere/
	# distance d between circle centers
	d_x = p0.x - p1.x;
	d_z = p0.z - p1.z;
	d = math.sqrt(d_x * d_x + d_z * d_z)
	if d > (r0 + r1): return None # no intersection; circles are too far apart
	if d < abs(r0 - r1): return None # no intersection; circle contains other

	a = (r0 * r0 - r1 * r1 + d * d) / (2.0 * d)
	h = math.sqrt(r0 * r0 - a * a)
	p2_x = p0.x + a * (p1.x - p0.x) / d
	p2_z = p0.z + a * (p1.z - p0.z) / d

	# circle intersect 1
	p3_1x = p2_x + h * (p1.z - p0.z) / d
	p3_1z = p2_z - h * (p1.x - p0.x) / d

	# circle intersect 2
	p3_2x = p2_x - h * (p1.z - p0.z) / d
	p3_2z = p2_z + h * (p1.x - p0.x) / d

	dist_1_x = p3_1x - ref_pos[0]
	dist_1_z = p3_1z - ref_pos[1]

	dist_2_x = p3_2x - ref_pos[0]
	dist_2_z = p3_2z - ref_pos[1]

	if (dist_2_x * dist_2_x + dist_2_z * dist_2_z) > (dist_1_x * dist_1_x + dist_1_z * dist_1_z):
		return (p3_1x, p3_1z)
	else:
		return (p3_2x, p3_2z)

def rotate_beam_towards_point(beam_obj, point_x, point_z):
      d_z = point_z - beam_obj.location.z
      d_x = point_x - beam_obj.location.x
      beam_obj.rotation_euler.y = -math.atan2(d_z, d_x)

def compute_transforms(arm_rotation_degrees):
    arm_rotation_radians = math.radians(arm_rotation_degrees)
    bpy.data.objects["driveshaft"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["gear_a"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["gear_b"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["stopper"].rotation_euler.y = arm_rotation_radians + STOPPER_OFFSET
    # beam_a is fixed to the gear
    beam_a = bpy.data.objects["beam_a"]
    beam_a.rotation_euler.y = arm_rotation_radians
    # beam_b rotates around the end of beam_a
    beam_b = bpy.data.objects["beam_b"]
    beam_b_loc_x, beam_b_loc_z = compute_endpoint(beam_a)
    beam_b.location.x = beam_b_loc_x
    beam_b.location.z = beam_b_loc_z
    # beam_c rotates around the end of the fixed_beam
    beam_c = bpy.data.objects["beam_c"]
    beam_c_loc_x, beam_c_loc_z = compute_endpoint(bpy.data.objects["fixed_beam"])
    beam_c.location.x = beam_c_loc_x
    beam_c.location.z = beam_c_loc_z
    # point beam_c and beam_a at the same endpoint - this is one of the intersections of
    # the two circles formed by their positions and radii
    current_endpoint = compute_endpoint(beam_b)
    common_x, common_z = circle_intersect(beam_b.location, beam_c.location, beam_b.scale.x, beam_c.scale.x, current_endpoint)
    rotate_beam_towards_point(beam_b, common_x, common_z)
    rotate_beam_towards_point(beam_c, common_x, common_z)

def frame_update_handler(scene):
    compute_transforms((bpy.context.scene.frame_current - 1 + FRAME_OFFSET) * 3.6)
    # match some of the test area transforms
    objs_to_match = [
        "gear_a",
        "gear_b",
        "beam_a",
        "beam_b",
        "beam_c",
        "driveshaft",
        "stopper"
    ]
    for obj_name in objs_to_match:
        obj_src = bpy.data.objects[f"{obj_name}"]
        obj_tgt = bpy.data.objects[f"{obj_name}.001"]
        obj_tgt.rotation_euler.y = obj_src.rotation_euler.y
        obj_tgt.location.x = obj_src.location.x
        obj_tgt.location.z = obj_src.location.z

bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frame_update_handler)
