# -*- coding: utf-8 -*-
"""example for DuMemory update_document."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        listing = client.list_documents(conf.BANK_ID)
        if not listing.items:
            print("No documents in bank %s; run example_files_retain first."
                  % conf.BANK_ID)
        else:
            document_id = listing.items[0]["id"]
            request = dumemory_model.new_update_document_request(
                tags=["sample", "updated"],
            )
            resp = client.update_document(conf.BANK_ID, document_id, request)
            print("Update document response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
