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