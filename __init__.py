


bl_info = {
    "name": "Indigo Tools",
    "author": "Indigo",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > UI > Indigo Tools",
    "description": "tools for hackers SM64",
    "warning": "",
    "doc_url": "",
    "category": "SM64 Tools"
}

from .Trajectory_Exporter import trajectory_register
from .Trajectory_Exporter import trajectory_unregister
from .Trajectory_Exporter_Cutscene import cutscene_trajectory_register
from .Trajectory_Exporter_Cutscene import cutscene_trajectory_unregister
from .Behavior_Srcipt_Exporter import behavior_script_register
from .Behavior_Srcipt_Exporter import behavior_script_unregister
from .Model_ID_Exporter import model_id_register
from .Model_ID_Exporter import model_id__unregister
import bpy
from bpy.utils import register_class, unregister_class


def register():

    
    trajectory_register()
    cutscene_trajectory_register()
    behavior_script_register()
    model_id_register()
    
def unregister():


    trajectory_unregister()
    cutscene_trajectory_unregister()
    behavior_script_unregister()
    model_id__unregister()
