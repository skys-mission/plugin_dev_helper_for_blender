# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
Blender API桥接类，实际上在这个项目并没有价值，只是我为后续开发做的实验
"""
import bpy # pylint: disable=import-error

from .local import *
from ...common.translator import get_translations_dict
from ..util.logger import Log


class Bridge:

    def __init__(self, addon_name):
        Log.info(f"Bridge init. addon name:{addon_name}")
        major, minor, _ = bpy.app.version
        self.bv = (major, minor)
        self.is_blender_gt_4_2 = self.bv >= (4, 2)
        self.is_blender_gt_4_0 = self.bv >= (4, 0)
        self.addon_name = addon_name

    def register_class(self, cls):
        bpy.utils.register_class(cls)

    def unregister_class(self, cls):
        bpy.utils.unregister_class(cls)

    def register_translations(self, translations_dict):

        # 翻译
        bpy.app.translations.register(self.addon_name, translations_dict)

    def unregister_translations(self):
        bpy.app.translations.unregister(self.addon_name)

    def get_translations_dict(self):
        if self.is_blender_gt_4_0:
            return get_translations_dict(LocalChinese40)
        else:
            return get_translations_dict(LocalChinese36)
