# -*- coding: utf-8 -*-

# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
#  of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions
# and limitations under the License.
"""
This module provide eni settings information.
"""

class EniIPSet(object):
    """ENI IP Set"""

    def __init__(self, public_ip=None, private_ip=None, primary=None):
        """

        :param public_ip: public IP
        :type public_ip: string

        :param private_ip: private IP
        :type private_ip: string

        :param primary: The parameter to specify whether is primary IP
        :type primary: bool
        """
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.primary = primary
