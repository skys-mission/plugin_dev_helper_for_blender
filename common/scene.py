# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and EcceTal
# This file is part of Plugin DEV Helper for Blender.

import bpy

plugin_path = bpy.props.StringProperty(
    name="Plugin Path",
    description="Path to the plugin file.",
    default="",
    maxlen=1024,
    subtype='FILE_PATH',
)

