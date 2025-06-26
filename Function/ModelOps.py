import bpy
from bpy.types import (
    Context,
    Menu
)

class PurgeOperator(bpy.types.Operator):
    bl_idname = "object.purge_operator"
    bl_label = "Purge"
    
    def execute(self, context):
        bpy.ops.outliner.orphans_purge()

        return {'FINISHED'}

class OBJECT_OT_SelectObjectsWithShapeKeys(bpy.types.Operator):
    bl_idname = "object.select_with_shape_keys"
    bl_label = "Select Objects with Shape Keys"
    bl_description = "Select all objects with shape keys"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.data.shape_keys:
                obj.select_set(True)
        return {'FINISHED'}

class OBJECT_OT_SelectObjectsWithModifiers(bpy.types.Operator):
    bl_idname = "object.select_with_modifiers"
    bl_label = "Select Objects with Modifiers"
    bl_description = "Select all objects with modifiers"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.modifiers:
                obj.select_set(True)
        return {'FINISHED'}

class OBJECT_OT_RemoveModifiers(bpy.types.Operator):
    bl_idname = "object.remove_modifiers"
    bl_label = "Remove Modifiers"
    bl_description = "Remove all modifiers from selected objects"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
            for modifier in obj.modifiers:
                    obj.modifiers.remove(modifier)
            obj.select_set(False)
        return {'FINISHED'}

class SelectFaceBySidesOperator(bpy.types.Operator):
    bl_idname = "object.select_face_by_sides"
    bl_label = "Select Faces by Sides"
    bl_description = "Select faces with a number of sides greater than 4"
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
        return {'FINISHED'} 

class OBJECT_OT_SelectObjectsWithNGon(bpy.types.Operator):
    bl_idname = "object.select_with_n_gon"
    bl_label = "Select Objects with N Gon"
    bl_description = "Select all objects with N Gon"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.select_all(action='DESELECT')
        objects_with_selected_faces = []
                
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                # Check if any faces are selected in the object
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
                if obj.data.polygons:
                    for poly in obj.data.polygons:
                        if poly.select:
                            objects_with_selected_faces.append(obj)
                            break
                bpy.ops.object.mode_set(mode='OBJECT')
                
        for slobj in objects_with_selected_faces:
            slobj.select_set(True)
                
        return {'FINISHED'}   

def check_display_device_and_view_transform(self, context):
    display_device = bpy.context.scene.display_settings.display_device
    view_transform = bpy.context.scene.view_settings.view_transform

    #bpy.context.window_manager.popup_menu(display_device_message, title="Display Device Notification")

    #bpy.context.window_manager.popup_menu(view_transform_custom_message, title="View Transform Notification")
    message = ""
   
    message = "Display device is set to '{}'.\n".format(display_device)
   
   
    message += "View transform is set to '{}'.".format(view_transform)

    self.layout.label(text=message)


class OBJECT_OT_PopUp(bpy.types.Operator):
    bl_idname = "object.select_with_pop_up"
    bl_label = "PopUp"
    bl_description = "PopUP"

    def execute(self, context):
        bpy.context.window_manager.popup_menu(check_display_device_and_view_transform, title="Display and View Transform Notifications")
        return {'FINISHED'}
        



class VIEW3D_MT_PIE_template(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "CG GameModel Check"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
       
        pie.operator("object.purge_operator", text= "Purge",icon="ORPHAN_DATA")
        #pie.operator("object.select_with_pop_up", text= "Color Management",icon="SEQUENCE_COLOR_01")

        box = pie.split().box()
        col = box.column(align=True)
        col.operator("object.select_with_shape_keys", text= "Shapekey object",icon="RESTRICT_SELECT_OFF")
        col.operator("object.select_with_modifiers", text= "Modified object",icon="RESTRICT_SELECT_OFF")
        
        pie.operator("object.remove_modifiers", text= "Remove all object's modifies",icon="X")
        
        box = pie.split().box()
        col = box.column(align= True)
        col.operator("object.select_face_by_sides", text= "N-gon Face (EditMode)",icon="RESTRICT_SELECT_OFF")
        col.operator("object.select_with_n_gon", text= "N-gon Objects",icon="RESTRICT_SELECT_OFF")
        

global_addon_keymaps = []





cls= {
    OBJECT_OT_SelectObjectsWithShapeKeys,
    
    PurgeOperator,
    OBJECT_OT_SelectObjectsWithModifiers,
    OBJECT_OT_RemoveModifiers,
    SelectFaceBySidesOperator,
    OBJECT_OT_SelectObjectsWithNGon,
    VIEW3D_MT_PIE_template,
    OBJECT_OT_PopUp

    
    }
    
def register():
    from bpy.utils import register_class
    for c in cls:
        register_class(c)
    
   

    
    window_manager = bpy.context.window_manager
    if window_manager.keyconfigs.addon:
        keymap = window_manager.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")

        keymap_item = keymap.keymap_items.new("wm.call_menu_pie", "D", "PRESS", ctrl=True, alt=True)
        keymap_item.properties.name = "VIEW3D_MT_PIE_template"

        # save the key map to deregister later
        global_addon_keymaps.append((keymap, keymap_item))
        
def unregister():
    from bpy.utils import unregister_class
    for c in cls:
        unregister_class(c)
    
   
 
   
    window_manager = bpy.context.window_manager
    if window_manager and window_manager.keyconfigs and window_manager.keyconfigs.addon:
        for keymap, keymap_item in global_addon_keymaps:
            keymap.keymap_items.remove(keymap_item)

    global_addon_keymaps.clear()    
        