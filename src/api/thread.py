def call_blender_thread(func, *args):
    bpy.app.timers.register(func)
