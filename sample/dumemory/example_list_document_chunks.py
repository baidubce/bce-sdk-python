# -*- coding: utf-8 -*-
"""example for DuMemory list_document_chunks."""

from baidubce.services.dumemory import dumemory_client
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
            resp = client.list_document_chunks(
                conf.BANK_ID, document_id, limit=20, offset=0)
            print("List document chunks response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
