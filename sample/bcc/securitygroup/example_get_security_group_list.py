# -*- coding: utf-8 -*-
"""
    Example for Listing SecurityGroup owned by the authenticated user.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.bcc import bcc_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    bcc_client = bcc_client.BccClient(config)  # client 初始化
    try:
        resp = bcc_client.list_security_groups(instance_id="Your instance_id", # 获取指定instance的SecurityGroup列表, 可选参数
                                               vpc_id="vpc-vsxcmpxyhvjt",# vpcid
                                               marker="", # 指定开始获取列表的位置，为空则从第一条记录开始
                                               max_keys=1, # 获取的列表的最大条目数，默认值为1000
                                               config=None)
        resp = resp.security_groups
        if len(resp) != 0:
            id = resp[0].id
            name = resp[0].name
            vpc_id = resp[0].vpc_id
            desc = resp[0].desc
            created_time = resp[0].created_time
            updated_time = resp[0].updated_time
            version = resp[0].version
            rules = resp[0].rules
            if len(rules) != 0:
                rule_remark = rules[0].remark
                rule_protocol = rules[0].protocol
                rule_direction = rules[0].direction
                rule_ethertype = rules[0].ethertype
                rule_port_range = rules[0].port_range
                rule_source_group_id = rules[0].source_group_id
                rule_source_ip = rules[0].source_ip
                rule_security_group_id = rules[0].security_group_id
                rule_security_group_rule_id = rules[0].security_group_rule_id
                rule_created_time = rules[0].created_time
                rule_updated_time = rules[0].updated_time
            tags = resp[0].tags
        print(u"[example] list sg response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)