# -*- coding: utf-8 -*-
"""example for DuMemory list_operations."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        options = dumemory_model.ListOperationsOptions(
            status="pending", limit=20, offset=0)
        resp = client.list_operations(conf.BANK_ID, options)
        print("List operations response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
