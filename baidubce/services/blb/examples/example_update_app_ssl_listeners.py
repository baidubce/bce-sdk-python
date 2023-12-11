# !/usr/bin/env python
# coding=utf-8
"""
Samples for update blb app ssl listeners.
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
        resp = app_blb_client.update_app_ssl_listener(
                blb_id='lb-75f648e5', listener_port=445, scheduler='RoundRobin', dual_auth=False)
        print("[example] update app blb ssl listener response : {}".format(resp))
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)