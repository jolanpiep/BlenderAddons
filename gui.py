import bpy

class JOLAN_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Jolan"
    bl_label = "Jolan's Utilities"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        layout.label(text = 'Fracture Processing')
        box = layout.box()
        col = box.column()
        
        col.label(text = f'Translation:')
        row = col.row(align=True)
        row.prop(context.scene, 'frac_translation', text = '')
        row.use_property_decorate = False

        col.label(text = f'Apply Modifiers until:')
        col.prop(context.scene, 'frac_modname', text = '', placeholder = 'Modifier Name')

        row = col.row(align=True)
        row.label(text = 'Generate Sockets:')
        row.prop(context.scene, 'frac_socket_toggle', text = '')

        row = col.row(align=True)
        row.label(text = 'Cleanup Fractures:')
        row.prop(context.scene, 'frac_cleanup_toggle', text = '')

        op = box.operator('object.fracture', text="Process", icon="STICKY_UVS_DISABLE")
        
        op.modifier_name = context.scene.frac_modname
        op.translation = context.scene.frac_translation
        op.socket_toggle = context.scene.frac_socket_toggle


        # layout.separator(factor=5.0)

_classes = {
    JOLAN_PT_panel,
}

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.frac_modname = bpy.props.StringProperty(name = 'frac_modname')
    bpy.types.Scene.frac_translation = bpy.props.FloatVectorProperty(name = 'frac_translation')
    bpy.types.Scene.frac_socket_toggle = bpy.props.BoolProperty(name = 'frac_socket_toggle', default = True)
    bpy.types.Scene.frac_cleanup_toggle = bpy.props.BoolProperty(name = 'frac_cleanup_toggle', default = True)

def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.frac_modname
    del bpy.types.Scene.frac_translation