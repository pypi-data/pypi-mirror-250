# -*- coding: utf-8 -*-

import json
import os
import sys
from threading import Lock

from .constants import *
from .proj_requester import ProjectItem
from .logger import init_logger

logger = init_logger("aivatar_project_tools")

if sys.version_info < (3, 0):
    import codecs
    open = codecs.open

ROOT = os.path.join(os.getenv("APPDATA"), PROJECT_RECORD_DIR)
if not os.path.exists(ROOT):
    os.makedirs(ROOT)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
KEY_ID = "PROJECT_ID"
KEY_NAME = "PROJECT_NAME"
KEY_EXPERIMENT = "EXPERIMENT"
SEPARATOR = "="


class NetworkConfig(object):
    """parse json-pattern config file
    The file should contain keys: host, route, guide_page_url, manager_page_url.
    
    """
    def __init__(self, path=""):
        self.__config = {}
        self.__init_config(path)
    
    @property
    def config_path(self):
        return self.__config_path
    
    @config_path.setter
    def config_path(self, path):
        self.__init_config(path)

    def __init_config(self, path):
        if os.path.exists(path):
            self.__config_path = path
        else:
            self.__config_path = os.path.join(MODULE_PATH, NET_CONFIG)
            if path:
                logger.warning("Invalid config path [{}]! Changed to default {}.".format(path, self.__config_path))
            if not os.path.exists(self.__config_path):
                logger.error("Error config path: {}".format(self.__config_path))
                return
        
        with open(self.__config_path, 'r') as cfg:
            self.__config = json.load(cfg)

    def get_projects_query_url(self):
        return "{host}/{route}".format(
                host=self.__config.get("host", "https://service.arthub.woa.com"),
                route=self.__config.get("route", "account/account/openapi/v3/core/get-aivatar-projects-by-account")
            )

    def get_guide_page_url(self):
        return self.__config.get("guide_page_url", "")


    def get_manager_page_url(self):
        return self.__config.get("manager_page_url", "")
    
    def is_log(self):
        return self.__config.get("log", False)


class ProjectRecord(object):
    FILE_LOCK = Lock()
    
    def __init__(self, terminal_type, business_type):
        self.__terminal_type = terminal_type
        self.__business_type = business_type

        path = os.path.join(ROOT, "{}/{}".format(self.__business_type, self.__terminal_type))
        if not os.path.exists(path):
            os.makedirs(path)
        self.__file_path = os.path.join(path, PROJECT_RECORD_FILE)

    @property
    def current_project_item(self):
        if not os.path.exists(self.__file_path): return ProjectItem()

        pid, pname, experiment = -1, "", 0
        self.FILE_LOCK.acquire()
        with open(self.__file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.count(SEPARATOR) != 1: continue
                line = line[:-1]  # skip \n
                [k, v] = line.split(SEPARATOR)
                if k == KEY_ID:
                    try: pid = int(v)
                    except ValueError: pass
                elif k == KEY_NAME:
                    pname = v
                elif k == KEY_EXPERIMENT:
                    experiment = 1 if v.lower() in ["1",  "true", "t"] else 0
        self.FILE_LOCK.release()
        return ProjectItem(project_id=pid, project_name=pname, experiment=experiment)

    @current_project_item.setter
    def current_project_item(self, project_item):
        if not os.path.exists(os.path.dirname(self.__file_path)):
            os.makedirs(os.path.dirname(self.__file_path))

        self.FILE_LOCK.acquire()
        try:
            self.__write(project_item)
        except (Exception, ) as e:
            logger.error("Error occured when record project: {}".format(e.message if hasattr(e, 'message') else e))
            try:
                self.enable_file_permissions(self.__file_path)
                self.__write(project_item)
            except (Exception, ) as e: pass
        self.FILE_LOCK.release()
    
    def __write(self, project_item):
        with open(self.__file_path, "w", encoding="utf-8") as f:
            f.write("{}{}{}\n".format(KEY_ID, SEPARATOR, project_item.project_id))
            f.write("{}{}{}\n".format(KEY_NAME, SEPARATOR, project_item.project_name))
            f.write("{}{}{}\n".format(KEY_EXPERIMENT, SEPARATOR, project_item.experiment))

    @staticmethod
    def enable_file_permissions(file_path):
        current_permissions = os.stat(file_path).st_mode
        new_permissions = current_permissions | 0o600
        os.chmod(file_path, new_permissions)
