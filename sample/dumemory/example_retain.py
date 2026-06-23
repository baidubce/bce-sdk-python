# -*- coding: utf-8 -*-
"""example for DuMemory retain (synchronous write)."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        items = [
            dumemory_model.new_memory_item(content="Today I learned about DuMemory."),
            dumemory_model.new_memory_item(content="Bearer token auth replaces AK/SK here."),
        ]
        request = dumemory_model.new_retain_request(items=items)
        resp = client.retain(conf.BANK_ID, request)
        print("Retain response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
