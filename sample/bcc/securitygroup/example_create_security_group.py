# -*- coding: utf-8 -*-
"""
    Example for creating a newly SecurityGroup with specified rules.
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
    endpoint = "Endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    bcc_client = bcc_client.BccClient(config)  # client 初始化
    security_group_name = 'test_security_group_'
    security_group_rule = bcc_model.SecurityGroupRuleModel(direction='ingress', # 入站/出站，取值ingress或egress
                                                           portRange='80-90', # 端口范围
                                                           protocol='tcp', # 协议类型，tcp、udp或icmp，值为空时默认取值all
                                                           sourceIp='0.0.0.0', # 源ip, 当direction为ingress时，可填此项
                                                           # destIp='0.0.0.1', # 目的ip, 当direction为egress时，可填此项
                                                           remark='',  # 备注
                                                           # sourceGroupId='g-8sf4z8sevkdj', # 源SecurityGroup的id, 与sourceIp不可同时指定
                                                           # destGroupId='g-ex1nnazr1q6x', # 目的SecurityGroup的id, 与destIp不可同时指定
                                                           ethertype='IPv4', # 网络类型，取值IPv4或IPv6。值为空时表示默认取值IPv4
                                                           )
    tags = [bcc_model.TagModel("test", "bcc")] # 标签
    security_group_rule_list = [] # 规则列表
    security_group_rule_list.append(security_group_rule)
    try:
        resp = bcc_client.create_security_group(name=security_group_name, # 创建sg的name
                                                rules=security_group_rule_list, # 创建sg的规则列表
                                                tags=tags, # sg的标签
                                                desc="test", # sg的描述
                                                client_token=str(uuid.uuid4()), # client token
                                                vpc_id="vpc-vsxcmpxyhvjt", # vpc id
                                                config=None
                                                )  # 创建sg
        security_group_id = resp.security_group_id  # 获取创建的sg id
        print("[example] create sg response: %s" % resp)
        print("[example] create sg id: %s" % security_group_id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)