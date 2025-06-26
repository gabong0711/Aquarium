      
###############
##DAMPEDTRACK##
###############


class DampedChain(bpy.types.Operator):
    bl_idname = "object.damped_chain"
    bl_label = "Damped track to the selected bone chain"
    bl_description = "Add secondary to the selected bone chain "
    def execute(self, context):
        TargetName = context.scene.my_addon_props.hair.name
        DataTargetName = context.scene.my_addon_props.hair.data.name
        TargetRealName = context.scene.my_addon_props.target
        Inf = context.scene.my_addon_props.influence
        #select all linked chain

        bpy.ops.pose.select_linked()
        selected_bones = bpy.context.selected_pose_bones
        if selected_bones is not None:
            
            
            linked_bones =[]

            #contain the tail of chain
            Last_Child = []
            #Get selection list
            for bone in selected_bones:
                linked_bones.append(bone.name)
                Last_Child.append(bone.name)

            #remove the parent to get the childest
            print(linked_bones)
            for Lbone in linked_bones:
                print(Lbone)    
                if bpy.data.objects[TargetName].pose.bones[Lbone].parent and bpy.data.objects[TargetName].pose.bones[Lbone].parent.name in Last_Child:
                    Last_Child.remove(bpy.data.objects[TargetName].pose.bones[Lbone].parent.name)   

            
            
            #damped track from the end to to first
            armature = bpy.data.objects[TargetName]
            for childest in Last_Child:
                temp = childest
                bone = bpy.data.objects[TargetName].pose.bones[temp]
                length=0 
                while (bone.parent != None and  bpy.data.armatures[DataTargetName].bones[temp].use_connect == True ):
                  #remove if existant 
                  if "Damped Track" in bone.parent.constraints:
                    # Get the constraint
                    ct = bone.parent.constraints.get("Damped Track")
                    # Remove the constraint from the bone
                    bone.parent.constraints.remove(ct)
                
                  constraint = bone.parent.constraints.new('DAMPED_TRACK')
                  constraint.target = armature
                  constraint.subtarget = bone.name
                  constraint.track_axis = 'TRACK_Y'
                  
                  length +=1
                  temp2 = bpy.data.objects[TargetName].pose.bones[temp].parent.name
                  temp = temp2
                  bone = bpy.data.objects[TargetName].pose.bones[temp]
                  
                temp = childest
                bone = bpy.data.objects[TargetName].pose.bones[temp]
                i=1
                print(length)
                while (bone.parent != None and  bpy.data.armatures[DataTargetName].bones[temp].use_connect == True ): 
                  cons = bone.parent.constraints["Damped Track"]
                  
                  driver = cons.driver_add("influence")
                  driver.driver.type = 'SCRIPTED'
                  #driver.driver.expression = sin(1)

                  Ratio_Chain = Inf*pow(sin((length-i)*pi/(2*length)),2)

                  var= driver.driver.variables.new()
                  var.name = 'Influence'
                  var.type = 'SINGLE_PROP'
                  var.targets[0].id_type ='OBJECT'

                  var.targets[0].id = TargetRealName
                  var.targets[0].data_path = 'pose.bones["Properties_Character_Sintel"]["Hair_Sim"]'
                  
                  driver.driver.expression = f'{var.name}*{Ratio_Chain}'
                  
                  i+=1
                  temp2 = bpy.data.objects[TargetName].pose.bones[temp].parent.name
                  temp = temp2
                  bone = bpy.data.objects[TargetName].pose.bones[temp]  
                  #cons.influence = Inf*pow(sin((length-i)*pi/(2*length)),2)  
                length=0       
            
        
        
        
        
        self.report({'INFO'}, "Add secondary to selected " + TargetName)
        return {'FINISHED'}  

#############
##Hair tool##
#############


                
def separateEdge(obj,col,old_collection):
    
   
    obj2_name= 'meshcage_' + obj.name
    obj2_Temp=obj.name +'.001'   
    # Check if the object exists and is a mesh
    if obj and obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode

        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all vertices/edges/faces

        bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode

        # Switch back to Edit Mode to see the selected edges
        #bpy.ops.object.mode_set(mode='EDIT')

        # Iterate through the edges and select all sharp edges
        for edge in obj.data.edges:
            if edge.use_edge_sharp:
                edge.select = True

        # Switch back to Edit Mode to see the selected edges
        bpy.ops.object.mode_set(mode='EDIT')



    if bpy.context.mode == 'EDIT_MESH':
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Please select an edge in Edit Mode before running the script.")
    
    obj2 = bpy.data.objects.get(obj2_Temp)
    obj2.name=obj2_name
    
    # Get the object by name
  

    if obj2:
    # Get the target collection
        target_collection = bpy.data.collections.get(col.name)

        if target_collection:
            # Move the object to the target collection
           
            target_collection.objects.link(obj2)
            old_collection.objects.unlink(obj2)

            print(f"Object '{obj2.name}' moved to collection '{col}'.")
        else:
            print(f"Target collection '{col}' not found.")
    else:
        print(f"Object '{obj2.name}' not found.")


class SeperateEdge(bpy.types.Operator):
    bl_idname = "object.seperateedge"
    bl_label = "Seperate Sharp edge into new object"
    bl_description = "Seperate Sharp edge into new object"
    def execute(self, context):
        collections_to_print = [collection for collection in bpy.data.collections if collection.name.endswith('.hair')]
        collection_name = 'meshcage_hair'
        existing_collection = bpy.data.collections.get(collection_name)
        if not existing_collection:
            new_collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(new_collection)
        
        col=bpy.data.collections.get(collection_name)
        
       
        for collection in collections_to_print:
            #print(f"Objects in collection '{collection.name}':")
    
            # Iterate through objects in the collection and print their names
            for obj in collection.objects:
                separateEdge(obj,col,collection)
            #print(f"  - {obj.name}")
        
        
        self.report({'INFO'}, "Create new collection")
        return {'FINISHED'}  

class CleanMeshcage(bpy.types.Operator):
    bl_idname = "object.cleanmeshcage"
    bl_label = "Meshcage into wire in viewport & hiden render"
    bl_description = "Meshcage into wire in viewport & hiden render, unlink shader, unlink sub"
    def execute(self, context):     
      
        collection_name = 'meshcage_hair'
        collection = bpy.data.collections.get(collection_name)

        for obj in collection.objects:
            if (obj.type == 'MESH'):
                bpy.data.objects[obj.name].display_type = 'WIRE'
            
            for modifier in obj.modifiers:
                if (modifier.type == 'SUBSURF'):
                    obj.modifiers.remove(modifier)
            obj.data.materials.clear()
           
            
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        
        self.report({'INFO'}, "Replace")
        return {'FINISHED'}

class reduceVertice(bpy.types.Operator):
    bl_idname = "object.reducevertice"
    bl_label = "reduce number of bones"
    bl_description = "reduce number of bones"
    def execute(self, context):
        bpy.ops.object.reduceverticebymergedistance()  
        bpy.ops.object.reduceverticebylimiteddissolve()  
        
        self.report({'INFO'}, "Reduce")
        return {'FINISHED'}

#mergedistance

class reduceVerticebyMD(bpy.types.Operator):
    bl_idname = "object.reduceverticebymergedistance"
    bl_label = "reduce number of bones"
    bl_description = "reduce number of bones"
    def execute(self, context):
        distance_threshhold = context.scene.my_addon_props.distance_threshhold
       
        collection_name = 'meshcage_hair'
        collection = bpy.data.collections.get(collection_name)

        for obj in collection.objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
            bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all vertices/edges/faces
            bpy.ops.mesh.select_all(action='SELECT')

            
            bpy.ops.mesh.remove_doubles(threshold=distance_threshhold)
            
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, "Reduce")
        return {'FINISHED'}

class reduceVerticebyLD(bpy.types.Operator):
    bl_idname = "object.reduceverticebylimiteddissolve"
    
    bl_label = "reduce number of bones"
    bl_description = "reduce number of bones"
    def execute(self, context):
        
        angle_dissolve= context.scene.my_addon_props.angle_dissolve
        collection_name = 'meshcage_hair'
        collection = bpy.data.collections.get(collection_name)

        for obj in collection.objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
            bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all vertices/edges/faces
            bpy.ops.mesh.select_all(action='SELECT')

            bpy.ops.mesh.dissolve_limited(angle_limit=angle_dissolve)
            
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        
        self.report({'INFO'}, "Reduce")
        return {'FINISHED'}

class addArmature(bpy.types.Operator):
    bl_idname = "object.addarmature"
    bl_label = "generate bone"
    bl_description = "Add skin modifier and generate"
    def execute(self, context):
        
        
        collection_name = 'meshcage_hair'
        collection = bpy.data.collections.get(collection_name)

        for obj in collection.objects:
           bpy.context.view_layer.objects.active = obj
           bpy.ops.object.modifier_add(type='SKIN')

        self.report({'INFO'}, "Added skin modifier")
        return {'FINISHED'}  

#create bone
def renameBoneinside(armature_name,obj_name):
    armature_obj= bpy.data.objects.get(armature_name)
    search_string ='Bone'
    replacement_string = obj_name.replace('meshcage_','Bone_')
    #replacement_string = 'thing'
    #replace string = 'Anh_hair'
    if armature_obj and armature_obj.type == 'ARMATURE':
        armature = armature_obj.data
        for bone in armature.bones:
            bone.name = bone.name.replace(search_string, replacement_string)
            bone.name = bone.name.replace('.','_')


def ReassignArmature(collection_name,armature_name):
    
    collection = bpy.data.collections.get(collection_name)
    armature = bpy.data.objects.get(armature_name)
    for obj in collection.objects:
        if (obj.type=='MESH'):
            for modifier in obj.modifiers: 
                if (modifier.type =='ARMATURE'):
                     obj.modifiers.remove(modifier)
    
            armature_modifier = obj.modifiers.new(name="Hair_rig", type='ARMATURE')
            armature_modifier.object = armature          
  
           
               
class GenArmature(bpy.types.Operator):
    bl_idname = "object.genarmature"
    bl_label = "generate bone"
    bl_description = "Add skin modifier and generate"
    def execute(self, context):
        
        
        collection_name = 'meshcage_hair'
        collection = bpy.data.collections.get(collection_name)
        
        #gen 2nd, delete old armature
        for obj in collection.objects:
            if (obj.type== 'ARMATURE'): 
                bpy.data.objects.remove(obj, do_unlink=True)
        
        #create bone chains
        for obj in collection.objects:
           for modifier in obj.modifiers: 
               if (modifier.type=='SKIN'):
                    #print(f"Object: {obj.name}, Skin Modifier: {modifier.name}")
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.skin_armature_create(modifier="Skin")
                    armature = bpy.context.view_layer.objects.active
                    armature.name= obj.name+'_arm_temp'
                    renameBoneinside(armature.name,obj.name)
        
        # Select all bone chains
        First= False
        for obj in collection.objects:
            if (obj.type== 'ARMATURE' and First == False):
                First = True
                armature=obj
                armature.select_set(True)
                armature.name =  armature.name.replace('meshcage_','RIG-ch.cc_')
                armature.name =  armature.name.replace('.hair_01_arm_temp','_hair')
            elif (obj.type== 'ARMATURE'):
                    
                    obj.select_set(True)

                    # Set the context to the active object (armature_A)
                    

                    # Join the armatures

        #Join bone chains into an armature
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.join()               

        ReassignArmature(collection_name,armature.name)

        self.report({'INFO'}, "Created Armature")
        return {'FINISHED'}  


class addMeshDeform(bpy.types.Operator):
    bl_idname = "object.addmeshdeform"
    bl_label = "Add Mesh Deform"
    bl_description = "Add mesh deform into hair mesh"
    def execute(self, context):
        collections_to_modify= [collection for collection in bpy.data.collections if collection.name.endswith('.hair')]
        for collection in collections_to_modify:    
            for obj in collection.objects:
                for modifier in obj.modifiers: 
                    #reorder the sub priority to bottom, then clean all the old meshdeform
                    
                    if (modifier.type =='SUBSURF'):
                        obj.modifiers.remove(modifier)
                    elif (modifier.type =='MESH_DEFORM'):
                        obj.modifiers.remove(modifier)
                
                obj_name=obj.name
                meshcage_name= 'meshcage_' + obj_name
                meshcage =  bpy.data.objects.get(meshcage_name)

                #Add bind for sub 0
                obj_modifier = obj.modifiers.new(name="Hair_bind_0", type='MESH_DEFORM') 
                obj_modifier.object = meshcage
                obj_modifier.precision = 4

                #Add bind for sub 1
                obj_modifier = obj.modifiers.new(name="Hair_bind_1", type='MESH_DEFORM') 
                obj_modifier.object = meshcage
                obj_modifier.precision = 4

                #Add bind for sub 2
                obj_modifier = obj.modifiers.new(name="Hair_bind_2", type='MESH_DEFORM') 
                obj_modifier.object = meshcage
                obj_modifier.precision = 4
                #de sub xuong cuoi cung
                sub =  obj.modifiers.new(name="Subdivision", type='SUBSURF') 
        
        
        self.report({'INFO'}, "Added Mesh Deform")
        return {'FINISHED'}  


#class Bind & unbind
class hairBind(bpy.types.Operator):
    bl_idname = "object.hairbind"
    bl_label = "hair bind"
    bl_description = "bind or unbind hair"
    def execute(self, context):
        collections_to_modify= [collection for collection in bpy.data.collections if collection.name.endswith('.hair')]
        sub_needtobind= bpy.context.scene.my_addon_props.BindSub
        for collection in collections_to_modify:    
            for obj in collection.objects:
                for modifier in obj.modifiers: 
                    if (modifier.type =='MESH_DEFORM' and sub_needtobind == 0 and modifier.name =='Hair_bind_0'):
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.meshdeform_bind(modifier=modifier.name)
                    elif (modifier.type =='MESH_DEFORM' and sub_needtobind == 1 and modifier.name =='Hair_bind_1'):
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.meshdeform_bind(modifier=modifier.name)
                        
                    elif (modifier.type =='MESH_DEFORM' and sub_needtobind == 2 and modifier.name =='Hair_bind_2'):
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.meshdeform_bind(modifier=modifier.name)

        self.report({'INFO'}, "Binded")
        return {'FINISHED'}  




#extrude frome its parent

def ConnectParent(BoneA, BoneB):
    # BoneA: Child
    # BoneB: Parent
    Hairrig_arm = bpy.context.scene.my_addon_props.hair.data
    Hairrig_arm.edit_bones[BoneA].parent = Hairrig_arm.edit_bones[BoneB]
    Hairrig_arm.edit_bones[BoneA].use_connect = True
def Del_bone(bone_name):
    Hairrig_arm = bpy.context.scene.my_addon_props.hair.data
    Hairrig_arm.edit_bones.remove(Hairrig_arm.edit_bones[bone_name])

class createconstructChain(bpy.types.Operator):
    bl_idname = "object.createconstructchain"
    bl_label = "Reconstruct the malfunction chain"
    bl_description = "Replace the malfunction chain" 
    def execute(self, context):
        Hairrig_name = context.scene.my_addon_props.hair.name
        Hairrig = bpy.data.objects[Hairrig_name]
        Hairrig_arm = Hairrig.data
       
       
        #select all linked chain
        bpy.ops.pose.select_linked()

        selected_bones = bpy.context.selected_pose_bones
        #Create all bones without duplicate
        if selected_bones is not None:
            #contain all name
            linked_bones =[]
            #contain the tail of chain
            # Parent = []

            #last bone
            Last_Child = []
            #contain all bone that construct 

            
            
            #Get selection list
            for bone in selected_bones:
                linked_bones.append(bone.name)
                # Parent.append(bone.name)
                Last_Child.append(bone.name)
            
            
            #Duplicate
            for Lbone in linked_bones:
                  
                if Hairrig.pose.bones[Lbone].parent and Hairrig.pose.bones[Lbone].parent.name in Last_Child:
                    Last_Child.remove(Hairrig.pose.bones[Lbone].parent.name)   
                #print(f'{Lbone}')
                    
                #reset xyz  
           
           
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.ops.object.mode_set(mode='EDIT')
            ConsList =[]
            #create the lastone
            for childest in Last_Child:
                
                #Temp - name of bone
                temp = childest
                #Temp bone
                bone = Hairrig.pose.bones[temp]
                
                length=0 
                First= True
                while (bone.parent != None and  Hairrig_arm.bones[temp].use_connect == True ):
                  #remove if existant 
                    bpy.ops.object.mode_set(mode='OBJECT') 
                    bpy.ops.object.mode_set(mode='EDIT')
                    namecons = bone.name.replace('Bone','Construct')
                    #set xyz and roll. 

                    bone1 = Hairrig_arm.edit_bones.new(namecons)
                    ConsList.append(namecons)
                    bone1.tail = Hairrig_arm.edit_bones[bone.name].tail
                    bone1.head = Hairrig_arm.edit_bones[bone.name].head
                    bone1.roll =  Hairrig_arm.edit_bones[bone.name].roll

                    #the first - no mark parent  
                    if (First):
                        First = False
                        
                    else: 
                        #mark parent
                        #at i. PrL[child] = parent
                        ConnectParent(bonetemp,bone1.name)
                        
                    
                    bonetemp = bone1.name

                    #go to parent
                    
                   
                    bone = Hairrig.pose.bones[temp].parent
                    temp = Hairrig.pose.bones[temp].parent.name
                    length+=1
                    #print(f'length is : {length}')
                
                bpy.ops.object.mode_set(mode='OBJECT') 
                bpy.ops.object.mode_set(mode='EDIT')
                
                #Parent bone
                namecons = bone.name.replace('Bone','Construct')
                bone1 = Hairrig_arm.edit_bones.new(namecons)
                ConsList.append(bone1.name)
                
                if (Hairrig_arm.edit_bones[bone.name].parent):
                    bone1.parent = Hairrig_arm.edit_bones[Hairrig_arm.edit_bones[bone.name].parent.name]
                
                bone1.tail = Hairrig_arm.edit_bones[bone.name].tail
                bone1.head = Hairrig_arm.edit_bones[bone.name].head
                bone1.roll =  Hairrig_arm.edit_bones[bone.name].roll
                ConnectParent(bonetemp,bone1.name)

            
            #bpy.ops.object.mode_set(mode='OBJECT') 
            #Del old chain
            print(f'mark')
            for i in linked_bones:
                Del_bone(i)
                print(f'{i}')
           
            # #Rename
            
            # for i in ConsList:
            #     bone = Hairrig_arm.edit_bones[i]    
            #     bone.name = bone.name.replace('Construct','Bone')
            #     #print(f'{i}')
                

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "Created")
        return {'FINISHED'}  

class renameBone(bpy.types.Operator):
    bl_idname = "object.renamebone"
    bl_label = "rename construct bone"
    bl_description = "Rename all construct bone into normal bone"
    def execute(self, context):
        Hairrig_name = context.scene.my_addon_props.hair.name
        Hairrig = bpy.data.objects[Hairrig_name]
        Hairrig_arm = Hairrig.data
        bpy.ops.object.mode_set(mode='OBJECT') 
        bpy.ops.object.mode_set(mode='EDIT')
        for bone in Hairrig_arm.edit_bones:
            if 'Construct' in bone.name:
                new_name = bone.name.replace('Construct','Bone')
                bone.name = new_name
        bpy.ops.object.mode_set(mode='POSE')
        
        self.report({'INFO'}, "Rename " +  Hairrig_name)
        return {'FINISHED'}  

#rename "construct"-> "real bone"
    