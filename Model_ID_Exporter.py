import bpy

import os

def geo_layout_to_model_id(input_str):
    input_str = input_str.replace("_geo", "")
    output_str = "MODEL_"

    for char in input_str:
        output_str += char.upper()

    return output_str

    


def export_id_in_model_ids(self, decomp_path_value, geo_layout_name, geo_constant_id_name):
    id_number_name = str(bpy.context.scene.id_model_input) 
    model_id_array = []
    #define MODEL_TRAJECTORY_MARKER_BALL      0xE1        // bowling_ball_track_geo - duplicate used in SSL Pyramid small sized and as a track ball

    model_id_array.append('#define ' + geo_constant_id_name +  '          ' + id_number_name + '          //' + geo_layout_name + "\n")

    model_id_array = "".join(model_id_array) 
    model_id_path = os.path.join(decomp_path_value, "include/model_ids.h")

    try:
            # Lire le contenu original du fichier
        with open(model_id_path, 'r') as file:
            content = file.read()

            
                # Vérifier si model_id_array a déjà été écrit dans le fichier
        if model_id_array in content:
            return
        

        start_index = content.find('#define ' + geo_constant_id_name +  '          ')
        end_index = content.find("_geo", start_index) + 4 if start_index != -1 else -1            # Trouver l'endroit où insérer le contenu

        if start_index != -1 and end_index != -1:
            content = content[:start_index] + model_id_array + content[end_index:]
            return

        insertion_index = content.find('#endif')

        if insertion_index == -1:
            self.report({"ERROR"}, "Le '#endif' n'a pas été trouvé dans le fichier.")
            return {'CANCELLED'}

            # Insérer le behavior_array avant le '#endif'
        content = content[:insertion_index] + model_id_array + content[insertion_index:]

            # Réécrire le fichier avec le nouveau contenu
        with open(model_id_path, 'w') as file:
            file.write(content)



    except Exception as e:
        self.report({"ERROR"}, f"Erreur lors de la modification du fichier: {e}")

class ModelIDPanel(bpy.types.Panel):
    """Crée un panneau dans l'onglet Propriétés de l'objet"""

    bl_idname = "ModelIDExporterPanel"
    bl_label = "Model ID Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Indigo Tools"
    
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        infoBox = col.box()
        infoBox.label(text="model id export")
        row.prop(context.scene, 'id_model_input', text=context.scene.geoStructName)
        row = layout.row()
        layout.label(text="add level", icon='WORLD_DATA')
        row.operator("wm.plus_operator", text="+")
        row = layout.row()

        row.operator("wm.model_id_operator", text="export id")
        row = layout.row()
        
        my_props = context.scene.my_addon_props
        
        layout.prop(my_props, "my_enum_prop", text="Liste déroulante")

        
class PlusOperator(bpy.types.Operator):
    bl_idname = "wm.plus_operator"
    bl_label = "+"

    def execute(self, context):
        return {'FINISHED'}

class ModelIdOperator(bpy.types.Operator):
    bl_idname = "wm.model_id_operator"
    bl_label = "export id"

    def execute(self, context):
        current_scene = context.scene
        
        geo_layout_name = context.scene.geoStructName
        geo_constant_id_name = geo_layout_to_model_id(geo_layout_name)

        decomp_path_value = current_scene.decompPath
        export_id_in_model_ids(self, decomp_path_value, geo_layout_name, geo_constant_id_name)
        self.report({'INFO'}, geo_constant_id_name )
        self.report({'INFO'}, "name of constante here" )
        return {'FINISHED'}
    


class MyAddonProperties(bpy.types.PropertyGroup):
    items_list = [
        ("OPTION1", "Option 1", "Description de l'option 1"),
        ("OPTION2", "Option 2", "Description de l'option 2"),
        ("OPTION3", "Option 3", "Description de l'option 3"),
    ]

    my_enum_prop: bpy.props.EnumProperty(
        items=items_list,
        name="Mes Options",
        description="Choisissez une option",
        default="OPTION1"
    )


       


def model_id_register():
   
    bpy.types.Scene.id_model_input = bpy.props.StringProperty(name="id_modelo")
    bpy.utils.register_class(ModelIDPanel)
    bpy.utils.register_class(ModelIdOperator)
    bpy.utils.register_class(PlusOperator)

    bpy.utils.register_class(MyAddonProperties)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyAddonProperties)


def model_id__unregister():
    del bpy.types.Scene.id_model_input  
    bpy.utils.unregister_class(ModelIDPanel)
    bpy.utils.unregister_class(ModelIdOperator)
    bpy.utils.unregister_class(PlusOperator)

    del bpy.types.Scene.my_addon_props
    bpy.utils.unregister_class(MyAddonProperties)