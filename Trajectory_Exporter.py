import bpy

# Définition d'un panneau
class TrajectoryPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_trajectory_panel"
    bl_label = "Trajectory Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Indigo Tools"

    def draw(self, context): 
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        infoBox = col.box()
        infoBox.label(text="How this works?")
        infoBox.label(text="click on the spawn button")
        infoBox.label(text="ctrc ctrv the object")
        infoBox.label(text="export the trajectory with the exporter button") 
        infoBox.label(text="clear all with the clear button")
        
        row = layout.row()
        row.operator("wm.trajectory_spawn", text="Trajectory point spawn")
        
        row = layout.row()
        row.prop(context.scene, "indigo_mod")
        
        row = layout.row()
        row.operator("wm.trajectory_export", text="Trajectory exporter")
        
        row = layout.row()
        row.operator("wm.trajectory_clear", text="Trajectory clear")
        


class TrajectorySpawn(bpy.types.Operator):
    bl_idname = "wm.trajectory_spawn"
    bl_label = "trajectory point Spawn"

    def execute(self, context):
        # Ajoute un objet vide de type "Plain Axes"
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        
        # Sélectionne l'objet nouvellement créé
        obj = bpy.context.selected_objects[0]
        
        # Donne un nom à l'objet
        obj.name = "trajectory.000"
        self.report({'INFO'}, "Spawned!")
        return{'FINISHED'}
    

# Définition d'un opérateur
class TrajectoryExport(bpy.types.Operator):
    bl_idname = "wm.trajectory_export"
    bl_label = "trajectory Exporter"

    def execute(self, context):
        indigo_mod = context.scene.indigo_mod
        if context.mode != "OBJECT":
            self.report({'ERROR'}, "You must be in object mode!")
            return {'CANCELLED'}
        elif len(context.selected_objects) == 0:
            self.report({'ERROR'}, "You must have an object in the scene!")
            return {'CANCELLED'}
        elif len(context.selected_objects) != 1:
            self.report({'ERROR'}, "You must select only one object!")
            return {'CANCELLED'}
        elif context.selected_objects[0].type != "EMPTY":
            self.report({'ERROR'}, "You must select an empty object!")
            return {'CANCELLED'}
        # add condition elif regarding the object name
        elif context.selected_objects[0].name != "trajectory.000":
            self.report({'ERROR'}, "The name must be trajectory.000!")
            return{'CANCELLED'}
        else:
            trajectory_array = [] 
            number_trajectory_point = 0
            if number_trajectory_point > 99:
                trajectory_name = "trajectory." + str(number_trajectory_point)
            elif number_trajectory_point > 9:
                trajectory_name = "trajectory.0" + str(number_trajectory_point)
            else:
                trajectory_name = "trajectory.00" + str(number_trajectory_point)
            loop = 0
            if indigo_mod == True:
                trajectory_array.append(' { \n')
            while loop == 0:
                if bpy.data.objects.get(trajectory_name) is not None: 
                  #
                    
                
                    obj = bpy.data.objects.get(trajectory_name)
                    
                    posx = obj.location.x
                    posx = int(posx * 100)
                    posy = obj.location.z
                    posy = int(posy * 100)
                    posz = obj.location.y
                    posz = int(posz * -100)
                    
                    
                    posx = str(posx)
                    posx = list(posx)
                    posx = "".join(posx)
                    
                    
                    posy = str(posy)
                    posy = list(posy)
                    posy = "".join(posy)
                        
                    
                    posz = str(posz)
                    posz = list(posz)
                    posz = "".join(posz)
                    
                    
                    if indigo_mod == False:
                        trajectory_array.append('    TRAJECTORY_POS( ' + str(number_trajectory_point) + ' , /*pos*/  ' + posx + ', ' + posy + ', ' + posz + '),\n') 
                    else:
                        trajectory_array.append(' { ' + str(number_trajectory_point) + ' , /*pos*/  ' + posx + ', ' + posy + ', ' + posz + '},\n') 

                    bpy.context.active_object.select_set(False)
                    number_trajectory_point += 1
                    if number_trajectory_point > 99:
                        trajectory_name = "trajectory." + str(number_trajectory_point)
                    elif number_trajectory_point > 9:
                        trajectory_name = "trajectory.0" + str(number_trajectory_point)
                    else:
                        trajectory_name = "trajectory.00" + str(number_trajectory_point)  
                        
                else:
                    loop = 1
            
            if indigo_mod == False:    
                trajectory_array.append("    TRAJECTORY_END(), // tank Indigo SM64")
            else : 
                 trajectory_array.append("{-1, 0, 0, 0} // tank Indigo SM64")
            trajectory_array = "".join(trajectory_array)          
            self.report({"INFO"}, trajectory_array)
            self.report({"INFO"}, "Your trajectory, here!") 
            return {'FINISHED'}


class TrajectoryClear(bpy.types.Operator):
    bl_idname = "wm.trajectory_clear"
    bl_label = "trajectory Clear"

    def execute(self, context):
        
        number_trajectory_point = 0
        
        #clear all trajectory objects
        #loop that checks if there is the name of trajectory object
        loop = 0
        while loop == 0:
            if number_trajectory_point > 99:
                trajectory_name = "trajectory." + str(number_trajectory_point)
            elif number_trajectory_point > 9:
                trajectory_name = "trajectory.0" + str(number_trajectory_point)
            else:
                trajectory_name = "trajectory.00" + str(number_trajectory_point)
            
            if bpy.data.objects.get(trajectory_name) is not None: 
                loop = 1
            else :
                number_trajectory_point += 1
            
            if number_trajectory_point > 999:
                self.report({"ERROR"}, "You have no trajectory object in the scene")
                loop = 1
                return {'CANCELLED'}
        
        loop = 0
        number_trajectory_point = 0
        while loop == 0:
            if number_trajectory_point > 99:
                trajectory_name = "trajectory." + str(number_trajectory_point)
            elif number_trajectory_point > 9:
                trajectory_name = "trajectory.0" + str(number_trajectory_point)
            else:
                trajectory_name = "trajectory.00" + str(number_trajectory_point)
                
            if bpy.data.objects.get(trajectory_name) is not None: 
                clear_obj = bpy.data.objects.get(trajectory_name)
                if clear_obj is not None:
                    bpy.data.objects.remove(clear_obj)
                number_trajectory_point += 1
            elif number_trajectory_point < 1000:
                number_trajectory_point += 1
            else:
                loop = 1
                
                
                
        self.report({"INFO"}, "Clearing all trajectory objects") 
        return {'FINISHED'}
        
        
def init_props():
    bpy.types.Scene.indigo_mod = bpy.props.BoolProperty(
        name="Indigo Mod",
        description="Export trajecory in a table",
        default=False,
    )        


# Enregistrement de l'addon
def trajectory_register():
    init_props()
    bpy.utils.register_class(TrajectoryPanel)
    bpy.utils.register_class(TrajectorySpawn)
    bpy.utils.register_class(TrajectoryExport)
    bpy.utils.register_class(TrajectoryClear)
    

def trajectory_unregister():
    bpy.utils.unregister_class(TrajectoryPanel)
    bpy.utils.unregister_class(TrajectorySpawn)
    bpy.utils.unregister_class(TrajectoryExport)
    bpy.utils.unregister_class(TrajectoryClear)


