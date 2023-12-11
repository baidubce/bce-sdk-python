# !/usr/bin/env python
# coding=utf-8
"""
Samples for delete blb policys.
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
        policys_list = []
        policys_list.append("policy-bbae9e3c")
        resp = app_blb_client.delete_policys(blb_id='lb-75f648e5', listener_port=443, policys_list=policys_list)
        print("[example] delete app blb listeners response : {}".format(resp))
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)