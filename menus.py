import bpy
from bpy.types import Menu, Panel


class VIEW3D_PT_MainMenu(Panel):
    bl_label = "Main Menu"
    bl_idname = "VIEW3D_PT_mainmenu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
 
    
    def draw(self, context):
        layout = self.layout
        layout.label(text ="abc")


classes = (
    VIEW3D_PT_MainMenu,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
