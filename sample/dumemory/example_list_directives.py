# -*- coding: utf-8 -*-
"""example for DuMemory list_directives."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        options = dumemory_model.ListDirectivesOptions(
            active_only=True, limit=20, offset=0)
        resp = client.list_directives(conf.BANK_ID, options)
        print("List directives response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
