# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

def get_translations_dict(local):
    translations_dict = {
        local: translation_map
    }

    return translations_dict


translation_map = {
    ("*", "Plugin Path"): "插件路径",
    ("*", "Global Settings"): "全局设置",
    ("*", "Addon DEV Helper"): "插件开发助手",
    ("*", "Auto change detection(Not rec.)"): "自动检测变化(不推荐)",
    ("*", "DEV Plugin 1"): "开发插件 1",
    ("*", "Perform the operation of loading plugins"): "执行加载插件的操作",
    ("*", "Perform the operation of uninstalling plugins"): "执行卸载插件的操作",
    ("*", "Perform the operation of reloading plugins"): "执行重载插件的操作",
    ("*", "Enable/Disable Automatic check for changes and reload(1.5s)"): "开启/关闭 自动检查变化重载(1.5s)",
    ("Operator", "user doc."): "用户文档",
    ("Operator", "open source"): "开源地址",
    ("Operator", "Load Plugin 1"): "加载插件 1",
    ("Operator", "Unload Plugin 1"): "卸载插件 1",
    ("Operator", "Reload Plugin 1"): "重载插件 1",
}
