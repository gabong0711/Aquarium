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


# from . import operators
# from . import prefs
from .Function import ops
from . import UI


def register():

    ops.register()
    UI.register()
   
def unregister():
    ops.unregister()
    UI.unregister()


if __name__ == "__main__":
    register()
