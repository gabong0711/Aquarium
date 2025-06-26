#Python access to blender
import bpy
#from bpy.types import Context

from math import pi, sin

from bpy.props import (
    StringProperty, BoolProperty, FloatProperty, IntProperty
  )

#propties get target rig
class MyAddonProperties(bpy.types.PropertyGroup):
    
    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Target Rig",
        description="Generated & Finalize Armature",
        poll=lambda self, obj: obj.type == 'ARMATURE' and obj.data is not self)
    
    hair: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Hair Rig",
        description="Simulated bone",
        poll=lambda self, obj: obj.type == 'ARMATURE' and obj.data is not self)
    
    metarig: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Meta Rig",
        description="The Meta rig",
        poll=lambda self, obj: obj.type == 'ARMATURE' and obj.data is not self)
    
    influence: FloatProperty(
        name="Influence",
        default=0.7,
        min=0.0,
        max=1.0
    )
      

    distance_threshhold: FloatProperty(
        name="Distance Threshhold",
        default=0.07,
        min=0.0,
        max=1.0
    )
    
    angle_dissolve: FloatProperty(
        name="Angle Dissolve",
        default= 0.175,
        min=0.0,
        max=1.0
    )
    BindSub: IntProperty(
        name="Sub to bind",
        default= 0,
        min=0,
        max=3
    )

class custom_prop(bpy.types.PropertyGroup):
    
    bind_unbind_property: BoolProperty(
        name		 = "Bind/Unbind"
        ,description = "Show the binding status"
        ,default	 = True
        ,override	 = {'LIBRARY_OVERRIDABLE'}
    )
    bind_unbind_text: StringProperty (
    default= 'BIND'
    )
    bind_unbind_icon : StringProperty(
    default="UNLINKED")
   
class BindorUnbindOperator(bpy.types.Operator):
    bl_idname = "object.bindorunbindops"
    bl_label = "Toggle bind or unbind"

    status: bpy.props.BoolProperty()
    
    def execute(self, context):
        # Toggle the bind/unbind property
        context.scene.Custom_prop.bind_unbind_property = not context.scene.Custom_prop.bind_unbind_property
        bpy.ops.object.hairbind()
        # Update the icon based on the on/off status
        if context.scene.Custom_prop.bind_unbind_property:
            context.scene.Custom_prop.bind_unbind_icon = "UNLINKED"
            context.scene.Custom_prop.bind_unbind_text = 'BIND'
        else:
            context.scene.Custom_prop.bind_unbind_icon = "LINKED"
            context.scene.Custom_prop.bind_unbind_text = 'UNBIND'
        
        return {'FINISHED'}
  

#propties get custom viewportdisplay


def move_bone_to_layer(armature_obj, bone_name, new_layer_index, keep_in_both_layers=False):
    

    # Get the armature data
    armature_data = armature_obj.data
    
    # Get the bone
   
    
    if bone_name in armature_obj.data.bones:
         
        bone = armature_data.bones[bone_name]
        # Clear the bone's current layer
        for index, layer in enumerate(armature_data.layers):
            if layer:
                if (index!= new_layer_index):              
                   if keep_in_both_layers != 0:
                       bone.layers[index] = False
        
        # Move the bone to the new layer
        bone.layers[new_layer_index] = True
        
        
        
        
    else:
        print("Bone not found.")

class CleanUpLayer(bpy.types.Operator):
    bl_idname = "object.cleanup_ops"
    bl_label = "CleanUpLayer"
    bl_description = "Moving control in right layer"
    def execute(self, context):
        
        #Perform some operation using the input variable
        
        target = context.scene.my_addon_props.target
       
        
        #move 
        #1: only layer
        #0: keep in old_layer 
        rarelyuse=18
        nonuse=27
        move_bone_to_layer(target,'Properties',30,1)

        move_bone_to_layer(target,'TGT-MainEye.L',1,1)
        move_bone_to_layer(target,'TGT-MainEye.R',1,1)

        move_bone_to_layer(target,'root',28,1)
        move_bone_to_layer(target,'P-root',28,1)
        
        move_bone_to_layer(target,'ROOT-Head',nonuse,1)
        move_bone_to_layer(target,'ROOT-Neck',nonuse,1)
        
        move_bone_to_layer(target,'ROOT-Thigh.L',nonuse,1)
      
        
        move_bone_to_layer(target,'ROOT-MainEye.L',nonuse,1)
        move_bone_to_layer(target,'ROOT-UpperArm.L',nonuse,1)
       
        move_bone_to_layer(target,'IK-UpperArm.L',rarelyuse,1)
        #move_bone_to_layer(target,'ROLL-Foot.L',rarelyuse,1)
        move_bone_to_layer(target,'IK-Thigh.L',rarelyuse,1)
        
        
        move_bone_to_layer(target,'ROOT-Thigh.R',nonuse,1)
      
        move_bone_to_layer(target,'ROOT-MainEye.R',nonuse,1)
        move_bone_to_layer(target,'ROOT-UpperArm.R',nonuse,1)
        move_bone_to_layer(target,'IK-UpperArm.R',rarelyuse,1)

        #move_bone_to_layer(target,'ROLL-Foot.R',rarelyuse,1)
        move_bone_to_layer(target,'IK-Thigh.R',rarelyuse,1)
        
        move_bone_to_layer(target,'SQ-JawSquash',rarelyuse,1)
      
        #rareuse
        #move_bone_to_layer(target,'FK-Neck',rarelyuse,1)
        #move_bone_to_layer(target,'FK-Shoulder.L',rarelyuse,1)
        #move_bone_to_layer(target,'FK-Shoulder.R',rarelyuse,1)
        
        
        #hand & finger
        move_bone_to_layer(target,'FK-P-UpperArm.R',rarelyuse,1)
        move_bone_to_layer(target,'FK-P-UpperArm.L',rarelyuse,1)
        
        move_bone_to_layer(target,'IK-MSTR-C-Wrist.L',rarelyuse,1)
        move_bone_to_layer(target,'IK-MSTR-C-Wrist.R',rarelyuse,1)
        
        
        #toe & foot 
        move_bone_to_layer(target,'RIK-Foot.L',20,1)
        #move_bone_to_layer(target,'RIK-Foot.L',21,0)
       
        move_bone_to_layer(target,'RIK-Foot.R',23,1)
        #move_bone_to_layer(target,'RIK-Foot.R',24,0)
       
        move_bone_to_layer(target,'FK-Toes.L',20,1)
        move_bone_to_layer(target,'FK-Toes.L',21,0)

        move_bone_to_layer(target,'FK-Toes.R',23,1)
        move_bone_to_layer(target,'FK-Toes.R',24,0)
        
        move_bone_to_layer(target,'Roll2.L',20,1)
        #move_bone_to_layer(target,'Roll2.L',21,0)
        
        move_bone_to_layer(target,'Roll3.L',20,1)
        #move_bone_to_layer(target,'Roll3.L',21,0)
        
        move_bone_to_layer(target,'Roll2.R',23,1)
        #move_bone_to_layer(target,'Roll2.R',24,0)
        
        move_bone_to_layer(target,'Roll3.R',23,1)
        #move_bone_to_layer(target,'Roll3.R',24,0)
        


        #spine FK vo 2 layer
        move_bone_to_layer(target,'FK-RibCage',11,1)
        move_bone_to_layer(target,'FK-RibCage',12,0)
        
        move_bone_to_layer(target,'FK-Chest',11,1)
        move_bone_to_layer(target,'FK-Chest',12,0)
        
        move_bone_to_layer(target,'MSTR-Spine_Torso',12,0)
        move_bone_to_layer(target,'MSTR-P-Spine_Chest',13,1)
       
        #P-spine to def gimbal
        move_bone_to_layer(target,'MSTR-Spine_Torso',rarelyuse,1)
        move_bone_to_layer(target,'MSTR-Spine_Chest',rarelyuse,1) 
       
        #facial
        #eyeL
        move_bone_to_layer(target,'CTR-MainEye.L',2,1)
        move_bone_to_layer(target,'CTR-MainEye_Highlight.L',1,1)
        move_bone_to_layer(target,'ROOT-MainEye.L',nonuse,1)
        #eyeR
        move_bone_to_layer(target,'CTR-MainEye.R',2,1)
        move_bone_to_layer(target,'CTR-MainEye_Highlight.R',1,1)
        move_bone_to_layer(target,'ROOT-MainEye.R',nonuse,1)
        
        self.report({'INFO'}, "Cleanup: " + target.name)
        return {'FINISHED'}


class ksetting(bpy.types.Operator):
    bl_idname = "object.ksetting_ops"
    bl_label = "FKIKsetting"
    bl_description = "Setting default of IK- FK"
    def execute(self, context):
        
        #Perform some operation using the input variable
        
        target = context.scene.my_addon_props.target
       
        target.pose.bones["Properties"]["ik_left_upperarm"] = 0.0
        target.pose.bones["Properties"]["ik_right_upperarm"] = 0.0
        #bpy.ops.pose.cloudrig_snap_bake(bones="[\"IK-POLE-UpperArm.L\"]", prop_bone="Properties", prop_id="ik_pole_follow_left_upperarm", select_bones=True)
        #bpy.ops.pose.cloudrig_snap_bake(bones="[\"IK-POLE-UpperArm.R\"]", prop_bone="Properties", prop_id="ik_pole_follow_right_upperarm", select_bones=True)

        target.pose.bones["Properties"]["ik_pole_follow_left_thigh"] = target.pose.bones["Properties"]["ik_stretch_left_finger_index1"]
        #target.pose.bones["Properties"]["ik_pole_follow_left_upperarm"] = target.pose.bones["Properties"]["ik_stretch_left_finger_index1"] 
        target.pose.bones["Properties"]["ik_pole_follow_right_thigh"] = target.pose.bones["Properties"]["ik_stretch_left_finger_index1"]
        #target.pose.bones["Properties"]["ik_pole_follow_right_upperarm"] = target.pose.bones["Properties"]["ik_stretch_left_finger_index1"]
        
        
        #Eyelid
        target.pose.bones["MainEyeTrack.L"]["EyelidFollow"] = target.pose.bones["Properties"]["ik_pole_follow_left_upperarm"]
        target.pose.bones["MainEyeTrack.R"]["EyelidFollow"] = target.pose.bones["Properties"]["ik_pole_follow_left_upperarm"]

        


        
        
        self.report({'INFO'}, "Setting IKFK done: " + target.name)
        return {'FINISHED'}
    
class Armaturesetting(bpy.types.Operator):
    bl_idname = "object.armature_setting"
    bl_label = "Armaturesetting"
    bl_description = "Setting default of Armature and get rid of test-action"
    def execute(self, context):
        
        #Perform some operation using the input variable
        
        target = context.scene.my_addon_props.target
        target.show_in_front= False
        target.data.show_axes= False

        bpy.ops.object.unlink_action()
        self.report({'INFO'}, "Setting armature done: " + target.name)
        return {'FINISHED'}

def VPtranslation(target,bone_name,X,axis):
     #from obj to armature
     target_data=target.data
     if bone_name in target_data:
         target.pose.bones[bone_name].custom_shape_translation[axis]=X

def VProtation(target,bone_name,X,axis):
     #from obj to armature
     target_data=target.data
     if bone_name in target_data:
         target.pose.bones[bone_name].custom_shape_rotation_euler[axis]=X

def VPscale(target,bone_name,X,axis):
     #from obj to armature
     target_data=target.data
     if bone_name in target_data:
         target.pose.bones[bone_name].custom_shape_scale_xyz[axis]=X

class ControlViewportdisplay(bpy.types.Operator):
    bl_idname = "object.control_viewport_display"
    bl_label = "Viewport Display of control"
    bl_description = "Right rotation for shoulder control display"
    def execute(self, context):
        target = context.scene.my_addon_props.target
        #rotate 90
        target.pose.bones["FK-Shoulder.R"].custom_shape_rotation_euler[1] =-1.5707963705062866
        #FOOT

        #RIK- Toes
        target.pose.bones["RIK-Toes.L"].custom_shape = target.pose.bones["Roll3.R"].custom_shape
        vscale=0.03
        target.pose.bones["RIK-Toes.L"].custom_shape_scale_xyz[0]=vscale
        target.pose.bones["RIK-Toes.L"].custom_shape_scale_xyz[1]=vscale
        target.pose.bones["RIK-Toes.L"].custom_shape_scale_xyz[2]=vscale
        target.pose.bones["RIK-Toes.L"].custom_shape_rotation_euler[0]= -2.2165682315826416


        target.pose.bones["RIK-Toes.R"].custom_shape = target.pose.bones["Roll3.R"].custom_shape
        vscale=0.03
        target.pose.bones["RIK-Toes.R"].custom_shape_scale_xyz[0]=vscale
        target.pose.bones["RIK-Toes.R"].custom_shape_scale_xyz[1]=vscale
        target.pose.bones["RIK-Toes.R"].custom_shape_scale_xyz[2]=vscale
        target.pose.bones["RIK-Toes.R"].custom_shape_rotation_euler[0]= -2.2165682315826416

        #FK-toes
        target.pose.bones["FK-Toes.L"].custom_shape = target.pose.bones["FK-Shoulder.L"].custom_shape
        target.pose.bones["FK-Toes.R"].custom_shape = target.pose.bones["FK-Shoulder.L"].custom_shape
        
        target.pose.bones["FK-Toes.L"].custom_shape_scale_xyz[0] = 0.125
        target.pose.bones["FK-Toes.L"].custom_shape_scale_xyz[1] = 0.11
        target.pose.bones["FK-Toes.L"].custom_shape_scale_xyz[2] = 0.11

        target.pose.bones["FK-Toes.L"].custom_shape_translation[1] = 0.015
        target.pose.bones["FK-Toes.L"].custom_shape_translation[2] = -0.013

        target.pose.bones["FK-Toes.L"].custom_shape_rotation_euler[0] =0.27401667833328247
        target.pose.bones["FK-Toes.L"].custom_shape_rotation_euler[1] = 3.1415927410125732

        target.pose.bones["FK-Toes.R"].custom_shape_scale_xyz[0] = 0.125
        target.pose.bones["FK-Toes.R"].custom_shape_scale_xyz[1] = 0.11
        target.pose.bones["FK-Toes.R"].custom_shape_scale_xyz[2] = 0.11

        target.pose.bones["FK-Toes.R"].custom_shape_translation[1] = 0.015
        target.pose.bones["FK-Toes.R"].custom_shape_translation[2] = -0.013

        target.pose.bones["FK-Toes.R"].custom_shape_rotation_euler[0] = 0.27401667833328247
        target.pose.bones["FK-Toes.R"].custom_shape_rotation_euler[1] = 3.1415927410125732

       
        #RIK-FOOT
        target.pose.bones["RIK-Foot.L"].custom_shape = target.pose.bones["FK-Shoulder.L"].custom_shape
        target.pose.bones["RIK-Foot.R"].custom_shape = target.pose.bones["FK-Shoulder.L"].custom_shape
        
        target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[0] = 0.125
        target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[1] = 0.11
        target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[2] = 0.11

        target.pose.bones["RIK-Foot.L"].custom_shape_translation[1] = 0.015
        target.pose.bones["RIK-Foot.L"].custom_shape_translation[2] = -0.013

        target.pose.bones["RIK-Foot.L"].custom_shape_rotation_euler[0] = 0.27401667833328247
        target.pose.bones["RIK-Foot.L"].custom_shape_rotation_euler[1] = 3.1415927410125732

        target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[0] = 0.125
        target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[1] = 0.11
        target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[2] = 0.11

        target.pose.bones["RIK-Foot.R"].custom_shape_translation[1] = 0.015
        target.pose.bones["RIK-Foot.R"].custom_shape_translation[2] = -0.013

        target.pose.bones["RIK-Foot.R"].custom_shape_rotation_euler[0] = 0.27401667833328247
        target.pose.bones["RIK-Foot.R"].custom_shape_rotation_euler[1] = 3.1415927410125732



        #VProtation(target,"FK-Shoulder.R",-1.5707963705062866)
        
        #target.pose.bones["MSTR-Spine_Chest"].custom_shape_scale_xyz[1] =-0.366744
        #target.pose.bones["MSTR-P-Spine_Chest"].custom_shape_scale_xyz[1] =-0.366744
        
        #target.pose.bones["MSTR-Spine_Chest"].custom_shape_translation[1] =0.35
        #target.pose.bones["MSTR-P-Spine_Chest"].custom_shape_translation[1] =0.35
      

        #target.pose.bones["MSTR-Spine_Hips"].custom_shape_scale_xyz[1] =-0.02
        #target.pose.bones["MSTR-Spine_Hips"].custom_shape_scale_xyz[0] =0.03
        #target.pose.bones["MSTR-Spine_Hips"].custom_shape_scale_xyz[2] =0.03
        
        
        #target.pose.bones["RIK-Foot.L"].custom_shape = bpy.data.objects['WGT-Roll_Flat']
      
        #target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[0] =0.002
        #target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[1] =0.002
        #target.pose.bones["RIK-Foot.L"].custom_shape_scale_xyz[2] =0.002
        #target.pose.bones["RIK-Foot.L"].custom_shape_translation[1] =0.0070
        #target.pose.bones["RIK-Foot.L"].custom_shape_translation[2] =0.0030

        # target.pose.bones["RIK-Foot.R"].custom_shape = bpy.data.objects['WGT-Roll_Flat']

        # target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[0] =0.002
        # target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[1] =0.002
        # target.pose.bones["RIK-Foot.R"].custom_shape_scale_xyz[2] =0.002
        # target.pose.bones["RIK-Foot.R"].custom_shape_translation[1] =0.0070
        # target.pose.bones["RIK-Foot.R"].custom_shape_translation[2] =0.0030

        self.report({'INFO'}, "Fix viewport display of control: " + target.name)
        return {'FINISHED'}     

class add_rollback(bpy.types.Operator):
    bl_idname = "object.addrollback"
    bl_label = "Rollback"
    bl_description = "add mecha at rollback control"
    clicked = bpy.props.BoolProperty(default=False)
    def execute(self, context):
        
        
        target = context.scene.my_addon_props.target
        
        constraint_name= 'extraroll'
        
        #Left back roll
        #not able to repeat
        IKboneL= target.pose.bones['IK-RollBack.L']
        has_constraint = any(constraint.name == constraint_name for constraint in IKboneL.constraints)
        if not has_constraint:
            constraint = IKboneL.constraints.new(type='TRANSFORM')
            constraint.name = constraint_name
            #able to repeat
            IKboneL.constraints[constraint_name].target = target
            IKboneL.constraints[constraint_name].subtarget = 'Roll2.L'
            IKboneL.constraints[constraint_name].target_space = 'LOCAL'
            IKboneL.constraints[constraint_name].owner_space = 'LOCAL'

            IKboneL.constraints[constraint_name].map_from = 'ROTATION'
            IKboneL.constraints[constraint_name].from_min_x_rot = -1.5707963705062866
            IKboneL.constraints[constraint_name].from_max_x_rot = 1.5707963705062866

            IKboneL.constraints[constraint_name].map_to = 'ROTATION'
            IKboneL.constraints[constraint_name].to_min_x_rot = 1.0471975803375244
            IKboneL.constraints[constraint_name].to_max_x_rot = -1.0471975803375244

            IKboneL.constraints[constraint_name].mix_mode_rot = 'BEFORE'

        #Right back roll
        #not able to repeat
        IKboneR= target.pose.bones['IK-RollBack.R']
        has_constraint = any(constraint.name == constraint_name for constraint in IKboneR.constraints)
        if not has_constraint:
            constraint = IKboneR.constraints.new(type='TRANSFORM')
            constraint.name = constraint_name
            #able to repeat    
            IKboneR.constraints[constraint_name].target = target
            IKboneR.constraints[constraint_name].subtarget = 'Roll2.R'
            IKboneR.constraints[constraint_name].target_space = 'LOCAL'
            IKboneR.constraints[constraint_name].owner_space = 'LOCAL'

            IKboneR.constraints[constraint_name].map_from = 'ROTATION'
            IKboneR.constraints[constraint_name].from_min_x_rot = -1.5707963705062866
            IKboneR.constraints[constraint_name].from_max_x_rot = 1.5707963705062866

            IKboneR.constraints[constraint_name].map_to = 'ROTATION'
            IKboneR.constraints[constraint_name].to_min_x_rot = 1.0471975803375244
            IKboneR.constraints[constraint_name].to_max_x_rot = -1.0471975803375244

            IKboneR.constraints[constraint_name].mix_mode_rot = 'BEFORE'
        
        

        #LEFT Front Roll
        RIKboneL= target.pose.bones['RIK-Foot.L']
        has_constraint = any(constraint.name == constraint_name for constraint in RIKboneL.constraints)
        if not has_constraint:
            constraint = RIKboneL.constraints.new(type='COPY_ROTATION')
            constraint.name = constraint_name

            #FOOT
            #target.pose.bones['RIK-Foot.L'].constraints.new(type='COPY_ROTATION')

            #able to repeat
            RIKboneL.constraints[constraint_name].target = target
            RIKboneL.constraints[constraint_name].subtarget = 'Roll3.L'
            RIKboneL.constraints[constraint_name].target_space = 'LOCAL'
            RIKboneL.constraints[constraint_name].owner_space = 'LOCAL'
            RIKboneL.constraints[constraint_name].mix_mode = 'AFTER'
            RIKboneL.constraints[constraint_name].invert_x = True
        
        
        #TOE
        RIKtoeL= target.pose.bones['RIK-Toes.L']
        has_constraint = any(constraint.name == constraint_name for constraint in RIKtoeL.constraints)
        if not has_constraint:
            constraint = RIKtoeL.constraints.new(type='COPY_ROTATION')
            constraint.name = constraint_name
            #repeat able
            #target.pose.bones['RIK-Toes.L'].constraints.new(type='COPY_ROTATION')
            RIKtoeL.constraints[constraint_name].target = target
            RIKtoeL.constraints[constraint_name].subtarget = 'Roll3.L'
            RIKtoeL.constraints[constraint_name].target_space = 'LOCAL'
            RIKtoeL.constraints[constraint_name].owner_space = 'LOCAL'
            RIKtoeL.constraints[constraint_name].mix_mode = 'AFTER'
            RIKtoeL.constraints[constraint_name].invert_x = True

        
        #RIGHT Front Roll

        RIKboneR= target.pose.bones['RIK-Foot.R']
        has_constraint = any(constraint.name == constraint_name for constraint in RIKboneR.constraints)
        if not has_constraint:
            constraint = RIKboneR.constraints.new(type='COPY_ROTATION')
            constraint.name = constraint_name
            #FOOT
            #RIKboneR.constraints.new(type='COPY_ROTATION')
            RIKboneR.constraints[constraint_name].target = target
            RIKboneR.constraints[constraint_name].subtarget = 'Roll3.R'
            RIKboneR.constraints[constraint_name].target_space = 'LOCAL'
            RIKboneR.constraints[constraint_name].owner_space = 'LOCAL'
            RIKboneR.constraints[constraint_name].mix_mode = 'AFTER'
            RIKboneR.constraints[constraint_name].invert_x = True
    
        #TOE
        RIKtoeR= target.pose.bones['RIK-Toes.R']
        has_constraint = any(constraint.name == constraint_name for constraint in RIKtoeR.constraints)
        if not has_constraint:
            constraint = RIKtoeR.constraints.new(type='COPY_ROTATION')
            constraint.name = constraint_name

            #RIKtoeR.constraints.new(type='COPY_ROTATION')
            RIKtoeR.constraints[constraint_name].target = target
            RIKtoeR.constraints[constraint_name].subtarget = 'Roll3.R'
            RIKtoeR.constraints[constraint_name].target_space = 'LOCAL'
            RIKtoeR.constraints[constraint_name].owner_space = 'LOCAL'
            RIKtoeR.constraints[constraint_name].mix_mode = 'AFTER'
            RIKtoeR.constraints[constraint_name].invert_x = True
        
        self.report({'INFO'}, "Add roll bone: " + target.name)
        #else:
        #   self.report({'WARNING'}, "Button can only be clicked once.")

        return {'FINISHED'}


class change_constraintTg(bpy.types.Operator):
    bl_idname = "object.change_constraint_tg"
    bl_label = "changeConstraintTarget"
    bl_description = "Find and replace the constraint that loose target when generate whole new RIG"
    def execute(self, context):
        final = context.scene.my_addon_props.target
       
        check = context.scene.my_addon_props.metarig
        bones = check.pose.bones
        for bone in bones:
             constrains = bone.constraints
             for i in constrains:
                    if i.type == 'ARMATURE':
                        for tg in i.targets:
                           if tg.target != check or tg.target == None:
                                tg.target =final
                                
                    if i.type in ["COPY_LOCATION", "LIMIT_DISTANCE", "TRACK_TO","COPY_TRANSFORMS", "COPY_LOCATION", "TRANSFORM","FLOOR"]:
                        if ((i.target != check) or (i.target == None)):
                            i.target = final
                        if i.target_space == "CUSTOM" or i.owner_space:
                            if i.space_object != check:
                                i.space_object = final

        
        self.report({'INFO'}, "ReAssign constraint target in metarig: " + check.name)
        return {'FINISHED'}    
        


class OnOffOperator(bpy.types.Operator):
    bl_idname = "object.on_off_ops"
    bl_label = "Toggle On/Off"

    status: bpy.props.BoolProperty()
    
    def execute(self, context):
        # Toggle the on/off property
        context.scene.on_off_property = not context.scene.on_off_property
        
        # Update the icon based on the on/off status
        if context.scene.on_off_property:
            context.scene.on_off_icon = "HIDE_ON"
        else:
            context.scene.on_off_icon = "HIDE_OFF"
        
        # Store the status in the variable
        global Status
        Status = context.scene.on_off_property
        
        return {'FINISHED'}
 
class SymmetryTargetContraintsRside(bpy.types.Operator):
    bl_idname = "object.symmetry_target_contraints_rside"
    bl_label = "SymmetryTarget"
    bl_description = "Replace the symmetry target & sub target on selected bones"
    def execute(self, context):
       
        armature = context.scene.my_addon_props.metarig
        # Get the selected bones
        selected_bones = [bone for bone in armature.data.bones if bone.select]

        # Iterate over the selected bones
        for bone in selected_bones:
            # Iterate over all constraints of the bone
            if ((".R" in bone.name) and len(armature.pose.bones[bone.name].constraints) !=0):
                
                for constraint in armature.pose.bones[bone.name].constraints:
                    # Check if the constraint has the subtarget property
                    if (".L" in constraint.name) :
                            oldname = constraint.name
                            newname = oldname.replace(".L", ".R")
                            constraint.name = newname
                    if constraint.type == 'ARMATURE':
                                for tg in constraint.targets:
                                   
                                        
                                        subtarget = tg.subtarget
                                        new_subtarget = subtarget.replace(".L", ".R")
                                        tg.subtarget = new_subtarget   
                    else :                   
                        if hasattr(constraint, "subtarget"):
                            # Get the current subtarget
                            subtarget = constraint.subtarget
                            
                            # Replace ".L" with ".R" in the subtarget
                            new_subtarget = subtarget.replace(".L", ".R")
                            
                            # Set the updated subtarget
                            constraint.subtarget = new_subtarget
                        if hasattr(constraint, "space_subtarget"):
                            # Get the current subtarget
                            space_subtarget = constraint.space_subtarget
                            
                            # Replace ".L" with ".R" in the subtarget
                            new_space_subtarget = space_subtarget.replace(".L", ".R")
                            
                            # Set the updated subtarget
                            constraint.space_subtarget = new_space_subtarget
                            
                   
                            
        self.report({'INFO'}, "ReAssign constraint target in R side: " + armature.name)
        return {'FINISHED'}  
    
class SymmetryTargetContraintsLside(bpy.types.Operator):
    bl_idname = "object.symmetry_target_contraints_lside"
    bl_label = "SymmetryTarget"
    bl_description = "Replace the symmetry target & sub target on selected bones"
    def execute(self, context):
       
        armature = context.scene.my_addon_props.metarig
        # Get the selected bones
        selected_bones = [bone for bone in armature.data.bones if bone.select]

        # Iterate over the selected bones
        for bone in selected_bones:
            # Iterate over all constraints of the bone
            if ((".L" in bone.name) and len(armature.pose.bones[bone.name].constraints) !=0):
                
                for constraint in armature.pose.bones[bone.name].constraints:
                    # Check if the constraint has the subtarget property
                    if (".R" in constraint.name) :
                            oldname = constraint.name
                            newname = oldname.replace(".R", ".L")
                            constraint.name = newname
                    if constraint.type == 'ARMATURE':
                                for tg in constraint.targets:
                                   
                                        
                                        subtarget = tg.subtarget
                                        new_subtarget = subtarget.replace(".R", ".L")
                                        tg.subtarget = new_subtarget   
                    else :                   
                        if hasattr(constraint, "subtarget"):
                            # Get the current subtarget
                            subtarget = constraint.subtarget
                            
                            # Replace ".L" with ".R" in the subtarget
                            new_subtarget = subtarget.replace(".R", ".L")
                            
                            # Set the updated subtarget
                            constraint.subtarget = new_subtarget
                        if hasattr(constraint, "space_subtarget"):
                            # Get the current subtarget
                            space_subtarget = constraint.space_subtarget
                            
                            # Replace ".L" with ".R" in the subtarget
                            new_space_subtarget = space_subtarget.replace(".R", ".L")
                            
                            # Set the updated subtarget
                            constraint.space_subtarget = new_space_subtarget
                            
                   
                            
        self.report({'INFO'}, "ReAssign constraint target in L side: " + armature.name)
        return {'FINISHED'}  


#________________________________________________________________________________________________________________________________________________________
##############
##Driver Sub##
##############   


# Function to add a driver to the Subdivision modifier level
def add_driver_to_subdivision(obj):
    # Check if the object has a Subdivision modifier
    subdivision_modifier = None
    for modifier in obj.modifiers:
        if modifier.type == 'SUBSURF':
            subdivision_modifier = modifier
            break
    target = bpy.context.scene.my_addon_props.target

    if subdivision_modifier:
 
            #viewport       
            subdivision_modifier.driver_remove("levels")
            driver = subdivision_modifier.driver_add("levels")
            driver.driver.type = 'SCRIPTED'
            driver.driver.variables.new()
            var = driver.driver.variables[0]
            var.name= 'SubdivisionLevel' 
            var.type = 'SINGLE_PROP'
            var.targets[0].id_type = 'OBJECT'
            var.targets[0].id = target
            var.targets[0].data_path = 'pose.bones["Properties_Character_Sintel"]["Sub_Viewport"]'        
            driver.driver.expression = 'SubdivisionLevel' 

            #render
            subdivision_modifier.driver_remove("render_levels")
            driver = subdivision_modifier.driver_add("render_levels")
            driver.driver.type = 'SCRIPTED'
            driver.driver.variables.new()
            var = driver.driver.variables[0]
            var.name= 'SubdivisionLevel' 
            var.type = 'SINGLE_PROP'
            var.targets[0].id_type = 'OBJECT'
            var.targets[0].id = target
            var.targets[0].data_path = 'pose.bones["Properties_Character_Sintel"]["Sub_Render"]'        
            driver.driver.expression = 'SubdivisionLevel' 
            

def get_all_collections_recursive(collection):
    collections = [collection]
    for child_collection in collection.children:
        collections.extend(get_all_collections_recursive(child_collection))
    return collections

class DriverSubdivision(bpy.types.Operator):
    bl_idname = "object.driversubdivision"
    bl_label = "Driver all subdivision"
    bl_description = "Driver all subdivision in collection model"
    def execute(self, context):
        
        collection_suffix = '_model'
        root_collections = [collection for collection in bpy.data.collections if collection.name.endswith(collection_suffix)]
        collections_to_modify = []
        for root_collection in root_collections:
            collections_to_modify.extend(get_all_collections_recursive(root_collection))


        for collection in collections_to_modify:
            # Iterate through objects in the collection
            for obj in collection.objects:
        
                print(f"Adding driver to Subdivision modifier for object '{obj.name}' in collection '{collection.name}'")
                add_driver_to_subdivision(obj)

      
        self.report({'INFO'}, "Drived all")
        return {'FINISHED'}  




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#                    
#ON OFF layer
class OBJECT_OT_TurnOnAllLayers(bpy.types.Operator):
    bl_idname = "object.turn_on_all_layers"
    bl_label = "Turn On All Layers"
    bl_description = "Turn all layers"
    def execute(self, context):
        # Get the selected armature object
        armature_obj = context.scene.my_addon_props.target.data
        # Make sure the selected object is an armature
        for bone_collection in armature_obj.collections:
            bone_collection.is_expanded = True
            bone_collection.is_visible = True

        self.report({'INFO'}, "All bone collections are now visible!")
        return {'FINISHED'}
    

class OBJECT_OT_TurnAnimLayers(bpy.types.Operator):
    bl_idname = "object.turn_anim_layers"
    bl_label = "Turn On Anim Layers"
    bl_description = "Turn anim layers"
    def execute(self, context):
        # Get the selected armature object
        armature_obj = context.scene.my_addon_props.target.data

        # List of Bone Collections need to be visible
        collection_names = ['Face', 'Body', 'Arm', 'Leg', 'Fingers', 'Root']       
        
        for bone_collection in armature_obj.collections:            
            bone_collection.is_expanded = False # !=Expand 
            bone_collection.is_visible = False # Hide 

            # bone_collection != bone_collection.parent
            # if bone_collection:
            #     bone_collection.is_visible = False
            # else:
            #     self.report({'WARNING'}, f"Failed")

        # Browse through the collection names and enable Bone Collections
        for collection_name in collection_names:
            bone_collection = armature_obj.collections.get(collection_name)
            if bone_collection:
                bone_collection.is_expanded = True
                bone_collection.is_visible = True
            else:
                self.report({'WARNING'}, f"Bone Collection '{collection_name}' not found")
       
      
            
        self.report({'INFO'}, "Specified bone collections are now visible")
        return {'FINISHED'}   
         
class OBJECT_OT_TurnOnlyRootLayers(bpy.types.Operator):
    bl_idname = "object.turn_only_root_layers"
    bl_label = "Turn Only Root Layers"
    bl_description = "Turn root layer"
    def execute(self, context):
        # Get the selected armature object
        armature_obj = context.scene.my_addon_props.target.data
        # Make sure the selected object is an armature
        armature_obj.layers[28] = True
        for layer_index in range(0,28):
                armature_obj.layers[layer_index] = False
        for layer_index in range(29,32):
                armature_obj.layers[layer_index] = False
            
        self.report({'INFO'}, "Turn Root on only")
        return {'FINISHED'}  

        
class OBJECT_OT_TurnOnlyDefLayers(bpy.types.Operator):
    bl_idname = "object.turn_only_def_layers"
    bl_label = "Turn Only Deform Layers"
    bl_description = "Turn deform layers"
    def execute(self, context):
        # Get the selected armature object
        armature_obj = context.scene.my_addon_props.target.data
        # Make sure the selected object is an armature
        armature_obj.layers[29] = True
        for layer_index in range(0,29):
                armature_obj.layers[layer_index] = False
        for layer_index in range(30,32):
                armature_obj.layers[layer_index] = False
            
        self.report({'INFO'}, "Turn Root on only")
        return {'FINISHED'}  

class OBJECT_OT_TurnOnlyMchLayers(bpy.types.Operator):
    bl_idname = "object.turn_only_mch_layers"
    bl_label = "Turn Only Machine Layers"
    bl_description = "Turn machine layers"
    def execute(self, context):
        # Get the selected armature object
        armature_obj = context.scene.my_addon_props.target.data
        # Make sure the selected object is an armature
        armature_obj.layers[30] = True
        for layer_index in range(0,30):
                armature_obj.layers[layer_index] = False
       
        armature_obj.layers[31] = False
            
        self.report({'INFO'}, "Turn Root on only")
        return {'FINISHED'} 
#wip
class OBJECT_OT_ColoryCloudmetaAdd(bpy.types.Operator):
    bl_idname = "object.colory_cloudmeta_add"
    bl_label = "Colory Metarig"
    bl_description = "Adding Colory Standard Rig"
    def execute(self, context):
        # Get the selected armature object
        
            
        self.report({'INFO'}, "It isn't ready. Keep Waiting. Will be here, soon.")
        return {'FINISHED'} 

#PURGE
class PurgeOperator(bpy.types.Operator):
    bl_idname = "object.purge_operator"
    bl_label = "Purge"
    
    def execute(self, context):
        bpy.ops.outliner.orphans_purge()

        return {'FINISHED'}
     
#Clip
class CopyToClipboardOperator(bpy.types.Operator):
    bl_idname = "my.copy_to_clipboard"
    bl_label = " "
    
    copy_text: bpy.props.StringProperty()  # Custom property to store the text to copy
    
    def execute(self, context):
        # Copy the content of copy_text to the clipboard
        bpy.context.window_manager.clipboard = self.copy_text
        return {'FINISHED'}


#1Button for all cleanup
class Magic(bpy.types.Operator):
    bl_idname = "object.magic"
    bl_label = "Magic Tools"
    bl_description = "Run all cleanup-Operators below. Exception Viewport Display."

    def execute(self, context):
        # Call the nine operators here
        bpy.ops.object.turn_on_all_layers()
        
        bpy.ops.object.cleanup_ops()
        bpy.ops.object.turn_anim_layers()    
        bpy.ops.object.ksetting_ops()
        bpy.ops.object.addrollback()
        bpy.ops.object.armature_setting()
        bpy.ops.object.unlink_action()

        
        return {'FINISHED'}

#unlinkaction
class UnlinkAction(bpy.types.Operator):
    bl_idname = "object.unlink_action"
    bl_label = "Unlink Active Action"
    bl_description = "Delete all the key and action is active in Rig Final "

    def execute(self, context):
        # Call the nine operators here
        #bpy.ops.object.turn_on_all_layers()
        target = context.scene.my_addon_props.target
        if target.animation_data:
            target.animation_data.action = None
        self.report({'INFO'}, "Unlink test action.")
        return {'FINISHED'} 



#class naming 'CATEGORY_PT_Name'

#Above this line is Function
           
cls= {
    MyAddonProperties
    ,change_constraintTg
    ,CleanUpLayer
    ,ksetting
    ,add_rollback
    ,OnOffOperator
    ,SymmetryTargetContraintsRside
    ,SymmetryTargetContraintsLside
    ,ControlViewportdisplay
    ,OBJECT_OT_TurnOnAllLayers
    ,OBJECT_OT_TurnOnlyRootLayers
    ,OBJECT_OT_TurnOnlyDefLayers
    ,OBJECT_OT_TurnOnlyMchLayers
    ,OBJECT_OT_ColoryCloudmetaAdd 
    ,DampedChain
    ,PurgeOperator
    ,OBJECT_OT_TurnAnimLayers
    ,Armaturesetting
    ,CopyToClipboardOperator
    ,Magic
    ,UnlinkAction
    ,DriverSubdivision
    ,SeperateEdge
    ,reduceVertice
    ,reduceVerticebyMD
    ,reduceVerticebyLD
    ,addArmature
    ,GenArmature
    ,addMeshDeform
    ,hairBind
    ,createconstructChain
    ,renameBone
    ,CleanMeshcage
    }

#register

def register():
    from bpy.utils import register_class
    for c in cls:
        register_class(c)
    
    # #Parent Panel
    # bpy.utils.register_class(VIEW3D_PT_beforeGenerate_panel)
    # bpy.utils.register_class(VIEW3D_PT_afterGenerate_panel)
    # bpy.utils.register_class(VIEW3D_PT_Hair_panel)
    # #Sub Panel
    # bpy.utils.register_class(parentSwitchList_SubPanel)
    
    # bpy.utils.register_class(AnimatorCleaning_SubPanel)
    # bpy.utils.register_class(VIEW3D_PT_UItidy_panel)
    # bpy.utils.register_class(generateHairbone_SubPanel)
    # bpy.utils.register_class(secondaryChain_SubPanel)
   

    
    #hid layer button
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyAddonProperties)
    bpy.types.Scene.on_off_property = bpy.props.BoolProperty(name="On/Off")
    bpy.types.Scene.on_off_icon = bpy.props.StringProperty(default="HIDE_OFF")


    #bind button
    bpy.utils.register_class(custom_prop)
    bpy.utils.register_class(BindorUnbindOperator)
    bpy.types.Scene.Custom_prop = bpy.props.PointerProperty(type=custom_prop)


   
 
def unregister():
    from bpy.utils import unregister_class
    for c in cls:
        unregister_class(c)

    # #Parent Panel
    # bpy.utils.unregister_class(VIEW3D_PT_beforeGenerate_panel)
    # bpy.utils.unregister_class(VIEW3D_PT_afterGenerate_panel)
    # bpy.utils.unregister_class(VIEW3D_PT_Hair_panel)
    # #Sub Panel
    # bpy.utils.unregister_class(parentSwitchList_SubPanel)
    
    # bpy.utils.unregister_class(AnimatorCleaning_SubPanel)
    # bpy.utils.unregister_class(VIEW3D_PT_UItidy_panel)
    # bpy.utils.unregister_class(generateHairbone_SubPanel)
    # bpy.utils.unregister_class(secondaryChain_SubPanel)

    del bpy.types.Scene.my_addon_props
    del bpy.types.Scene.on_off_property
    del bpy.types.Scene.on_off_icon

    #unbind custom
    bpy.utils.unregister_class(custom_prop)
    bpy.utils.unregister_class(BindorUnbindOperator)
    del  bpy.types.Scene.Custom_prop

   