# -*- coding: utf-8 -*-
"""
    Example for authorizing a security group rule to the specified security group
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
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    esg_client = esg_client.EsgClient(config)  # client 初始化
    rule1 = esg_model.EnterpriseSecurityGroupRuleModel(remark='test1', # 规则备注
                                                       direction='ingress',# 规则方向 ingress or egress
                                                       action='allow', # 动作 allow or deny
                                                       protocol='tcp', # 协议 tcp or udp
                                                       portRange='78-98', # 端口范围
                                                       priority=1000, # 优先级
                                                       ethertype='IPv4', # 协议类型
                                                       sourceIp='192.168.0.3', # 源ip
                                                       destIp='192.168.0.4', # 目的 ip
                                                       localIp='192.168.0.5', # 本地ip
                                                       sourcePortRange='78-98', # 源端口范围
                                                       )
    rule2 = esg_model.EnterpriseSecurityGroupRuleModel(remark='test2', # 规则备注
                                                       direction='egress',# 规则方向 ingress or egress
                                                       action='allow', # 动作 allow or deny
                                                       protocol='tcp', # 协议 tcp or udp
                                                       portRange='71-98', # 端口范围
                                                       priority=1000, # 优先级
                                                       ethertype='IPv4', # 协议类型
                                                       sourceIp='192.168.0.1', # 源ip
                                                       destIp='192.168.0.9', # 目的 ip
                                                       localIp='192.168.0.5',  # 本地ip
                                                       sourcePortRange='78-98',  # 源端口范围
                                                       )
    rules = []  # 规则列表
    rules.append(rule1)
    rules.append(rule2)
    try:
        resp = esg_client.authorize_enterprise_security_group_rule(rules=rules, # 规则列表, 最多20条
                                                                   client_token=str(uuid.uuid4()), # 幂等token
                                                                   enterprise_security_group_id='esg-fg01y9tdm13a' # 企业安全组 id
                                                                   )  # 创建esg rule
        print("[example] authorize esg rules response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)