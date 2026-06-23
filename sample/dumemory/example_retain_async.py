# -*- coding: utf-8 -*-
"""example for DuMemory retain_async (asynchronous write)."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        items = [
            dumemory_model.new_memory_item(content="Async retain sample item."),
        ]
        request = dumemory_model.new_retain_request(items=items)
        resp = client.retain_async(conf.BANK_ID, request)
        print("Retain async response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
