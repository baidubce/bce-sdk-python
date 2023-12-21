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
"""
This module provides models for ESG-SDK.
"""

class TagModel(object):
    """
    TAGModel
    """

    def __init__(self, tagKey=None, tagValue=None):
        self.tagKey = tagKey
        self.tagValue = tagValue


class EnterpriseSecurityGroupRuleModel(object):
    """
        This class define the rule of the securitygroup.
        param: remark:
            The remark for the rule.
        param: direction:
            The parameter to define the rule direction,available value are "ingress/egress".
        param: ethertype:
            The ethernet protocol.
        param: portRange:
            The port range to specify the port which the rule will work on.
            Available range is rang [0, 65535], the fault value is "" for all port.
        param: sourceportRange:
            The source port range to specify the port which the rule will work on.
            Available range is rang [0, 65535], the fault value is "" for all port.
        param: protocol:
            The parameter specify which protocol will the rule work on, the fault value is "" for all protocol.
            Available protocol are tcp, udp and icmp.
        param: sourceIp:
            The source ip range with CIDR formats. The default value 0.0.0.0/0 (allow all ip address),
            other supported formats such as {ip_addr}/12 or {ip_addr}. Only supports IPV4.
            Only works for  direction = "ingress".
        param: destIp:
            The destination ip range with CIDR formats. The default value 0.0.0.0/0 (allow all ip address),
            other supported formats such as {ip_addr}/12 or {ip_addr}. Only supports IPV4.
            Only works for  direction = "egress".
        param: EnterprisesecurityGroupId:
            The id of the Enterprisesecuritygroup for the rule.
        param: localIp:
            The parameter specify the localIP (allow all ip address: all).
        param: priority:
            The parameter specify the priority of the rule(range 1-1000).
        param: action:
        	The parameter specify the action of the rule, available value are "allow/deny".
	"""

    def __init__(self, remark=None, direction=None, ethertype=None, portRange=None, sourcePortRange=None,
                 protocol=None, sourceIp=None, destIp=None,
                 enterpriseSecurityGroupId=None, action=None, localIp=None, priority=None):
        self.remark = remark
        self.direction = direction
        self.ethertype = ethertype
        self.portRange = portRange
        self.sourcePortRange = sourcePortRange
        self.protocol = protocol
        self.sourceIp = sourceIp
        self.destIp = destIp
        self.enterpriseSecurityGroupId = enterpriseSecurityGroupId
        self.action = action
        self.localIp = localIp
        self.priority = priority
