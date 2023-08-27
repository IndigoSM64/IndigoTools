import bpy
import os


def transform_string(input_str):
    output_str = ""

    for char in input_str:
        if char.isupper():
            output_str += '_' + char.lower()
        else:
            output_str += char

    return output_str

def control_bhv(input_str):
    if input_str[0] != "b" or input_str[1] != "h" or input_str[2] != "v":
        return 1
    else: return 0


def include_file(self, behavior_script_name, decomp_path_value, init_function, name_file): 
        include_array = [] 
        extern_data_path = os.path.join(decomp_path_value, "src/game/behavior_actions.c")
        include_array.append('\n#include "behaviors/' + name_file )
        #include "behaviors/sl_walking_penguin.inc.c"

        include_array = "".join(include_array) 
        
        try:
            # Lire le contenu original du fichier
            with open(extern_data_path, 'r') as file:
                content = file.read()

            
                # Vérifier si include_array a déjà été écrit dans le fichier
            if include_array in content:
               
                return

            # Insérer le behavior_array avant le '#endif'
            content = include_array 

            # Réécrire le fichier avec le nouveau contenu
            with open(extern_data_path, 'a') as file:
                file.write(content)



        except Exception as e:
            self.report({"ERROR"}, f"Erreur lors de la modification du fichier: {e}")
    
def create_file(name_file, decomp_path_value, init_function, loop_function, bool_function_init, bool_function_loop):
    content_array = []
    content_array.append("// " + name_file +  "\n")

    if bool_function_init == True :
        content_array.append("\n void  " + init_function +  "(void){")
        content_array.append("\n \n")
        content_array.append("}\n")


    if bool_function_loop == True :
        content_array.append("\n void  " + loop_function +  "(void){")
        content_array.append("\n \n ")
        content_array.append("}\n")
        
    content_array.append("\n")
        
    content_array = "".join(content_array) 


    file_creat_path = os.path.join(decomp_path_value, "src/game/behaviors/" + name_file)
    if os.path.exists(file_creat_path):
        return
    else:
        with open(file_creat_path, 'w') as file:
            file.write(content_array)
            print(f"Le fichier {file_creat_path} a été créé.")


def behavior_data_extern(self, behavior_script_name, decomp_path_value):
        behavior_extern_array = [] 
        extern_data_path = os.path.join(decomp_path_value, "include/behavior_data.h")
        behavior_extern_array.append("extern const BehaviorScript " + behavior_script_name +  "[];\n")
        behavior_extern_array = "".join(behavior_extern_array) 
        
        try:
            # Lire le contenu original du fichier
            with open(extern_data_path, 'r') as file:
                content = file.read()

            
                # Vérifier si behavior_extern_array a déjà été écrit dans le fichier
            if behavior_extern_array in content:
                return
            # Trouver l'endroit où insérer le contenu
            insertion_index = content.find('#endif // BEHAVIOR_DATA_H')

            if insertion_index == -1:
                self.report({"ERROR"}, "Le '#endif' n'a pas été trouvé dans le fichier.")
                return {'CANCELLED'}

            # Insérer le behavior_array avant le '#endif'
            content = content[:insertion_index] + behavior_extern_array + content[insertion_index:]

            # Réécrire le fichier avec le nouveau contenu
            with open(extern_data_path, 'w') as file:
                file.write(content)



        except Exception as e:
            self.report({"ERROR"}, f"Erreur lors de la modification du fichier: {e}")


def behavior_loop_include(self, behavior_script_name, decomp_path_value, init_function, loop_function, bool_function_init, bool_function_loop):
        loop_include_array = [] 
        extern_data_path = os.path.join(decomp_path_value, "src/game/behavior_actions.h")
        if bool_function_init == True :
            loop_include_array.append("\n void  " + init_function +  "(void);")


        if bool_function_loop == True :
            loop_include_array.append("\n void  " + loop_function +  "(void);")
        loop_include_array.append("\n")
        loop_include_array = "".join(loop_include_array) 
        
        try:
            # Lire le contenu original du fichier
            with open(extern_data_path, 'r') as file:
                content = file.read()

            
                # Vérifier si loop_include_array a déjà été écrit dans le fichier
            if loop_include_array in content:
                return
            # Trouver l'endroit où insérer le contenu
            insertion_index = content.find('Gfx *geo_move_mario_part_from_parent(s32 callContext, UNUSED struct GraphNode *node, Mat4 mtx);')

            if insertion_index == -1:
                self.report({"ERROR"}, "Le '#endif' n'a pas été trouvé dans le fichier.")
                return {'CANCELLED'}

            # Insérer le behavior_array avant le '#endif'
            content = content[:insertion_index] + loop_include_array + content[insertion_index:]

            # Réécrire le fichier avec le nouveau contenu
            with open(extern_data_path, 'w') as file:
                file.write(content)



        except Exception as e:
            self.report({"ERROR"}, f"Erreur lors de la modification du fichier: {e}")



def behavior_data(self, behavior_script_name, decomp_path_value, init_function, loop_function, bool_function_init, bool_function_loop):
    data_path = os.path.join(decomp_path_value, "data/behavior_data.c")
    behavior_array = []

    behavior_array.append("\nconst BehaviorScript " + behavior_script_name + "[] = {")

    if bool_function_init:
        behavior_array.append("\n    CALL_NATIVE(" + init_function + "),")

    if bool_function_loop:
        behavior_array.append("\n    BEGIN_LOOP(),")
        behavior_array.append("\n        CALL_NATIVE(" + loop_function + "),")
        behavior_array.append("\n    END_LOOP(),")

    behavior_array.append("\n};\n")
    behavior_array = "".join(behavior_array)

    try:
        with open(data_path, 'r') as file:
            content = file.read()

        # Trouver le début et la fin du BehaviorScript existant
        start_index = content.find("const BehaviorScript " + behavior_script_name + "[] = {")
        end_index = content.find("};", start_index) + 2 if start_index != -1 else -1

        # Si le BehaviorScript existe, le supprimer
        if start_index != -1 and end_index != -1:
            content = content[:start_index] + behavior_array + content[end_index:]
            return

        # Ajouter le nouveau BehaviorScript à la fin du fichier
        content += behavior_array

        with open(data_path, 'w') as file:
            file.write(content)



    except Exception as e:
        self.report({"ERROR"}, f"Erreur lors de la modification du fichier: {e}")




class SimplePanel(bpy.types.Panel):
    """Crée un panneau dans l'onglet Propriétés de l'objet"""

    bl_idname = "BehaviorScriptPanel"
    bl_label = "Behavior Script Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Indigo Tools"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        infoBox = col.box()
        row = layout.row()
        infoBox.label(text="bhvName")
        row.prop(context.scene, 'my_text_input', text="Saisie du texte")
        row = layout.row()
     
        row.operator("wm.print_repo", text="afficher le chemin du repo")
        row = layout.row()

        row.prop(context.scene, "is_there_a_init")
        row = layout.row()

        row.prop(context.scene, "is_there_a_loop")
        row = layout.row()

        row.prop(context.scene, "is_there_a_file_inc_c")


class PrintRepo(bpy.types.Operator):
    bl_idname = "wm.print_repo"
    bl_label = "afficher le chemin du repo"

    def execute(self, context):
        bool_function_init = context.scene.is_there_a_init
        bool_function_loop = context.scene.is_there_a_loop
        bool_file = context.scene.is_there_a_file_inc_c
        
        
        current_scene = bpy.context.scene
        decomp_path_value = current_scene.decompPath

        
        # Écrire dans le fichier
        behavior_script_name = str(context.scene.my_text_input) 
        if behavior_script_name == "":
            self.report({'ERROR'}, 'no bhvScript name...')
            return {'CANCELLED'} 
        
        if control_bhv(behavior_script_name) == 1:
            if behavior_script_name == "":
                self.report({'ERROR'}, 'no bhvScript name...')
                return {'CANCELLED'} 
            self.report({'ERROR'}, 'bhv script must begin with bhv')
            return {'CANCELLED'} 
        
        name_file = init_function = transform_string(behavior_script_name.replace("bhv_", "")) + ".inc.c"
        init_function = transform_string(behavior_script_name) + "_init"
        loop_function = transform_string(behavior_script_name) + "_loop"

 
        
        
        behavior_data_extern(self, behavior_script_name, decomp_path_value)

        behavior_data(self, behavior_script_name, decomp_path_value, init_function, loop_function , bool_function_init, bool_function_loop)

        behavior_loop_include(self, behavior_script_name, decomp_path_value, init_function, loop_function , bool_function_init, bool_function_loop)
        
        if bool_file == True:

            include_file(self, behavior_script_name, decomp_path_value, init_function, name_file)
            create_file(name_file, decomp_path_value, init_function, loop_function, bool_function_init, bool_function_loop)
        self.report({'INFO'}, 'Export Sucess')
        return {'FINISHED'}
    

def init_props():
    bpy.types.Scene.is_there_a_init = bpy.props.BoolProperty(
        name="function init",
        description="export a function init",
        default=False,
    )
    bpy.types.Scene.is_there_a_loop = bpy.props.BoolProperty(
        name="function loop",
        description="export a function loop",
        default=False,
    )
    bpy.types.Scene.is_there_a_file_inc_c = bpy.props.BoolProperty(
        name="create a bhv files",
        description="create a new files with loop function",
        default=False,
    )


def behavior_script_register():
    init_props()
    bpy.types.Scene.my_text_input = bpy.props.StringProperty(name="contenu")  # Ajout de la StringProperty
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(PrintRepo)

def behavior_script_unregister():
    del bpy.types.Scene.my_text_input  # Suppression de la StringProperty lors de la désinscription
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(PrintRepo)



  

