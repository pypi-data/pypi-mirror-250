# -*- coding: utf-8 -*-
#
# Copyright @ 2023 Tencent.com

"""API to operate project-info of users in Aivatar products, e.g. get list, choose project..."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import time
import webbrowser

from .proj_requester import *
from .config_io import *
from .logger import init_logger

logger = init_logger("aivatar_project_tools")


def set_log_details(log_details=False):
    if log_details:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)


class AivProjectAPI(object):
    QUERY_INTERVAL = 5  # don't query project lists repeatedly in 5s
    def __init__(self, token, terminal_type, business_type, is_test=False):
        self.__proj_rec = ProjectRecord(terminal_type=terminal_type, business_type=business_type)
        self.__config = NetworkConfig(os.path.join(MODULE_PATH, "configs/network_test.json")) if is_test else NetworkConfig()
        self.__requester = AivProjectRequester(token=token,
                                               business_type=business_type,
                                               url=self.__config.get_projects_query_url())
        
        self.__project_items = []
        # self.__cur_proj_item = ProjectItem()
        self.__last_query_time = 0
        self.__login_backend = None

        set_log_details(self.__config.is_log())
    
    @property
    def current_valid_project_id(self):
        # self.__cur_proj_item = self.__proj_rec.current_project_item
        cur_proj_item = self.__proj_rec.current_project_item  # local record - chosen project
        project_items = self.get_project_items()  # remote record - project lists
        ids = [pi.project_id for pi in project_items]
        pid = cur_proj_item.project_id
        # check validation
        if pid in ids: return pid
        
        cur_pid = -1
        if len(project_items) == 0: 
            logger.warning("Failed to get project id. Project list is empty")
            return -1
        if len(project_items) == 1:
            cur_pid = project_items[0].project_id
        # each user should have only one experiment project
        for pi in project_items:
            if not pi.is_experiment():
                cur_pid = pi.project_id
                break
        # set local record
        # self.__cur_proj_item = pi if cur_pid >= 0 else project_items[0]
        # self.__proj_rec.current_project_item = pi if cur_pid >= 0 else project_items[0]
        # logger.warning("The last project id \"{}\" is expired, change to: {}".format(pid, cur_pid))
        return cur_pid
    
    @property
    def current_project_id(self):
        return self.__proj_rec.current_project_item.project_id

    @current_project_id.setter
    def current_project_id(self, project_id):
        project_item = ProjectItem(project_id=project_id)
        for pi in self.__project_items:
            if pi.project_id == project_id:
                project_item = pi
        # self.__cur_proj_item = project_item
        self.__proj_rec.current_project_item = project_item
    
    @property
    def current_project_name(self):
        # if self.__cur_proj_item.project_id < 0 or not self.is_project_record_valid():
        #     pid = self.current_project_id  # refresh project item
        # return self.__cur_proj_item.project_name
        return self.__proj_rec.current_project_item.project_name
    
    @property
    def current_project_experiment(self):
        # if self.__cur_proj_item.project_id < 0 or not self.is_project_record_valid():
        #     pid = self.current_project_id  # refresh project item
        # return self.__cur_proj_item.experiment
        return self.__proj_rec.current_project_item.experiment

    def is_project_record_valid(self):
        project_item = self.__proj_rec.current_project_item
        pid = project_item.project_id
        if pid < 0: return False

        project_items = self.get_project_items()
        ids = [pi.project_id for pi in project_items]
        return pid in ids
    
    def get_project_items(self):
        """
        :return list of ProjectItem with member: project_id(str), project_name(str), experiment(int, 0/1)
        """
        cur_time = time.time()
        if not self.__project_items or (cur_time - self.__last_query_time) > self.QUERY_INTERVAL:
            try:
                self.__project_items = self.__requester.query_projects()
            except (Exception, ) as e:
                logger.error("Failed to get project list. {}".format(e.message if hasattr(e, 'message') else e))
            self.__last_query_time = cur_time
        return self.__project_items
    
    @property
    def config(self):
        return self.__config
    
    def change_network_config_path(self, path):
        """

        :param path: path to a JSON file which should contain keys: "host", "route", "guide_page_url", "manager_page_url"
        """
        token, business_type = self.__requester.token, self.__requester.business_type
        self.__config.config_path = path
        self.__requester = AivProjectRequester(token=token,
                                               business_type=business_type,
                                               url=self.__config.get_projects_query_url())
        set_log_details(self.__config.is_log())

    def set_login_backend(self, login_backend):
        if login_backend:
            attrs = ["is_login", "popup_admin", "popup_introduction"]
            if all([hasattr(login_backend, attr) for attr in attrs]):
                self.__login_backend = login_backend
            else:
                raise TypeError("No valid type of LoginBackend! Need version >= 0.5.5")
        else:
            self.__login_backend = None

    def jump_to_guide_page(self):
        if self.__login_backend and self.__login_backend.is_login():
            self.__login_backend.popup_introduction()
        else:
            self.__jump_to(self.__config.get_guide_page_url())

    def jump_to_manager_page(self):
        if self.__login_backend and self.__login_backend.is_login():
            self.__login_backend.popup_admin()
        else:
            self.__jump_to(self.__config.get_manager_page_url())
    
    def __jump_to(self, url):
        webbrowser.open(url)
