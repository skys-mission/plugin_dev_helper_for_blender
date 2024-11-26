# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
import bpy

from .src.util.logger import Log
from .src.models.ui36 import is_auto_update_radio
from .src.handler.watch_handler import stop_watch
from .src.api.bridge import Bridge
from .common import scene
from .src.models import ui36
from .src.handler import package_mgr
from .src.data import py_models as pm

# 插件信息字典，用于存储插件的元数据
bl_info = {
    # 插件名称
    "name": "Plugin DEV Helper",
    # 插件作者
    "author": "SoyMilkWhisky, github.com/skys-mission",
    # 插件版本号
    "version": (0, 2, 1),
    # 兼容的Blender版本
    "blender": (3, 6, 0),
    # 插件在Blender界面中的位置
    "location": "View3D > N-Panel  > Plugin DEV Helper",
    # 插件描述
    "description": "Dynamically load, unload, and auto-reload plugins.",
    # 插件类别
    "category": "Development",
    "doc_url": "https://whiskyai.xyz/doc/blender/addon/plugin_dev_helper_for_blender",
    "tracker_url": "https://github.com/skys-mission/plugin_dev_helper_for_blender/issues",
    "warning": "This plugin is designed for users with software development expertise."
}

addon_name = __name__
bridge = Bridge(addon_name)

ui_classes = (
    # ui36.SelfRefresh, 早期测试的时候写的自加载 子模块有问题，后面改造后可能有BUG，先注释掉
    # ui36.GlobalSettings,
    ui36.PluginPanel1,
    ui36.PluginPanel1.LoadPlugin,
    ui36.PluginPanel1.UnloadPlugin,
    ui36.PluginPanel1.ReloadPlugin,
    ui36.OpenURLOperator
)


def register():
    try:

        global bridge
        global addon_name

        # 更新子模块 TODO 早期DEBUG的时候加的，忘记为什么要调用了
        package_mgr.reload_addon_submodules(addon_name)

        # 加载翻译
        bridge.register_translations(bridge.get_translations_dict())

        # 注册UI
        for cls in ui_classes:
            bridge.register_class(cls)

        # Blender Scene
        bpy.types.Scene.plugin_path = scene.plugin_path
        bpy.types.Scene.is_auto_update = is_auto_update_radio

    except Exception as err:
        unregister()
        Log.raise_error(f"Failed to register {err}")

    pass


def unregister():
    global bridge

    # 停止所有协程
    try:
        stop_watch()
    except Exception as err:
        Log.error(f"unregister stop_watch error: {err}")

    # 清除用户模块
    for module in pm.get_modules(1):
        try:
            package_mgr.unload_package(module)
        except Exception as err:
            Log.error(f"unregister unload_package error: {err}")

    # 清除所有已经加载的模块 TODO 支持多模组时需要修改
    try:
        pm.clear_identifier(1)
    except Exception as err:
        Log.error(f"unregister clear_identifier error: {err}")

    # 删除Blender Scene
    if hasattr(bpy.types.Scene, "plugin_path"):
        del bpy.types.Scene.plugin_path
    if hasattr(bpy.types.Scene, "is_auto_update"):
        del bpy.types.Scene.is_auto_update

    # 卸载所有UI
    for cls in ui_classes:
        try:
            bridge.unregister_class(cls)
        except Exception as err:
            Log.error(f"unregister unregister_class error: {err}")

    # 卸载翻译
    bridge.unregister_translations()
    pass


# bpy.app.handlers.depsgraph_update_post.append(check_for_plugin_changes)
# bpy.app.handlers.depsgraph_update_post.remove(check_for_plugin_changes)


if __name__ == "__main__":
    pass
