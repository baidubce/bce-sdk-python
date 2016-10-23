#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief bes_base
"""

import bes_conf

class BaseTest(object):
    """
    base func
    """
    def __init__(self):
        self.host = bes_conf.HOST
        self.ak = bes_conf.AK
        self.sk = bes_conf.SK

    def setUp(self):
        """
        prepare
        """
        pass


