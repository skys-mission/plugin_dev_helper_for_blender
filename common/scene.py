# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

import bpy # pylint: disable=import-error

plugin_path = bpy.props.StringProperty(
    name="Plugin Path",
    description="Path to the plugin file.",
    default="",
    maxlen=512,
    subtype='FILE_PATH',
)

