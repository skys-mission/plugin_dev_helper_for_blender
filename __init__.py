# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
Blender插件入口
"""
import bpy  # pylint: disable=import-error

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
    "version": (0, 2, 2),
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

ADDON_NAME = __name__
BRIDGE = Bridge(ADDON_NAME)

ui_classes = (
    # ui36.SelfRefresh, 早期测试的时候写的自加载 子模块有问题，后面改造后可能有BUG，先注释掉
    # ui36.GlobalSettings,
    ui36.GlobalSettingPanel,
    ui36.GlobalSettingPanel.ToggleConsole,
    ui36.PluginPanel1,
    ui36.PluginPanel1.LoadPlugin,
    ui36.PluginPanel1.UnloadPlugin,
    ui36.PluginPanel1.ReloadPlugin,
    ui36.OpenURLOperator
)


def register():
    """
    注册函数，用于初始化和注册插件的各个部分。
    此函数尝试执行一系列注册操作，如果操作失败，则调用unregister函数进行卸载。
    """
    try:

        # 更新子模块 TODO 早期DEBUG的时候加的，忘记为什么要调用了
        package_mgr.reload_addon_submodules(ADDON_NAME)

        # 加载翻译
        BRIDGE.register_translations(BRIDGE.get_translations_dict())

        # 注册UI
        for cls in ui_classes:
            BRIDGE.register_class(cls)

        # Blender Scene
        bpy.types.Scene.plugin_path = scene.plugin_path
        bpy.types.Scene.is_auto_update = is_auto_update_radio

    except Exception as err:  # pylint: disable=broad-exception-caught
        unregister()
        Log.raise_error(f"Failed to register {err}")


def unregister():
    """
    注销或卸载插件时调用此函数。
    该函数负责停止协程、卸载模块、删除场景属性和卸载UI类及翻译。
    """
    # 停止所有协程
    try:
        stop_watch()
    except Exception as err:  # pylint: disable=broad-exception-caught
        Log.error(f"unregister stop_watch error: {err}")

    # 清除用户模块
    for module in pm.get_modules(1):
        try:
            package_mgr.unload_package(module)
        except Exception as err:  # pylint: disable=broad-exception-caught
            Log.error(f"unregister unload_package error: {err}")

    # 清除所有已经加载的模块 TODO 支持多模组时需要修改
    try:
        pm.clear_identifier(1)
    except Exception as err:  # pylint: disable=broad-exception-caught
        Log.error(f"unregister clear_identifier error: {err}")

    # 删除Blender Scene
    if hasattr(bpy.types.Scene, "plugin_path"):
        del bpy.types.Scene.plugin_path
    if hasattr(bpy.types.Scene, "is_auto_update"):
        del bpy.types.Scene.is_auto_update

    # 卸载所有UI
    for cls in ui_classes:
        try:
            BRIDGE.unregister_class(cls)
        except Exception as err:  # pylint: disable=broad-exception-caught
            Log.error(f"unregister unregister_class error: {err}")

    # 卸载翻译
    BRIDGE.unregister_translations()


# bpy.app.handlers.depsgraph_update_post.append(check_for_plugin_changes)
# bpy.app.handlers.depsgraph_update_post.remove(check_for_plugin_changes)


if __name__ == "__main__":
    pass
