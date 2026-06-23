# -*- coding: utf-8 -*-
"""example for DuMemory files_retain (multipart file upload)."""

import json
import os
import tempfile

from baidubce.services.dumemory import dumemory_client
from sample.dumemory import dumemory_sample_conf as conf


if __name__ == "__main__":
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    # Create a small temp file so the example is self-contained. Replace with
    # your own file_path (e.g. "/path/to/your/file.pdf") for real uploads.
    fd, file_path = tempfile.mkstemp(suffix=".txt", prefix="dumemory_sample_")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(b"hello dumemory from python sdk sample")
        with open(file_path, "rb") as fh:
            files = [(os.path.basename(file_path), fh.read())]
        request = json.dumps({
            "tags": ["sample"],
            "metadata": {"source": "dumemory python sdk sample"},
        })
        resp = client.files_retain(conf.BANK_ID, files, request)
        print("Files retain response: %s" % resp)
    except Exception as e:
        print("Exception when calling api: %s" % e)
    finally:
        try:
            os.remove(file_path)
        except OSError:
            pass
