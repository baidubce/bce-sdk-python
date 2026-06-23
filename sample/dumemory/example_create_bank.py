# -*- coding: utf-8 -*-
"""example for DuMemory create_bank."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        request = dumemory_model.new_create_bank_request(
            name="sample bank",
            mission="created from dumemory python sdk sample",
        )
        resp = client.create_bank(conf.BANK_ID, request)
        print("Create bank response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
