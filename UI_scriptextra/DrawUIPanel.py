import bpy
from bpy.types import Context, Menu, Panel
#UI Collection preset planning
class VIEW3D_PT_edit_drawLayerButton(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Edit Layer2"
    def draw(self, context):
        layout = self.layout
        layout.label(text ="Chim tren troi")


classes = (
    VIEW3D_PT_edit_drawLayerButton,
    
)


def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)


  

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    
