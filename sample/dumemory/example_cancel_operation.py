# -*- coding: utf-8 -*-
"""example for DuMemory cancel_operation."""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    try:
        listing = client.list_operations(
            conf.BANK_ID,
            dumemory_model.ListOperationsOptions(status="pending", limit=20),
        )
        if not listing.operations:
            print("No pending operations in bank %s; nothing to cancel."
                  % conf.BANK_ID)
        else:
            operation_id = listing.operations[0].id
            resp = client.cancel_operation(conf.BANK_ID, operation_id)
            print("Cancel operation response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
