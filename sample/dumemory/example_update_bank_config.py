# -*- coding: utf-8 -*-
"""example for DuMemory update_bank_config."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        request = dumemory_model.new_bank_config_update(
            updates={"retain_chunk_size": 800},
        )
        resp = client.update_bank_config(conf.BANK_ID, request)
        print("Update bank config response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
