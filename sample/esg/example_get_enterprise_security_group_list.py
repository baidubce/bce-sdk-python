# -*- coding: utf-8 -*-
"""
    Example for Listing EnterpriseSecurityGroup owned by the authenticated user.
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
        resp = esg_client.list_enterprise_security_groups(instance_id=None,# instanceid，可选项
                                                          max_keys=1, # 最大查询数量，默认1000
                                                          marker='',# 起始查询位置，可选项，默认从第一条开始
                                                          config=None)  # 查询esg
        resp = resp.enterprise_security_groups
        if len(resp) != 0:
            id = resp[0].id
            name = resp[0].name
            desc = resp[0].desc
            created_time = resp[0].created_time
            updated_time = resp[0].updated_time
            version = resp[0].version
            rules = resp[0].rules
            if len(rules) != 0:
                rule_remark = rules[0].remark
                rule_direction = rules[0].direction
                rule_action = rules[0].action
                rule_priority = rules[0].priority
                rule_ethertype = rules[0].ethertype
                rule_port_range = rules[0].port_range
                rule_source_port_range = rules[0].source_port_range
                rule_local_ip = rules[0].local_ip
                rule_source_ip = rules[0].source_ip
                rule_dest_ip = rules[0].dest_ip
                rule_enterprise_security_group_rule_id = rules[0].enterprise_security_group_rule_id
                rule_protocol = rules[0].protocol
                rule_created_time = resp[0].created_time
                rule_updated_time = resp[0].updated_time

            tags = resp[0].tags
        print("[example] list esg response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)