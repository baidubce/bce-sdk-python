# -*- coding: utf-8 -*-
"""
    Example for revoking a security group rule from the specified security group.
"""

import uuid
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.bcc import bcc_client
from baidubce.services.bcc import bcc_model

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    bcc_client = bcc_client.BccClient(config)  # client 初始化
    security_group_id = "r-eg280qrkmxp0"  # 指定SecurityGroup的id
    security_group_rule = bcc_model.SecurityGroupRuleModel(direction='ingress', # ingress or egress
                                                           portRange='80-90', # 端口范围
                                                           protocol='tcp', # tcp or udp, icmp
                                                           sourceIp='0.3.8.0', # 源ip, direction=ingress可填
                                                           # destIp='0.0.0.1', # 目的ip, direction=egress可填
                                                           remark='',  # 备注
                                                           # sourceGroupId='g-h4jdn8iw95qa', # 源SecurityGroup的id, 与sourceIp不同时选
                                                           # destGroupId='g-8sf4z8sevkdj', # 目的SecurityGroup的id, 与destIp不同时选
                                                           ethertype='IPv4', # IPv4 or IPv6
                                                           securityGroupId=security_group_id, # SecurityGroup的id
                                                           )
    try:
        resp = bcc_client.revoke_security_group_rule(security_group_id=security_group_id, # security_group_id
                                                     rule=security_group_rule,# 撤销SecurityGroupRule
                                                     client_token=str(uuid.uuid4()),  # client_token
                                                     config=None)
        print("[example] revoke sg rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    try:
        # 方式2：使用sg_version进行版本控制（推荐用于需要版本控制的场景）
        resp = bcc_client.revoke_security_group_rule(security_group_id=security_group_id,
                                                     rule=security_group_rule,
                                                     client_token=str(uuid.uuid4()),
                                                     sg_version=0, config=None)  # 安全组版本号，用于版本控制
        print("[example] revoke sg rule with version control response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)