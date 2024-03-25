# -*- coding: utf-8 -*-
"""
    Example for creating a newly esg with specified rules.
"""
import uuid
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.esg import esg_client
from baidubce.services.esg import esg_model

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    esg_client = esg_client.EsgClient(config)  # client 初始化
    name = 'test_esg'
    rule = esg_model.EnterpriseSecurityGroupRuleModel(remark='test0', # 规则备注
                                                      direction='ingress',# 规则方向 ingress or egress
                                                      action='allow', # 动作 allow or deny
                                                      protocol='tcp', # 协议 tcp or udp
                                                      portRange='78-98', # 端口范围
                                                      priority=1000, # 优先级
                                                      ethertype='IPv4', # 协议类型
                                                      sourceIp='192.168.0.1',# 源ip
                                                      destIp='10.0.0.0',# 目的ip
                                                      sourcePortRange='10-19',# 源端口范围
                                                      localIp='10.0.0.1') # 源ip
    tags = [esg_model.TagModel("test", "esg")]  # 标签
    rules = []  # 规则列表
    rules.append(rule)
    try:
        resp = esg_client.create_enterprise_security_group(name=name, # esg名称
                                                           rules=rules,    # 规则列表
                                                           desc='test0', # 描述
                                                           tags=tags, # 标签
                                                           client_token=str(uuid.uuid4()))  # 创建esg
        esg_id = resp.enterprise_security_group_id  # 获取esg id
        print("[example] create esg response: %s" % resp)
        print("[example] create esg id: %s" % esg_id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)