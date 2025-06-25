import bpy
from bpy.types import Menu, Panel, Context
from .Function import ops
from .Function import LayerScript


class VIEW3D_PT_MainMenu(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Main Menu"
    
    
    def draw(self, context):
        layout = self.layout
        layout.label(text ="Chim tren troi")


class VIEW3D_PT_Info(Panel):
    bl_space_type =  "VIEW_3D" #3D viewport
    bl_region_type = "UI"  #side bar
    #add labels
    bl_category = "Aquarium"
    bl_label = ""
    bl_options = {"DEFAULT_CLOSED","HEADER_LAYOUT_EXPAND"}
    def draw_header(self,context):
        layout = self.layout
        layout.label(text="Infomation", icon='INFO')  # icon + label in header
        
    def draw(self, context: Context):
        """define the layout of the panel"""
        layout = self.layout
        col = layout.column()
        box = col.box()
        row = box.row()
        row.label(text="Author: Nhi Nguyen 🐱",icon="EVENT_A")
        row = box.row()
        row.label(text= "version",icon="EVENT_V")   
        row.label(text= "Support up to B4.4",icon="BLENDER") 
        
        col = layout.column()
        col.separator()
        col.separator()
        col = layout.column()
        box = col.box()
        row = box.row()
        row.operator("wm.url_open", text="Download at Github2").url = "https://github.com/gabong0711/Aquarium.git"



class RiggingTabProperties(bpy.types.PropertyGroup):
    tab: bpy.props.EnumProperty(
        name="Tabs",
        items=[
            ('DECLARE', "Declare", "Declared the armature"),
            ('GENERAL', "General", "General settings"),
            ('METARIG', "Metarig", "Metarig tools & options"),
            ('GENERATED', "Generated", "Generated tools & options"),
            ('CLEAN', "Clean Up", "Clean & Polished file"),
        ],
        default='GENERAL'
    )

class VIEW3D_PT_Rigging(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Rigging"
    bl_idname="VIEW3D_PT_Rigging"
    
    
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tool for rigging process")
        
        #Tab
        props =  context.scene.Rigging_tabs
        row =layout.row()
        row.prop(props, "tab", expand=True)
        if props.tab == 'DECLARE' :
            box = layout.box()
            box.label(text="This is the Declare tab.", icon='CURRENT_FILE')
            prop = context.scene.my_addon_props
            target = prop.target
            layout = self.layout
            col=layout.column()
            box = col.box()
            row = box.row()
            row.prop(prop, "metarig")
            row = box.row()
            row.prop(prop, "target")
            row = box.row()
            row.prop(prop, "hair")
                
        elif props.tab == 'GENERAL' :
            box = layout.box()
            box.label(text="This is the General tab.")
            row = box.row()
            row.operator("object.symmetry_target_contraints_side", text="Fix Constraint Target in Mirror Bone", icon="MOD_MIRROR")
            
        elif props.tab == 'METARIG' :
            box = layout.box()
            box.label(text="This is the METARIG tab.")
            row = box.row() 
            row.operator("object.change_constraint_tg", text="ReAssign Target", icon="GROUP_BONE")
            
            

        elif props.tab == 'GENERATED' :
            box = layout.box()
            box.label(text="This is the GENERATED tab.")
            row = box.row()
            row = box.row()
            box = layout.box()
            box.label(text="Cloud UI Script.")
            row = box.row()
            row.operator("object.textbutton_operator",text="",icon = "DUPLICATE")
            row.operator("object.textbutton_operator",text="",icon = "FILE_CACHE")
            box.label(text="Edit Layer is temporary in development process.")

        elif props.tab == 'CLEAN' :
            box = layout.box()
            box.label(text="This is Clean up tab",icon="BRUSH_DATA")
            row = box.row() 
            row.operator("object.purge_operator", text="Purge", icon="ORPHAN_DATA")  
            
            box = layout.box()
            row = box.row() 
            row.label(text="Collection Cleaner",icon="SEQ_STRIP_META")
            row = box.row()
            row.operator("object.turn_anim_bone_collections", text= "Turn ANIM layer on", icon="ANIM") 
            row = box.row()
            row.operator("object.turn_on_all_bone_collections", text= "Turn ALL Layer on", icon="ARMATURE_DATA")
            row = box.row()
            row.operator("object.turn_solo_bone_collection", text="Solo Root", icon= "SOLO_ON").collection_name = "Root"
            row.operator("object.turn_solo_bone_collection", text="Solo DEF", icon= "SOLO_ON").collection_name = "Deform Bones"
            row.operator("object.turn_solo_bone_collection", text="Solo MCH", icon= "SOLO_ON").collection_name = "Mechanism Bones"  
            row = box.row()
            props = context.scene.bc_settings
            row.prop(props, "cl_name")
            row.operator("object.turn_solo_bone_collection",text="", icon= bpy.context.scene.Custom_prop.solo_icon).collection_name = props.cl_name
            row.operator("object.hide_bone_collection",text="", icon= bpy.context.scene.Custom_prop.hide_unhide_icon).collection_name = props.cl_name
             
            row = box.row()
            # row.operator("object.hide_bone_collection", text="", icon=bpy.context.scene.Custom_prop.hide_unhide_icon) = props.cl_name

            # Moving control right collections 
            # box = layout.box()
            # row = box.row() 
            # row.label(text= "Control Cleaner",icon="POSE_HLT")
            # row.operator("object.cleanup_ops", text= "Clean Layer",icon="BRUSH_DATA" )

            


class VIEW3D_PT_Animation(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Animation"
    bl_idname="VIEW3D_PT_Animation"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tool for Animation process")

class VIEW3D_PT_Model(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Model"
    bl_idname="VIEW3D_PT_Model"
    bl_options = {"DEFAULT_CLOSED"}
    
    
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tools for Model process & checking tools for Rigger")

classes = (
    VIEW3D_PT_MainMenu,
    VIEW3D_PT_Info,
    RiggingTabProperties,
    
)


def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)


    #Parent Panel
    bpy.utils.register_class(VIEW3D_PT_Rigging)
    bpy.utils.register_class(VIEW3D_PT_Model)
    bpy.utils.register_class(VIEW3D_PT_Animation)
 
    #Sub Panel
    
    
    #Properties
    bpy.types.Scene.Rigging_tabs = bpy.props.PointerProperty(type=RiggingTabProperties)


def unregister():
    from bpy.utils import unregister_class
    
    for cls in classes:
        unregister_class(cls)

    #Parent Panel
    bpy.utils.unregister_class(VIEW3D_PT_Rigging)
    bpy.utils.unregister_class(VIEW3D_PT_Model)
    bpy.utils.unregister_class(VIEW3D_PT_Animation)

    #Sub Panel
    

    #Properties
    del bpy.types.Scene.Rigging_tabs
    
