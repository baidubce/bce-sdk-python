# -*- coding: utf-8 -*-
"""
example for add et channel users
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et.et_client import EtClient

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = 'Your endpoint'
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = EtClient(config)
    try:
        resp = client.add_et_channel_users(et_id='dcphy-gq65bz9ip712',
                                           et_channel_id='dedicatedconn-zy9t7n91k0iq',
                                           authorized_users=['8770d0e94e2728ca81b0ec99db9f4df8'],
                                           client_token=str(uuid.uuid4()))
        print("add et channel users response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
