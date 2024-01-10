# vim: ts=4:sw=4:expandtab
# -*- encoding: utf-8 -*-
"""
@File    :   logger.py
@Time    :   2020/05/17 12:27:08
@Author  :   zijiaozeng@tencent.com
@Version :   1.0
@Desc    :   edited to available for python2 by freddieyang@tencent.com
             edited as an independent module by lavenderyao@tencent.com. 2023/08/22
"""

import logging
import logging.handlers
import os
import sys
import time
from collections import OrderedDict

# from maya_go_skinning.constants import PACKAGE_NAME

__LOG_FORMAT_MAP = {
    "long": "[%(asctime)s] %(filename)s:%(lineno)d :[%(levelname)s]: %(message)s",
    "short": "[%(levelname)s] %(message)s"
}


def init_logger(package_name):
    """
    Initializes a logger with the given package name.

    :param package_name: A string representing the name of the package is used
    for log parent-folder name and filename
    """
    logger_info = LoggerInfo()
    logger_info.set_package_name(package_name)
    return logger_info.get_logger()


def get_logger(name, filepath=''):
    """
    Returns a logger object that can be used for logging information to a file.

    :param name: A string that represents the name of the logger. It is used to identify the logger
    when logging messages
    :param filepath: A string that represents the path to the log file. If no `filepath` is provided,
    the log file will be created in the default location, which is './Document/PACAKGE_NAME/log/'
    :return: a logger object.
    """
    real_name = str(time.time()) + '@' + name
    logger = logging.getLogger(real_name)

    ct = time.time()
    local_time = time.localtime(ct)
    data_head = ""  # time.strftime("%Y%m%d_%H_%M_%S", local_time)[2:8]

    logger_info = LoggerInfo()
    # print('logger_info id', id(logger_info))
    if filepath == '':
        filepath = os.path.join(os.path.expanduser('~/' + logger_info.get_package_name()), logger_info.get_postfix())
        if sys.version_info >= (3, 9) or 'document' not in filepath.lower():
            filepath = os.path.join(
                os.path.expanduser('~/Documents/' + logger_info.get_package_name()), logger_info.get_postfix())
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    file_handler = logging.FileHandler(filename=filepath)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(__LOG_FORMAT_MAP.get("long", "long"),
                                                datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)
    logger.setLevel(logging.WARNING)
    return logger


# The LoggerInfo class is a singleton class that stores information about a package name and a postfix
# for log files.
class LoggerInfo(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(LoggerInfo, cls)
            cls._instance = orig.__new__(cls)

            cls._instance.__package_name = 'aivatar'
            cls._instance.__postfix = '_aivatar.log'
            cls._instance.__logger = None
            # print('new logger', id(cls._instance), cls._instance.__package_name)
        return cls._instance

    def set_package_name(self, package_name):
        # print('set_package_name', id(self), package_name, self.__package_name)
        self.__package_name = package_name
        self.__postfix = "AivatarProject.log"
        if not self.__logger:
            self.__logger = get_logger(__name__)

    def get_package_name(self):
        # print('get_package_name', id(self), self.__package_name)
        return self.__package_name

    def get_postfix(self):
        return self.__postfix
    
    def get_logger(self):
        return self.__logger
