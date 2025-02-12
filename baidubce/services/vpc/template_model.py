# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 Piston Cloud Computing, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# -*- coding: utf-8 -*-
"""
This module provides models for template-sdk.
"""

class TemplateIpAddressInfo(object):
    """Template IP Address Info""" 

    def __init__(self, ip_address=None, description=None):
        """
        :param ip_address: ip_address
        :type ip_address: string

        :param description: description
        :type description: string
        """
        self.ip_address = ip_address
        self.description = description