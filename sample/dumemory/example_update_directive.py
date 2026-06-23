# -*- coding: utf-8 -*-
"""example for DuMemory update_directive."""

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
                content="Initial directive content.",
            ),
        )
        request = dumemory_model.new_update_directive_request(
            content="Answer in concise bullet points; cite sources when possible.",
        )
        resp = client.update_directive(conf.BANK_ID, created.id, request)
        print("Update directive response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
