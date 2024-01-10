# -*- coding: utf-8 -*-
#
# Copyright @ 2023 Tencent.com

"""API to operate project-info of users in Aivatar products, e.g. get list, choose project..."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from aivatar_project_api.core import AivProjectAPI


__all__ = ["AivProjectAPI"]

try:
    from pkg_resources import get_distribution
    __version__ = get_distribution(__name__).version
except (Exception, ):
    # Package is not installed
    __version__ = "0.0.0-dev.1"
