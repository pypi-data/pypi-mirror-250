# -*- coding: utf-8 -*-

import os

from aivatar_project_api import AivProjectAPI


TERMINAL_TYPE = "dcc"
BUSINESS_TYPE = "AutoLUV"

def test_config():
    api = AivProjectAPI("", TERMINAL_TYPE, BUSINESS_TYPE, is_test=True)
    assert api.config.get_projects_query_url()
    assert api.config.get_manager_page_url()
    assert api.config.get_guide_page_url()

    api = AivProjectAPI("", TERMINAL_TYPE, BUSINESS_TYPE, is_test=False)
    assert api.config.get_projects_query_url()
    assert api.config.get_manager_page_url()
    assert api.config.get_guide_page_url()

def test_project_record():
    # set valid token here
    token = ""

    api = AivProjectAPI(token, TERMINAL_TYPE, BUSINESS_TYPE, is_test=True)

    api.current_project_id = -1
    assert api.current_project_id == -1
    assert api.current_project_name == ""
    assert api.current_project_experiment == 0

    assert not api.is_project_record_valid()

    valid_id = api.current_valid_project_id
    assert api.current_project_id == valid_id
    p_items = api.get_project_items()
    ids = [pi.project_id for pi in p_items]
    assert valid_id in ids
