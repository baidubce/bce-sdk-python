# -*- coding: utf-8 -*-
"""
    In a multi-line master-slave routing mode, switching the main route to the backup route.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.route import route_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    route_client = route_client.RouteClient(config)  # client 初始化
    try:
        resp = route_client.switch_route(route_rule_id="Your routeruleid") # 指定路由规则ID
        print("[example] switch route rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)