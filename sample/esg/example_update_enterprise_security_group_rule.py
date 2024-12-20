# -*- coding: utf-8 -*-
"""
    Example for updating an enterprise security group rule from the specified enterprise security group.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.esg import esg_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    esg_client = esg_client.EsgClient(config)  # client 初始化
    try:
        # 更新企业安全组规则
        resp = esg_client.update_enterprise_security_group_rule(enterprise_security_group_rule_id='esgr-yrrdy14n5zhn', # 企业安全组id
                                                                remark='test',# 备注
                                                                source_portrange='1-10', # 源端口范围
                                                                protocol='udp', # 协议udp，tcp，icmp
                                                                portrange='1-10', # 端口范围
                                                                source_ip='10.0.0.1', # 源ip
                                                                dest_ip='10.0.0.2',# 目的ip
                                                                action='deny', # 规则动作allow/deny
                                                                local_ip='10.0.0.9', # 本地ip
                                                                priority=150
                                                                ) # 更新企业安全组规则
        print("[example] update esg rules response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)