# -*- coding: utf-8 -*-
"""example for DuMemory get_directive."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        # bootstrap a directive so the sample is runnable end-to-end
        created = client.create_directive(
            conf.BANK_ID,
            dumemory_model.new_create_directive_request(
                name="reply-style",
                content="Always answer in concise bullet points.",
            ),
        )
        resp = client.get_directive(conf.BANK_ID, created.id)
        print("Get directive response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)

