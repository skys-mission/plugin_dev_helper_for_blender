# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

import bpy

from .local import *
from ...common.translator import get_translations_dict


class Bridge:

    def __init__(self, addon_name):
        print(f"debug:{addon_name}")
        major, minor, _ = bpy.app.version
        self.bv = (major, minor)
        self.is_blender_4_2 = self.bv >= (4, 2)
        self.addon_name = addon_name

    def register_class(self, cls):
        bpy.utils.register_class(cls)

    def unregister_class(self, cls):
        bpy.utils.unregister_class(cls)

    def register_translations(self, translations_dict):

        # 翻译
        if self.is_blender_4_2:
            print(f"A:{get_translations_dict(LocalChinese42)}")
            bpy.app.translations.register(self.addon_name, translations_dict)
        else:
            print(f"A:{get_translations_dict(LocalChinese36)}")
            bpy.app.translations.register(self.addon_name, translations_dict)

    def unregister_translations(self):
        bpy.app.translations.unregister(self.addon_name)

    def get_translations_dict(self):
        if self.is_blender_4_2:
            return get_translations_dict(LocalChinese42)
        else:
            return get_translations_dict(LocalChinese36)
