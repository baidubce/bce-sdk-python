# -*- coding: utf-8 -*-
"""
    Example for updating a security group rule from the specified security group
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
    security_group_rule_id = "g-dcqaukr9u3yn"  # 指定SecurityGroupRule的id
    try:
        resp = bcc_client.update_security_group_rule(security_group_rule_id=security_group_rule_id,# 指定SecurityGroupRuleid
                                                     remark="test_update",# 指定标记
                                                     direction="ingress", # 指定方向 ingress or egress
                                                     protocol="udp", # 指定协议 tcp or udp
                                                     portrange='68-90',# 指定端口范围
                                                     source_ip="10.0.0.1", # 指定源ip, 不能否同时指定sourceGroupId
                                                     # sourcegroup_id="sourcegroup_id",
                                                     # dest_ip="10.0.0.2", # 指定目的ip, 不能否同时指定destGroupId
                                                     # destgroup_id="destgroup_id"
                                                     )
        print("[example] update sg rule response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)