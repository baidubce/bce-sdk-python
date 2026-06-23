# -*- coding: utf-8 -*-
"""example for DuMemory get_bank_config."""

from baidubce.services.dumemory import dumemory_client
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        resp = client.get_bank_config(conf.BANK_ID)
        print("Get bank config response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
