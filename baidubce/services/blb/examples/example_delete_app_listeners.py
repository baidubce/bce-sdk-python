# !/usr/bin/env python
# coding=utf-8
"""
Samples for delete blb app listners.
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
        portlist = []
        portlist.append(451)
        resp = app_blb_client.delete_app_listeners(blb_id='lb-75f648e5', portList=portlist)
        print("[example] delete app blb listeners response : {}".format(resp))
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)