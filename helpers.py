import bpy
import bmesh
import mathutils

#FUNCTION: reset selection for Operators
def select(object):

    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)
    bpy.context.view_layer.objects.active = object

#FUNCTION: Duplicate object and return new object
#TODO: Remove Duplicate operator
def duplicate(object):
    
    select(object)

    bpy.ops.object.duplicate()
    obj = bpy.context.active_object

    return obj

    me = bpy.data.meshes.new_from_object(object)
    obj = bpy.data.objects.new(object.name, me)
    
    #BUG: Seems complex to copy all modifier values?!
    #for mod in object.modifiers:
        #obj.modifiers.new(name=mod.name, type=mod.type)
        #obj.modifiers[mod.name].values

    #BUG: Trying temp_override, but doesn't seem to work?
    with bpy.context.temp_override(selected_objects=obj, active_object=object):
        bpy.ops.object.make_links_data(type='MODIFIERS')

    #NOTE: Solution from someone else
    for modifier in active_object.modifiers:
        # Om modifiern finns sedan tidigare återanvänder vi den
        modifier_copy = obj.modifiers.get(modifier.name, None)
        
        # Annars skapar vi en ny
        if not modifier_copy:
            modifier_copy = obj.modifiers.new(modifier.name, modifier.type)
        
        properties = [p.identifier for p in modifier.bl_rna.properties
                        if not p.is_readonly]
        
        for prop in properties:
            setattr(modifier_copy, prop, getattr(modifier, prop))

    
    bpy.context.collection.objects.link(obj)

    return obj

#FUNCTION: Rename object
def rename(object, name):
    object.name = name

#FUNCTION: 0 = A, 1 = B, 2 = C, (...), 26 = AA, 27 = AB, 28 = AC, ...
def numbersToLetters(number: int) -> str:

    cycle, remainder = divmod(number, 26)

    letter = chr(ord('A') + remainder)
    
    if cycle == 0:
        return letter
    
    return numbersToLetters(cycle - 1) + letter

#FUNCTION: Apply all modifiers until specified modifier
#TODO: Remove Apply Modifier operator
def applyModifiers(object, modifier_name):

    select(object)

    # Find final modifier index  
    for i, mod in enumerate(object.modifiers):
        if mod.name == modifier_name:
            final_mod_index = i+1
    
    # Apply modifiers until final modifier index
    for mod in object.modifiers[:final_mod_index]:
        # NOTE: Replacing this with a direct call to apply the modifiers requires to dig into the dependency graph. A complex topic,how blender handles modifiers, shape keys and other data. Stick with the operator for now. 
        bpy.ops.object.modifier_apply(modifier=mod.name)

def unparent(object):
    origin = object.parent.location
    
    object.parent = None
    object.location = origin

    return

#FUNCTION: Translate object
def translate(object, translation):

    # NOTE: If you want to transfer locations it can be good to use bpy.context.object.matrix_world instead. 

    oldLoc = object.location
    translation = mathutils.Vector(translation)

    object.location = oldLoc + translation

#FUNCTION: Separate object to loose parts and return objects
#TODO: Remove separate operator
def separate(object):

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()

    return bpy.context.selected_objects

#FUNCTION: Add new empty object with SOCKET_ prefix
def addSocket(object):

    socket = bpy.data.objects.new(object.name, None)
    socket.location = object.location
    bpy.context.collection.objects.link(socket)

    socket.name = f'SOCKET_{object.name}'

    return socket

#FUNCTION: Origin to Geometry by Bounds
#TODO: Remove Origin Set operator
def originToGeometry(object):

    select(object)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    return

    c = {"object" : bpy.context.scene.objects[0],
        "selected_objects" : bpy.context.scene.objects,
        "selected_editable_objects" : bpy.context.scene.objects}
        
    if mesh_obs:
        with bpy.context.temp_override(**c):
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

#FUNCTION: Parent child to parent while preserving location
def parent(child, parent):

    child.parent = parent
    child.location = child.location - parent.location

#FUNCTION: Clean up some non-manifold meshes
def cleanup(objects):
    
    # NOTE: Might be easier to keep this way for now. And first get more familiar with UI and addons. This requires diving deep into bmesh and mesh data. Good enough for now
    
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    #bpy.ops.mesh.select_by_pole_count(pole_count=1, type='EQUAL')
    #bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.editmode_toggle()