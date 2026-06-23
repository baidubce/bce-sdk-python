# -*- coding: utf-8 -*-
"""example for DuMemory delete_directive."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        created = client.create_directive(
            conf.BANK_ID,
            dumemory_model.new_create_directive_request(
                name="reply-style",
                content="Sample directive to be deleted.",
            ),
        )
        resp = client.delete_directive(conf.BANK_ID, created.id)
        print("Delete directive response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
