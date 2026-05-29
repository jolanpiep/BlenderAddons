_needs_reload = 'gui' in locals()

from . import operators, gui

if _needs_reload:
    import importlib

    operators = importlib.reload(operators)
    gui = importlib.reload(gui)


def register():
    gui.register()
    operators.register()


def unregister():
    gui.unregister()
    operators.unregister()