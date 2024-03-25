# -*- coding: utf-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Example for blb unbind enterprise securitygroups
"""

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.exception import BceHttpClientError
from baidubce.services.blb import blb_client

if __name__ == '__main__':

    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "Your Endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)

    blb_client = blb_client.BlbClient(config)
    try:
        blbid = "Your blb's id"  # 指定的BLB ID
        esggroupids = ["esg-djr0dtxxxxnx"]  # 指定的企业安全组 ID
        resp = blb_client.unbind_enterprise_security_groups(blbid, esggroupids, None, config)
        print("[example] unbind enterprise securitygroups response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
