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
 

   