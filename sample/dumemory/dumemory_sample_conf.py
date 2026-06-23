# -*- coding: utf-8 -*-
"""Shared configuration for DuMemory samples.

DuMemory authenticates with an HTTP ``Authorization: Bearer <API_KEY>`` header
(NOT BCE AK/SK), so each sample only needs the service base URL and an API key.

Replace the placeholders before running any sample.
"""

# Service entry point. The default points at the BJ region; override as needed.
BASE_URL = "https://cloud.memory.bj.baidubce.com/api"

# Bearer token issued for the calling identity, e.g. "bce-v3/ALTAK-xxx/yyy".
API_KEY = "bce-v3/ALTAK-xxx/yyy"

# A bank id used across the samples. Most endpoints scope their operations to a
# single bank, so each example reads this constant rather than hard-coding it.
BANK_ID = "sample-bank"
