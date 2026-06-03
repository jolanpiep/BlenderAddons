import bpy
from bpy.props import (
    StringProperty,
    FloatVectorProperty,
    BoolProperty,
)
from . import helpers

# Disable PyLance warnings about declaring parameters in classes with the unusual Blender syntax
# pyright: reportInvalidTypeForm=false


def fracture(objects, modifier_name, translation, socket_toggle, cleanup_toggle):
    
    allFracs = []

    for object in objects:
        
        ## High-level functions, see helpers.py ##
        
        objname = object.name

        dupObj = helpers.duplicate(object)
        helpers.applyModifiers(dupObj, modifier_name)
        
        if dupObj.parent is not None:
            objname = object.parent.name
            helpers.unparent(dupObj)

        helpers.translate(dupObj, translation)

        fractures = helpers.separate(dupObj)
        
        allFracs.extend(fractures)

        for i, frac in enumerate(fractures):
            letter = helpers.numbersToLetters(i)
            helpers.rename(frac, f"{objname}_Frac_{letter}")

            if socket_toggle:
                socket = helpers.addSocket(frac)
                helpers.originToGeometry(frac)
                helpers.parent(socket, frac)

    if cleanup_toggle:
        helpers.cleanup(allFracs)


class OBJECT_OT_Fracture(bpy.types.Operator):
    bl_idname = "object.fracture"
    bl_label = "Fracture"
    bl_description = "Process Fractured Objects to Seperate Pieces"
    bl_options = {'REGISTER', 'UNDO'}

    modifier_name: StringProperty(
        name = 'Modifier Name', 
        default = 'Fracture'
    )

    translation: FloatVectorProperty(
        name = 'Translation', 
        default = (0, 0, 0)
    )

    socket_toggle: BoolProperty(
        name = 'Socket Toggle',
        default = True
    )

    cleanup_toggle: BoolProperty(
        name = 'Cleanup Toggle',
        default = True
    )

    def execute(self, context):

        selection = bpy.context.selected_objects.copy()

        fracture(selection, self.modifier_name, self.translation, self.socket_toggle, self.cleanup_toggle)

        return {"FINISHED"}
    
    def invoke(self, context, event):

        selection = bpy.context.selected_objects

        for sel in selection:
            if len(sel.modifiers) == 0:
                self.report({"ERROR"}, 'An object has no modifiers')
                return {'CANCELLED'}

            for mod in sel.modifiers:
                if mod.name == self.modifier_name:
                    hasModifier = True
                    break
                else:
                    hasModifier = False
                
            if hasModifier == False:
                self.report({"ERROR"}, f"An object doesn't have the specified modifier")
                return {'CANCELLED'}
    
        return self.execute(context)
        

    @classmethod
    def poll(cls, context):
        # Input is not empty
        if bpy.context.scene.frac_modname == '':
            return False
        
        selection = bpy.context.selected_objects

        if len(selection) == 0:
            return False

        return True


_classes = {
    OBJECT_OT_Fracture,
}

def register():
    #_register()
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    #_unregister()
    for cls in _classes:
        bpy.utils.unregister_class(cls)