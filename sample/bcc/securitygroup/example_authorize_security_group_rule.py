# -*- coding: utf-8 -*-
"""
    Example for authorize a security group rule to the specified security group
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
    security_group_id = "g-dcqaukr9u3yn"  # 指定SecurityGroup的id
    security_group_rule1 = bcc_model.SecurityGroupRuleModel(direction='ingress', # 入站/出站，取值ingress或egress
                                                            portRange='80-90', # 端口范围
                                                            protocol='tcp', # 协议类型，tcp、udp或icmp，值为空时默认取值all
                                                            sourceIp='0.0.0.0', # 源ip, 当direction为ingress时，可填此项
                                                            # destIp='0.0.0.1', # 目的ip, 当direction为egress时，可填此项
                                                            remark='',  # 备注
                                                            # sourceGroupId='id', # 源SecurityGroup的id, 与sourceIp不可同时指定
                                                            # destGroupId='id', # 目的SecurityGroup的id, 与destIp不可同时指定
                                                            ethertype='IPv4', # 网络类型，取值IPv4或IPv6。值为空时表示默认取值IPv4
                                                            securityGroupId=security_group_id, # SecurityGroup的id
                                                            )
    try:
        resp = bcc_client.authorize_security_group_rule(security_group_id=security_group_id, # security_group_id
                                                        rule=security_group_rule1,# SecurityGroupRule
                                                        client_token=str(uuid.uuid4()),
                                                        config=None)  # client_token
        print("[example] authorize sg rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    security_group_rule2 = bcc_model.SecurityGroupRuleModel(direction='egress', # 入站/出站，取值ingress或egress
                                                            portRange='80-90', # 端口范围
                                                            protocol='tcp', # 协议类型，tcp、udp或icmp，值为空时默认取值all
                                                            # sourceIp='0.0.0.0', # 源ip, 当direction为ingress时，可填此项
                                                            destIp='0.0.0.1', # 目的ip, 当direction为egress时，可填此项
                                                            remark='',  # 备注
                                                            # sourceGroupId='id', # 源SecurityGroup的id, 与sourceIp不可同时指定
                                                            # destGroupId='id', # 目的SecurityGroup的id, 与destIp不可同时指定
                                                            ethertype='IPv4', # 网络类型，取值IPv4或IPv6。值为空时表示默认取值IPv4
                                                            securityGroupId=security_group_id, # SecurityGroup的id
                                                            )
    try:
        resp = bcc_client.authorize_security_group_rule(security_group_id=security_group_id, # security_group_id
                                                        rule=security_group_rule2,# SecurityGroupRule
                                                        client_token=str(uuid.uuid4()),
                                                        config=None)  # client_token
        print("[example] authorize sg rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    security_group_rule3 = bcc_model.SecurityGroupRuleModel(direction='ingress', # 入站/出站，取值ingress或egress
                                                            portRange='80-90', # 端口范围
                                                            protocol='tcp', # 协议类型，tcp、udp或icmp，值为空时默认取值all
                                                            # sourceIp='0.0.0.0', # 源ip, 当direction为ingress时，可填此项
                                                            # destIp='0.0.0.1', # 目的ip, 当direction为egress时，可填此项
                                                            remark='',  # 备注
                                                            sourceGroupId='g-h4jdn8iw95qa', # 源SecurityGroup的id, 与sourceIp不可同时指定
                                                            # destGroupId='g-8sf4z8sevkdj', # 目的SecurityGroup的id, 与destIp不可同时指定
                                                            ethertype='IPv4', # 网络类型，取值IPv4或IPv6。值为空时表示默认取值IPv4
                                                            securityGroupId=security_group_id, # SecurityGroup的id
                                                            )
    try:
        resp = bcc_client.authorize_security_group_rule(security_group_id=security_group_id, # security_group_id
                                                        rule=security_group_rule3,# SecurityGroupRule
                                                        client_token=str(uuid.uuid4()),
                                                        config=None)  # client_token
        print("[example] authorize sg rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)