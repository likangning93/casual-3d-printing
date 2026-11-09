import bpy
import math

OFFSET = math.radians(120) # 90 # 120 is a bit more "poke at highest point"
STOPPER_OFFSET = math.radians(60)
def compute_positions(arm_rotation_degrees):
    arm_rotation_radians = math.radians(arm_rotation_degrees)
    bpy.data.objects["driveshaft"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["gear_a"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["gear_b"].rotation_euler.y = arm_rotation_radians
    bpy.data.objects["stopper"].rotation_euler.y = arm_rotation_radians + STOPPER_OFFSET
    # do arm stuff
    arm_object = bpy.data.objects["arm"]
    oscillator_object = bpy.data.objects["oscillator"]
    beam_a_object = bpy.data.objects["beam_a"]
    beam_b_object = bpy.data.objects["beam_b"]
    poker_object = bpy.data.objects["poker"]
    arm_object.rotation_euler.y = arm_rotation_radians
    # compute the oscillator's end position
    arm_length = arm_object.scale.x
    arm_position = arm_object.location
    arm_end_x = math.cos(arm_rotation_radians) * arm_length + arm_position.x
    arm_end_z = math.sin(-arm_rotation_radians) * arm_length + arm_position.z # Z-up
    oscillator_object.location.x = arm_end_x
    oscillator_object.location.z = arm_end_z
    # compute oscillator and beam_a and beam_b's rotations
    beam_a_position = beam_a_object.location
    d_x = beam_a_position.x - arm_end_x
    d_z = beam_a_position.z - arm_end_z
    oscillator_object.rotation_euler.y = -math.atan2(d_z, d_x)
    beam_rotation = oscillator_object.rotation_euler.y - OFFSET
    beam_a_object.rotation_euler.y = beam_rotation
    beam_b_object.rotation_euler.y = beam_rotation
    # compute the location of the poker
    beam_a_length = beam_a_object.scale.x
    beam_a_end_x = math.cos(beam_rotation) * beam_a_length + beam_a_position.x
    beam_a_end_z = math.sin(-beam_rotation) * beam_a_length + beam_a_position.z
    poker_object.location.x = beam_a_end_x
    poker_object.location.z = beam_a_end_z

def frame_update_handler(scene):
    compute_positions((bpy.context.scene.frame_current - 1) * 3.6)
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frame_update_handler)
