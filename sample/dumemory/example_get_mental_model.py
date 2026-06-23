# -*- coding: utf-8 -*-
"""example for DuMemory get_mental_model."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        created = client.create_mental_model(
            conf.BANK_ID,
            dumemory_model.new_create_mental_model_request(
                name="user-preferences",
                source_query="What are the user's stable preferences?",
            ),
        )
        resp = client.get_mental_model(conf.BANK_ID, created.mental_model_id, detail="full")
        print("Get mental model response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
