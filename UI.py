import bpy
from bpy.types import Menu, Panel, Context
from .Function import ops
from .Function import LayerScript
from .Function import ModelOps
class VIEW3D_PT_MainMenu(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Main Menu"
    bl_idname= "VIEW3D_PT_MainMenu"
    
    def draw(self, context):
        layout = self.layout
        #layout.label(text ="Chim tren troi")
        box = layout. box() 
        row = box.row() 
        row.operator("object.purge_operator", text="Purge", icon="ORPHAN_DATA")  


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
    bl_parent_id = "VIEW3D_PT_MainMenu"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tool for rigging process")
        
        #Tab
        props =  context.scene.Rigging_tabs
        row = layout.row()
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
            col = box.column()
            col.label(text="This is the General tab.")
            col.label(text="In this tab, using for active object, don't need to declared.")
            
            box = layout.box()
            row = box.row()
            row.operator("object.symmetry_target_contraints_side", text="Fix Constraint Target in Mirror Bone", icon="MOD_MIRROR")
            
            row = box.row(align=True)
            if not context.object : temp = ''
            else: temp = context.object.name
            row.operator("object.unlink_action", text= "Unlink Action",icon="EXPERIMENTAL").Target = temp
            row.operator("object.armature_setting", text= "Armature Viewport Display",icon="EXPERIMENTAL").Target = temp
            
        elif props.tab == 'METARIG' :
            box = layout.box()
            box.label(text="This is the METARIG tab.")
            
            box = layout.box()
            row = box.row() 
            row.operator("object.change_constraint_tg", text="ReAssign Target", icon="GROUP_BONE")
            #Parent switch list
            props = context.scene.my_addon_props
            box = layout.box()
            row = box.row()
            icon = "TRIA_DOWN" if props.show_box else "TRIA_RIGHT"
            row.prop(props, "show_box", text=" Parent Switching List", icon=icon, emboss=False)
            #row.label(text="Parent Switching List",icon="SOLO_ON")
            if props.show_box:
                row = box.row()
                for label_text, copy_text_1, copy_text_2 in [("Root", "Root", "sub-Root"),
                                                            ("P-root", "P-root", "P-root"),
                                                            ("Shoulder.L", "Shoulder.L", "FK-Shoulder.L"),
                                                            ("Shoulder.R", "Shoulder.R", "FK-Shoulder.R"),
                                                            ("Hips", "Hips", "MSTR-Spine_Hips"),
                                                            ("Torso", "Torso", "MSTR-Spine_Torso"),
                                                            ("Chest", "Chest", "DEF-Chest"),
                                                            ("Head", "Head", "FK-Head"),
                                                            ("No", "No", "no"),]:
                        #row = box.row()
                        row = box.row(align = False)
                        row.use_property_split = True
                        row.use_property_decorate = False
                        row.label(text = label_text)
                        row.operator("my.copy_to_clipboard", text="", icon="DUPLICATE",depress=False).copy_text = copy_text_1
                        row.operator("my.copy_to_clipboard", text="", icon="BONE_DATA",depress=False).copy_text = copy_text_2
            
            layout.separator()
            layout.separator()
            
        elif props.tab == 'GENERATED' :
            box = layout.box()
            box.label(text="This is the GENERATED tab.")
            box = layout.box()
            row = box.row()
            row.operator("object.driversubdivision", text= "Subdivision Driver",icon="STRIP_COLOR_06")
            
            col = box.column(align=True)
            row = col.row (align=True)
            row.operator("object.magic", text= "Magic of your life",icon="EXPERIMENTAL")
            
            row = col.row(align = True)
            row.operator("object.ifksetting_ops", text= "IK FK Common Setting")
            row.operator("object.addrollback", text= "Add Extra RollBack")
            
            row = box.row()

            #Script
            box = layout.box()
            row = box.row(align= True)
            row.label(text="Cloud UI Script.")
            row.operator("object.textbutton_operator",text="",icon = "DUPLICATE")
            row.operator("object.textbutton_operator",text="",icon = "FILE_CACHE")
            row = box.row()
            row.label(text="Edit Layer is temporary in development process." , icon = "PINNED")
            
        elif props.tab == 'CLEAN' :
            box = layout.box()
            box.label(text="This is Clean up tab",icon="BRUSH_DATA")
            
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True) 
            row.label(text="Collection Cleaner",icon="SEQ_STRIP_META")
            row = col.row(align=True)
            row.operator("object.turn_anim_bone_collections", text= "Turn ANIM layer on", icon="ANIM") 
            row = col.row(align=True)
            row.operator("object.turn_on_all_bone_collections", text= "Turn ALL Layer on", icon="ARMATURE_DATA")
            row = col.row(align=True)
            row.operator("object.turn_solo_bone_collection", text="Solo Root", icon= "SOLO_ON").collection_name = "Root"
            row.operator("object.turn_solo_bone_collection", text="Solo DEF", icon= "SOLO_ON").collection_name = "Deform Bones"
            row.operator("object.turn_solo_bone_collection", text="Solo MCH", icon= "SOLO_ON").collection_name = "Mechanism Bones" 
            
            box = layout.box()
            row = box.row(align=True)

            # Chia tỷ lệ 70% cho tên, 30% cho nút
            split = row.split(factor=0.7)
            props = context.scene.bc_settings
            # Phần tên cl_name
            split.label(text="Bone Collection:")
            
            

            # Phần còn lại: hai nút
            #row = box.row()
            row.prop(props, "cl_name",text="")
            row.operator("object.turn_solo_bone_collection", text="", icon=context.scene.Custom_prop.solo_icon).collection_name = props.cl_name
            row.operator("object.hide_bone_collection", text="", icon=context.scene.Custom_prop.hide_unhide_icon).collection_name = props.cl_name
             
         
        
        



class VIEW3D_PT_Animation(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Animation"
    bl_idname="VIEW3D_PT_Animation"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_MainMenu"
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
    bl_parent_id = "VIEW3D_PT_MainMenu"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tools for Model process & checking tools for Rigger")
        layout.label(text= "Pie Menu: Ctrl Alt + D", icon = "PINNED")

        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.operator("object.select_with_shape_keys", text= "Shapekey object",icon="RESTRICT_SELECT_OFF")
        row.operator("object.select_with_modifiers", text= "Modified object",icon="RESTRICT_SELECT_OFF")
        row = col.row(align = True)
        row.operator("object.remove_modifiers", text= "Remove all object's modifies",icon="X")
        row = col.row(align = True)
        row.operator("object.select_face_by_sides", text= "N-gon Face (Edit Mode)",icon="RESTRICT_SELECT_OFF")
        row.operator("object.select_with_n_gon", text= "N-gon Object",icon="RESTRICT_SELECT_OFF")
        
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.operator("object.select_with_pop_up", text= "Color Management",icon="RESTRICT_SELECT_OFF")
        
class VIEW3D_PT_Lighting(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aquarium"
    bl_label = "Lighting"
    bl_idname="VIEW3D_PT_Lighting"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_MainMenu"
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Include all the tool for Lighting process")    
        
          

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
        row = col.row()
        row.operator("wm.url_open", text="Download at Github").url = "https://github.com/gabong0711/Aquarium.git"



classes = (
    #VIEW3D_PT_MainMenu,
    VIEW3D_PT_Info,
    RiggingTabProperties,
    
)


def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)


    #Parent Panel
    bpy.utils.register_class(VIEW3D_PT_MainMenu)
 
    #Sub Panel
    bpy.utils.register_class(VIEW3D_PT_Rigging)
    bpy.utils.register_class(VIEW3D_PT_Model)
    bpy.utils.register_class(VIEW3D_PT_Animation)
    
    bpy.utils.register_class(VIEW3D_PT_Lighting)
    #Properties
    bpy.types.Scene.Rigging_tabs = bpy.props.PointerProperty(type=RiggingTabProperties)


def unregister():
    from bpy.utils import unregister_class
    
    for cls in classes:
        unregister_class(cls)

    #Parent Panel
    bpy.utils.unregister_class(VIEW3D_PT_MainMenu)

    #Sub Panel
    bpy.utils.unregister_class(VIEW3D_PT_Rigging)
    bpy.utils.unregister_class(VIEW3D_PT_Model)
    bpy.utils.unregister_class(VIEW3D_PT_Animation)
    bpy.utils.unregister_class(VIEW3D_PT_Lighting)
    #Properties
    del bpy.types.Scene.Rigging_tabs
    
