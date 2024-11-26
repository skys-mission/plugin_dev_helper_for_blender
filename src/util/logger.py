# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

import logging
import traceback


class Log:
    _logger = None

    @staticmethod
    def _get_logger():
        if Log._logger is None:
            # 配置日志记录器
            Log._logger = logging.getLogger('plugin_dev_helper')
            Log._logger.setLevel(logging.INFO)

            # 创建一个控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # 创建一个格式化器
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)

            # 将处理器添加到日志记录器
            Log._logger.addHandler(console_handler)

        return Log._logger

    @staticmethod
    def _get_caller_info():
        stack = traceback.extract_stack()
        # 找到调用日志方法的堆栈帧
        for i, frame in enumerate(reversed(stack)):
            if frame.name in ['info', 'warning', 'error']:
                # 返回倒数第二层堆栈的文件名和行数
                if i + 1 < len(stack):
                    caller_frame = stack[-i - 2]
                    return f"{caller_frame.filename}:{caller_frame.lineno}"
        return None

    @staticmethod
    def info(message):
        logger = Log._get_logger()
        caller_info = Log._get_caller_info()
        logger.info(f"{message} ({caller_info})")

    @staticmethod
    def warning(message):
        logger = Log._get_logger()
        caller_info = Log._get_caller_info()
        logger.warning(f"{message} ({caller_info})")

    @staticmethod
    def error(message):
        logger = Log._get_logger()
        stack = traceback.format_stack()
        logger.error(f"{message}\n{''.join(stack)}")

    @staticmethod
    def raise_error(message, exception_type=RuntimeError):
        logger = Log._get_logger()
        caller_info = Log._get_caller_info()
        error_message = f"{message} ({caller_info})"
        logger.error(error_message)
        raise exception_type(error_message)
