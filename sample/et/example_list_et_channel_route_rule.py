# -*- coding: utf-8 -*-
"""
example for et channel route rule.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_channel_route_rule_client as client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = client.EtChannelRouteRuleClient(config)  # client 初始化
    
    et_id = "etId"  # 专线ID
    et_channel_id = "etChannelId"  # 专线通道ID
    
    try:
        resp = client.list_et_channel_route_rules(et_id, et_channel_id)  # 查询专线通道路由规则
        print("[example] list et channel route rule response: %s." % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s.\n" % e)
