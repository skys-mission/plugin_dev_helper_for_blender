# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
Blender API桥接类，实际上在这个项目并没有价值，只是我为后续开发做的实验
"""
import bpy  # pylint: disable=import-error

from .local import LOCAL_CH_36, LOCAL_CH_40
from ...common.translator import get_translations_dict
from ..util.logger import Log


class Bridge:
    """
    Blender和插件之间的桥梁类，用于处理插件的注册、注销和翻译相关事宜。
    """

    def __init__(self, addon_name):
        """
        初始化桥梁类。

        参数:
        addon_name (str): 插件的名称，用于日志和翻译的标识。
        """
        Log.info(f"Bridge init. addon name:{addon_name}")
        major, minor, _ = bpy.app.version
        self.bv = (major, minor)
        self.is_blender_gt_4_2 = self.bv >= (4, 2)
        self.is_blender_gt_4_0 = self.bv >= (4, 0)
        self.addon_name = addon_name

    def register_class(self, cls):
        """
        注册一个类到Blender中。

        参数:
        cls (type): 要注册的类。
        """
        bpy.utils.register_class(cls)

    def unregister_class(self, cls):
        """
        从Blender中注销一个类。

        参数:
        cls (type): 要注销的类。
        """
        bpy.utils.unregister_class(cls)

    def register_translations(self, translations_dict):
        """
        注册插件的翻译。

        参数:
        translations_dict (dict): 包含翻译的字典。
        """
        # 翻译
        bpy.app.translations.register(self.addon_name, translations_dict)

    def unregister_translations(self):
        """
        从Blender中注销插件的翻译。
        """
        bpy.app.translations.unregister(self.addon_name)

    def get_translations_dict(self):
        """
        获取翻译字典。

        返回:
        dict: 根据Blender版本选择的翻译字典。
        """
        if self.is_blender_gt_4_0:
            return get_translations_dict(LOCAL_CH_40)

        return get_translations_dict(LOCAL_CH_36)
