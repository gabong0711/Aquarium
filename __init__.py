'''
Copyright (C) 2025 Nhi Nguyen
punie.nhinguyen@gmail.com

'''
bl_info = {
    "name": "Aquarium RigTool",
    "author": "Nhi Nguyen",
    "version": (0,1,0),
    "blender": (4,4,0),
    "location": "3D Viewport > Sidebar > Aquarium",
    "description": "Useful rigtool",
    "category": "Rigging",
}

import bpy 
import os

from . import bl_class_registry
# from . import operators
# from . import prefs
from . import menus

def register():
#     # operators.register()
    menus.register()
    bl_class_registry.BlClassRegistry.register()
def unregister():
#     # operators.unregister()
    menus.unregister()
    bl_class_registry.BlClassRegistry.unregister()
if __name__ == "__main__":
    register()
