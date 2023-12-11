# !/usr/bin/env python
# coding=utf-8
"""
Samples for create blb policys.
"""
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.exception import BceHttpClientError

from baidubce.services.blb import app_blb_client

if __name__ == '__main__':

    config = BceClientConfiguration(
        credentials=BceCredentials(
            access_key_id='YourAK', # 用户的ak
            secret_access_key='YourSK' # 用户的sk
        ),
        endpoint='blb.bj.qasandbox.baidu-int.com' # console的endpoint

    )
    app_blb_client = app_blb_client.AppBlbClient(config)
    try:
        app_policy_vos = []
        rule_list = []
        app_rule = {
            'key': '*',
            'value': '*'
        }
        rule_list.append(app_rule)
        app_policy = {
            'desc': 'for test',
            'appServerGroupId': 'sg-4366acf7',
            'backendPort': 80,
            'priority': 2334,
            'ruleList': rule_list
        }
        app_policy_vos.append(app_policy)
        resp = app_blb_client.create_policys(blb_id='lb-75f648e5', listener_port=443, 
                                             app_policy_vos=app_policy_vos)
        print("[example] create app blb policy response : {}".format(resp))
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)