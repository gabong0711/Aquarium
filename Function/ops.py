#Python access to blender
import bpy
#from bpy.types import Context

from math import pi, sin

from bpy.props import (
    StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty
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
    show_box: bpy.props.BoolProperty(
        name="Advanced",
        description="Show advanced options",
        default=False
    )

class Custom_properties(bpy.types.PropertyGroup):
    hide_unhide_property: BoolProperty(
        name		 = "Hide/Unhide"
        ,description = "Show the visible status"
        ,default	 = True
        ,override	 = {'LIBRARY_OVERRIDABLE'}
    )
    hide_unhide_text: StringProperty (
    default= 'HIDEN'
    )
    hide_unhide_icon : StringProperty(
    default="HIDE_OFF")
    solo_icon : StringProperty(
    default="SOLO_ON")


#Meta progress 
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
        
class FixSymmetryTarget(bpy.types.Operator):
    bl_idname = "object.symmetry_target_contraints_side"
    bl_label = "SymmetryTarget"
    bl_description = "Replace the symmetry target & sub target on selected bones"
    def execute(self, context):
       
        armature = context.object
        if armature.type == 'ARMATURE':
        # Get the selected bones
            selected_bones = [bone for bone in armature.data.bones if bone.select]
            if not selected_bones:
                self.report({'INFO'}, "Didn't select any bones")
                return {'FINISHED'}
            else:                      
                # Iterate over the selected bones
                for bone in selected_bones:
                    # Iterate over all constraints of the bone
                    if (((".R" in bone.name) or (".L" in bone.name)) and len(armature.pose.bones[bone.name].constraints) !=0):
                        
                        for constraint in armature.pose.bones[bone.name].constraints:
                            # Check if the constraint has the subtarget property
                            if (".L" in constraint.name) and (".R" in bone.name)  :
                                    oldname = constraint.name
                                    newname = oldname.replace(".L", ".R")
                                    constraint.name = newname
                            elif (".R" in constraint.name) and (".L" in bone.name)  :
                                    oldname = constraint.name
                                    newname = oldname.replace(".R", ".L")
                                    constraint.name = newname
                            if constraint.type == 'ARMATURE':
                                        for tg in constraint.targets:
                                                subtarget = tg.subtarget
                                                if (".R" in bone.name)  :
                                                    new_subtarget = subtarget.replace(".L", ".R")
                                                elif  (".L" in bone.name):
                                                    new_subtarget = subtarget.replace(".R", ".L")
                                                tg.subtarget = new_subtarget                  
                            else :                   
                                if hasattr(constraint, "subtarget"):
                                    # Get the current subtarget
                                    subtarget = constraint.subtarget
                                    
                                    # Replace ".L" with ".R" in the subtarget
                                    if (".R" in bone.name)  :
                                        new_subtarget = subtarget.replace(".L", ".R")
                                    elif  (".L" in bone.name):
                                        new_subtarget = subtarget.replace(".R", ".L")
                                    # Set the updated subtarget
                                    constraint.subtarget = new_subtarget
                                if hasattr(constraint, "space_subtarget"):
                                    # Get the current subtarget
                                    space_subtarget = constraint.space_subtarget
                                    if (".R" in bone.name)  :
                                        new_space_subtarget = subtarget.replace(".L", ".R")
                                    elif  (".L" in bone.name):
                                        new_space_subtarget = subtarget.replace(".R", ".L")
                                    
                                    # Set the updated subtarget
                                    constraint.space_subtarget = new_space_subtarget
        else:
            self.report({'INFO'}, "Didn't select any armature")
            return {'FINISHED'}                       
                   
                            
        self.report({'INFO'}, "ReAssign constraint target in L/R side: " + armature.name)
        return {'FINISHED'}  

# Clean up
class OBJECT_OT_TurnOnAllCollections(bpy.types.Operator):
    bl_idname = "object.turn_on_all_bone_collections"
    bl_label = "Turn On All bone collections"
    bl_description = "Turn all bone collections"
    def execute(self, context):
        # Get the selected armature object
        obj = context.object
        armature_obj = obj.data
        # armature_obj = context.scene.my_addon_props.target.data
        # Make sure the selected object is an armature
        for bone_collection in armature_obj.collections_all:
            bone_collection.is_solo = False
            bone_collection.is_visible = True
        context.scene.Custom_prop.hide_unhide_icon = "HIDE_ON"
        context.scene.Custom_prop.solo_icon = "SOLO_OFF"
        self.report({'INFO'}, "All bone collections are now visible!")
        return {'FINISHED'}
    
class OBJECT_OT_TurnAnimCollections(bpy.types.Operator):
    bl_idname = "object.turn_anim_bone_collections"
    bl_label = "Turn On Anim bone collections"
    bl_description = "Turn anim bone collections"
    def execute(self, context):
        # Get the selected armature object
        #armature_obj = context.scene.my_addon_props.target.data
        obj = context.object
        armature_obj = obj.data
        # List of Bone Collections need to be visible
        collection_names = ['Face', 'Body', 'Arm', 'Leg', 'Fingers', 'Root']       
        
        for bone_collection in armature_obj.collections_all:            
            bone_collection.is_visible = False # Hide 

        for collection_name in collection_names:
                bone_collection = armature_obj.collections.get(collection_name)
                if bone_collection:
                    bone_collection.is_expanded = True
                    bone_collection.is_visible = True
                else:
                    self.report({'WARNING'}, f"Bone Collection '{collection_name}' not found")
       
      
            
        self.report({'INFO'}, "Specified bone collections are now visible")
        return {'FINISHED'}   
         
class OBJECT_OT_SoloBoneCollection(bpy.types.Operator):
    bl_idname = "object.turn_solo_bone_collection"
    bl_label = "Turn Only solo bone collection"
    bl_description = "Turn solo bone collection"
    bl_options = {'REGISTER', 'UNDO'}
    collection_name: bpy.props.StringProperty(name="Collection Name")
    def execute(self, context):
        
        # Get the selected armature object
        #armature_obj = context.scene.my_addon_props.target.data
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            bone_collection = obj.data.collections_all.get(self.collection_name)
            # Make sure the selected object is an armature
            if bone_collection:
                if bone_collection.is_solo == False :
                    bone_collection.is_solo = True
                    context.scene.Custom_prop.solo_icon = "SOLO_ON"
                else:
                    bone_collection.is_solo = False
                    context.scene.Custom_prop.solo_icon = "SOLO_OFF"
                    
                self.report({'INFO'}, "Turn "+ self.collection_name +" on only")
                return {'FINISHED'}  
            else:
                self.report({'WARNING'}, f"Bone Collection "+ self.collection_name + " not found")
                return {'FINISHED'}    
           
        else:
            self.report({'WARNING'}, "Not select any armature")
            return {'FINISHED'}
       
class OBJECT_OT_HideandUnhideBoneCollection(bpy.types.Operator):
    bl_idname = "object.hide_bone_collection"
    bl_label = "Hide and unhide bone collection"
    bl_description = "Hide and unhide bone collection"
    bl_options = {'REGISTER', 'UNDO'}
    collection_name: bpy.props.StringProperty(name="Collection Name")
    def execute(self, context):
        
        # Get the selected armature object
        #armature_obj = context.scene.my_addon_props.target.data
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            bone_collection = obj.data.collections_all.get(self.collection_name)
            # Make sure the selected object is an armature
            if bone_collection:
                if bone_collection.is_visible == True :
                    bone_collection.is_visible = False
                    bone_collection.is_expanded = False
                    context.scene.Custom_prop.hide_unhide_icon = "HIDE_ON"
                    self.report({'INFO'}, "Turn "+ self.collection_name +"off")
                else:
                    bone_collection.is_visible = True
                    for bc in obj.data.collections_all:
                        if bc.parent == bone_collection :
                            bc.is_visible = True
                    # bone_collection.is_expanded = True # khong can mo
                    context.scene.Custom_prop.hide_unhide_icon = "HIDE_OFF"
                    self.report({'INFO'}, "Turn "+ self.collection_name +" on")
                return {'FINISHED'}  
            else:
                self.report({'WARNING'}, f"Bone Collection "+ self.collection_name + " not found")
                return {'FINISHED'}    
           
        else:
            self.report({'WARNING'}, "Not select any armature")
            return {'FINISHED'}           

#Bone collection list

def get_bone_collections(self, context):
    items = []
    if not context.object: return items
    else: 
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            for i, col in enumerate(obj.data.collections_all):
                items.append((col.name, col.name, "", i))
        return items  

class BoneCollectionProps(bpy.types.PropertyGroup):
    cl_name: bpy.props.EnumProperty(
        name="Bone Collection",
        description="Choose a bone collection",
        items= get_bone_collections
        
    )

#Parent Clipping Board
class CopyToClipboardOperator(bpy.types.Operator):
    bl_idname = "my.copy_to_clipboard"
    bl_label = " "
    
    copy_text: bpy.props.StringProperty()  # Custom property to store the text to copy
    
    def execute(self, context):
        # Copy the content of copy_text to the clipboard
        bpy.context.window_manager.clipboard = self.copy_text
        return {'FINISHED'}


#Driver Sub
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

#Magic

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
        pb = target.pose.bones
        if all(name in pb for name in ['IK-RollBack.L', 'RIK-Foot.L', 'RIK-Toes.R']):
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
        else:
            self.report({'WARNING'}, "Not Setup baseExtraRoll.")
            return {'FINISHED'}
class ifksetting(bpy.types.Operator):
    bl_idname = "object.ifksetting_ops"
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
        #target.pose.bones["MainEyeTrack.L"]["EyelidFollow"] = target.pose.bones["Properties"]["ik_pole_follow_left_upperarm"]
        #target.pose.bones["MainEyeTrack.R"]["EyelidFollow"] = target.pose.bones["Properties"]["ik_pole_follow_left_upperarm"]

        self.report({'INFO'}, "Setting IKFK done: " + target.name)
        return {'FINISHED'}

class UnlinkAction(bpy.types.Operator):
    bl_idname = "object.unlink_action"
    bl_label = "Unlink Active Action"
    bl_description = "Delete all the key and action is active in Rig Final "
    Target: bpy.props.StringProperty(name="Target")
    def execute(self, context):
        # Call the nine operators here
        #bpy.ops.object.turn_on_all_layers()
        if (self.Target != "") :
            target = bpy.data.objects.get(self.Target)
            if target:
                if target.animation_data:
                    target.animation_data.action = None
                    self.report({'INFO'}, "Unlink test action.")
                    return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Not have any active object")
                return {'FINISHED'}
            
class Armaturesetting(bpy.types.Operator):
    bl_idname = "object.armature_setting"
    bl_label = "Armaturesetting"
    bl_description = "Setting default of Armature and get rid of test-action"
    Target: bpy.props.StringProperty(name="Target")
    def execute(self, context):
        if (self.Target != "") :
        #Perform some operation using the input variable
            target = bpy.data.objects.get(self.Target)
            if target and target.type == 'ARMATURE':
                #target = context.scene.my_addon_props.target
                target.show_in_front= False
                target.data.show_axes= False
                self.report({'INFO'}, "Setting armature done: " + target.name)
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Not select any active armature")
                return {'FINISHED'}


class Magic(bpy.types.Operator):
    bl_idname = "object.magic"
    bl_label = "Magic Tools"
    bl_description = "Run all cleanup-Operators below : anim collection on, others off, turn off infont, unlink action, IKFK default setting,add extra rollback,... "

    def execute(self, context):
        if context.scene.my_addon_props.target:
            MagicTarget = context.scene.my_addon_props.target.name
            # Call the nine operators here
            bpy.ops.object.turn_on_all_bone_collections()
            #bpy.ops.object.cleanup_ops()
            bpy.ops.object.turn_anim_bone_collections()    
            bpy.ops.object.ifksetting_ops()
            bpy.ops.object.addrollback()
            bpy.ops.object.armature_setting(Target = MagicTarget )
            bpy.ops.object.unlink_action(Target = MagicTarget )

            self.report({'INFO'},"Magic had happen")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Didn't declare Target Rig")
            return {'FINISHED'}
#unlinkaction

#_________________________________________________________________________________________________________________________________________________________________

cls= {
    MyAddonProperties,
    OBJECT_OT_TurnOnAllCollections,
    OBJECT_OT_TurnAnimCollections,
    OBJECT_OT_SoloBoneCollection,
    change_constraintTg,
    FixSymmetryTarget,
    BoneCollectionProps,
    OBJECT_OT_HideandUnhideBoneCollection,
    Custom_properties,
    CopyToClipboardOperator,
    DriverSubdivision,
    Magic,
    Armaturesetting,
    UnlinkAction,
    ifksetting,
    add_rollback,
    }

#register

def register():
    from bpy.utils import register_class
    for c in cls:
        register_class(c)


    #hid layer button
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyAddonProperties)
    bpy.types.Scene.bc_settings = bpy.props.PointerProperty(type=BoneCollectionProps)
    bpy.types.Scene.Custom_prop = bpy.props.PointerProperty(type=Custom_properties)

   
 
def unregister():
    from bpy.utils import unregister_class
    for c in cls:
        unregister_class(c)

    del bpy.types.Scene.my_addon_props
    del bpy.types.Scene.bc_settings
    del bpy.types.Scene.Custom_prop
 

   