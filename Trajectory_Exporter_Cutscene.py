import bpy

def setup_cam_focus():
   
    obj = bpy.data.objects.get("CutsceneCamera")
        
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.constraint_add(type='TRACK_TO')
        
    bpy.context.object.constraints["Track To"].target = bpy.data.objects["cutscene_focus"]
    
    

def transforme_spline_offset(spline):
    spline *= 2.86
    spline = round(spline)
    return spline

    


def transforme_all_trajectory_for_sm64(posx, posy, posz):
                    pos_inter = posy
                    posx = posx*100
                    posy = posz*100
                    posz = pos_inter * -100
                    
                    posx = round(posx)
                    posx = str(posx)
                    posx = list(posx)
                    posx = "".join(posx)
                    
                    posy = round(posy)
                    posy = str(posy)
                    posy = list(posy)
                    posy = "".join(posy)
                        
                    posz = round(posz)
                    posz = str(posz)
                    posz = list(posz)
                    posz = "".join(posz)
                    return posx, posy, posz
    


def add_focus_point():
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        
        obj = bpy.context.selected_objects[0]
        
        obj.name = "cutscene_focus"
        
        bpy.ops.object.select_all(action='DESELECT')


def add_cutscene_camera():
        camera_data = bpy.data.cameras.new(name='CutsceneCamera')
        
        camera_object = bpy.data.objects.new('CutsceneCamera', camera_data)
        
        bpy.context.scene.collection.objects.link(camera_object)
        
        bpy.data.objects['CutsceneCamera'].select_set(True)
        
        bpy.ops.transform.translate(value=(0, 0, 4.92654))
        
        setup_cam_focus()




class CutsceneTrajectoryPanel(bpy.types.Panel):
    bl_idname = "CutsceneTrajectoryPanel"
    bl_label = "Cutscene Trajectory Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Indigo Tools"
    
    def draw(self, context): 
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        infoBox = col.box()
        infoBox.label(text="How this works?")
        infoBox.label(text="cutscene trajectory setup")
        infoBox.label(text="make a animation with location")
        infoBox.label(text="and click on the cutscene trajectory exporter button")
    
        row = layout.row()
        row.operator("wm.cutscene_trajectory_setup", text="Cutscene Trajectory Setup")
    
        row = layout.row()
        row.prop(context.scene, "use_single_point")

        row = layout.row()
        row.prop(context.scene, "indigo_mod_cutscene")
    
        row = layout.row()
        row.operator("wm.cutscene_trajectory_export", text="Cutscene Trajectory Exporter")


class CutsceneTrajectorySetup(bpy.types.Operator):
    bl_idname = "wm.cutscene_trajectory_setup"
    bl_label = "Cutscene Trajectory Setup"

    def execute(self, context):
 
        bpy.ops.object.select_all(action='DESELECT')
        
        cam_obj = bpy.data.objects.get("CutsceneCamera") 
        focus_obj = bpy.data.objects.get("cutscene_focus")
        if cam_obj and focus_obj :
            self.report({'ERROR'}, 'the object "CutscenCamera" and "cutscene_focus" already exists !')
            return {'CANCELLED'}
        elif cam_obj and not focus_obj :
            add_focus_point()
            setup_cam_focus()
        elif not cam_obj and focus_obj :
            add_cutscene_camera()
        else:
            add_focus_point()
            
            add_cutscene_camera()

     

        
        # Donne un nom à l'objet
       
        self.report({'INFO'}, "Spawned!")
        return{'FINISHED'}
    

class CutsceneTrajectoryExport(bpy.types.Operator):
    bl_idname = "wm.cutscene_trajectory_export"
    bl_label = "Cutscene Trajectory Exporter"

    def execute(self, context):
        use_single_point = context.scene.use_single_point
        indigo_mod = context.scene.indigo_mod_cutscene
        
        if context.mode != "OBJECT":
            self.report({'ERROR'}, "You must be in object mode!")
            return {'CANCELLED'}
        elif(use_single_point == True):
            
                camName = "CutsceneCamera"
                focusName = "cutscene_focus" 
                obj = bpy.data.objects.get(camName)
                if obj:
                    x, y, z = obj.location
                    x, y, z = transforme_all_trajectory_for_sm64(x, y, z)
                    self.report({'INFO'}, "{" + str(x) + ", " + str(y) + ", " + str(z) + "} //cam")
    
                obj = bpy.data.objects.get(focusName)
                if obj:
                    x, y, z = obj.location
                    x, y, z = transforme_all_trajectory_for_sm64(x, y, z)
                    self.report({'INFO'}, "{" + str(x) + ", " + str(y) + ", " + str(z) + "} //focus")
                    
                return{'FINISHED'}
                    
        
        else :
            
           
            # Get the camera object named "CutsceneCamera"
            cam_obj = bpy.data.objects.get("CutsceneCamera")
            if not cam_obj:
                self.report({'ERROR'}, 'No camera named "CutsceneCamera" found!')
                return {'CANCELLED'}

            # Retrieve f-curves of camera object
            location_fcurves = cam_obj.animation_data.action.fcurves[:3]
            rotation_fcurves = cam_obj.animation_data.action.fcurves[3:]

            # Get number of keyframes
            num_keyframes = len(location_fcurves[0].keyframe_points)

            output_string = ["//cam:\n"]

            
           
            
            if indigo_mod == True:
                for i in range(num_keyframes):
                    if i < num_keyframes - 1:
                        # Compute number of frames between keyframes
                        num_frames = location_fcurves[0].keyframe_points[i+1].co[0] - location_fcurves[0].keyframe_points[i].co[0]

                        # Compute camera position at keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                     

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])
            
                        # Add information to output string
                        string_line = "{" + str(i) + "," + str(round(num_frames)) + ", " + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + " },\n" 
                        output_string.append(string_line)
                                    
                    else:
                        # Compute camera position at last keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        # Add information to output string
                        
                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])
                        
                        string_line = "{-1,0, " + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + " }" 
                        output_string.append(string_line)  
                        output_string = "".join(output_string)              

            else:
                for i in range(num_keyframes):
                    if i < num_keyframes - 1:
                        # Compute number of frames between keyframes
                        num_frames = location_fcurves[0].keyframe_points[i+1].co[0] - location_fcurves[0].keyframe_points[i].co[0]

                        # Compute camera position at keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        num_frames = transforme_spline_offset(num_frames)

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])
            
                        # Add information to output string
                        string_line = "{" + str(i) + "," + str(round(num_frames)) + ",{ " + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + "} },\n" 
                        output_string.append(string_line)
                                    
                    else:
                        # Compute camera position at last keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        # Add information to output string
                        
                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])
                        
                        string_line = "{-1,0,{ " + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + "} }" 
                        output_string.append(string_line)  
                        output_string = "".join(output_string)              

            # Print output string for debugging
            
            
            
            
                        # Get the empty object named "cutscene_focus"
            empty_obj = bpy.data.objects.get("cutscene_focus")
            if not empty_obj:
                self.report({'ERROR'}, 'No empty object named "cutscene_focus" found!')
                return {'CANCELLED'}

            # Retrieve f-curves of empty object
            location_fcurves = empty_obj.animation_data.action.fcurves[:3]
            rotation_fcurves = empty_obj.animation_data.action.fcurves[3:]

            # Get number of keyframes
            num_keyframes = len(location_fcurves[0].keyframe_points)

            output_focus_string = ["//focus:\n"]

            if indigo_mod == True:
                for i in range(num_keyframes):
                    if i < num_keyframes - 1:
                        # Compute number of frames between keyframes
                        num_frames = location_fcurves[0].keyframe_points[i+1].co[0] - location_fcurves[0].keyframe_points[i].co[0]

                        # Compute empty object position at keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])

                        
                        # Add information to output string
                        string_line = "{" + str(i) + "," + str(round(num_frames)) + "," + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + "} ,\n" 
                        output_focus_string.append(string_line)
                        
                        
                    else:
                        # Compute empty object position at last keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])

                        # Add information to output string
                        string_line = "{-1,0, " + sm64_pos_x  + "," + sm64_pos_y + "," + sm64_pos_z + " }\n" 
                        output_focus_string.append(string_line)
                        output_focus_string = "".join(output_focus_string)   

            else:
                for i in range(num_keyframes):
                    if i < num_keyframes - 1:
                        # Compute number of frames between keyframes
                        num_frames = location_fcurves[0].keyframe_points[i+1].co[0] - location_fcurves[0].keyframe_points[i].co[0]

                        # Compute empty object position at keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])

                        num_frames = transforme_spline_offset(num_frames)
                        
                        # Add information to output string
                        string_line = "{" + str(i) + "," + str(round(num_frames)) + ",{ " + sm64_pos_x + "," + sm64_pos_y + "," + sm64_pos_z + "} },\n" 
                        output_focus_string.append(string_line)
                        
                        
                    else:
                        # Compute empty object position at last keyframe
                        position = [location_fcurves[j].keyframe_points[i].co[1] for j in range(3)]

                        sm64_pos_x, sm64_pos_y, sm64_pos_z = transforme_all_trajectory_for_sm64(position[0], position[1], position[2])

                        # Add information to output string
                        string_line = "{-1,0,{ " + sm64_pos_x  + "," + sm64_pos_y + "," + sm64_pos_z + "} }\n" 
                        output_focus_string.append(string_line)
                        output_focus_string = "".join(output_focus_string)   
                    
            # Print output string for debugging
            print(output_focus_string)
            self.report({'INFO'}, output_focus_string)
            

            
            
            
            
            
            
            
            print(output_string)
            self.report({'INFO'}, output_string)
            return {'FINISHED'}
        
        

def init_props():
    bpy.types.Scene.use_single_point = bpy.props.BoolProperty(
        name="Single Point",
        description="Use camera's current position and focus",
        default=False,
    )
    bpy.types.Scene.indigo_mod_cutscene = bpy.props.BoolProperty(
        name="Indigo Mod",
        description="Export cutscene trajecory in a table",
        default=False,
    )




def cutscene_trajectory_register():
    init_props()
    bpy.utils.register_class(CutsceneTrajectoryPanel)
    bpy.utils.register_class(CutsceneTrajectorySetup)
    bpy.utils.register_class(CutsceneTrajectoryExport)

def cutscene_trajectory_unregister():
    bpy.utils.unregister_class(CutsceneTrajectoryPanel)
    bpy.utils.unregister_class(CutsceneTrajectorySetup)
    bpy.utils.unregister_class(CutsceneTrajectoryExport)
    

    

