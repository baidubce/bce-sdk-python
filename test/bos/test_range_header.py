"""Local range-header tests; no BOS credentials or network access required."""
import unittest
from unittest.mock import patch

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import http_headers
from baidubce.services.bos.bos_client import BosClient


class TestRangeHeader(unittest.TestCase):
    def test_get_object_open_ended_range(self):
        with patch.object(BosClient, '_send_request') as send:
            client = BosClient(BceClientConfiguration(endpoint='https://example.invalid'))
            client.get_object('bucket', 'key', range=(10, None))
        self.assertEqual(send.call_args[1]['headers'][http_headers.RANGE], b'bytes=10-')

    def test_open_ended_range(self):
        self.assertEqual(BosClient._get_range_header_dict((10, None)),
                         {http_headers.RANGE: b'bytes=10-'})
        self.assertEqual(BosClient._get_range_header_dict([0, None]),
                         {http_headers.RANGE: b'bytes=0-'})

    def test_closed_range(self):
        self.assertEqual(BosClient._get_range_header_dict((0, 9)),
                         {http_headers.RANGE: b'bytes=0-9'})

    def test_no_range(self):
        self.assertIsNone(BosClient._get_range_header_dict(None))

    def test_invalid_range(self):
        self.assertRaises(TypeError, BosClient._get_range_header_dict, '0-9')
        self.assertRaises(ValueError, BosClient._get_range_header_dict, (0,))
        self.assertRaises(TypeError, BosClient._get_range_header_dict, (None, None))
