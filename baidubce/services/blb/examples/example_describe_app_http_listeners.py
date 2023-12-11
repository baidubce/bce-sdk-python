# !/usr/bin/env python
# coding=utf-8
"""
Samples for describe blb app http listeners.
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
        resp = app_blb_client.describe_app_http_listener(blb_id='lb-75f648e5', listener_port=451)
        print("[example] describe app blb HTTP listener response : {}".format(resp))
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)