# Copyright 2026 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Offline tests for bounded file checksums."""

import base64
import hashlib
import io
import unittest
import zlib

import crc32c

from baidubce import utils


class FileChecksumTest(unittest.TestCase):
    def check_empty_range(self, checksum, expected):
        stream = io.BytesIO(b'123456789')
        stream.seek(2)
        self.assertEqual(checksum(stream, offset=4, length=0), expected)
        self.assertEqual(stream.tell(), 2)

    def test_md5_empty_range(self):
        self.check_empty_range(utils.get_md5_from_fp,
                               base64.b64encode(hashlib.md5(b'').digest()))

    def test_sha256_empty_range(self):
        self.check_empty_range(utils.get_sha256_from_fp,
                               hashlib.sha256(b'').hexdigest())

    def test_crc32_empty_range(self):
        self.check_empty_range(utils.get_crc32_from_fp, 0)

    def test_crc32c_empty_range(self):
        self.check_empty_range(utils.get_crc32c_from_fp, 0)

    def test_crc64_empty_range(self):
        self.check_empty_range(utils.get_crc64_ecma_from_fp, 0)

    def test_positive_and_unbounded_ranges(self):
        checksums = [
            (utils.get_md5_from_fp,
             lambda data: base64.b64encode(hashlib.md5(data).digest())),
            (utils.get_sha256_from_fp,
             lambda data: hashlib.sha256(data).hexdigest()),
            (utils.get_crc32_from_fp, zlib.crc32),
            (utils.get_crc32c_from_fp, crc32c.crc32c),
            (utils.get_crc64_ecma_from_fp,
             lambda data: utils._crc64_update(0, data)),
        ]
        for checksum, expected in checksums:
            for length in (1, 3, 20, -1):
                stream = io.BytesIO(b'123456789')
                stream.seek(2)
                data = b'56789'[:length] if length >= 0 else b'56789'
                self.assertEqual(
                    checksum(stream, offset=4, length=length, buf_size=2),
                    expected(data), checksum.__name__)
                self.assertEqual(stream.tell(), 2)

    def test_empty_ranges_do_not_read(self):
        class UnreadableStream(io.BytesIO):
            def read(self, size=-1):
                raise AssertionError('An empty range must not read data')

        for checksum in (utils.get_md5_from_fp, utils.get_sha256_from_fp,
                         utils.get_crc32_from_fp, utils.get_crc32c_from_fp,
                         utils.get_crc64_ecma_from_fp):
            checksum(UnreadableStream(b'123456789'), length=0)


if __name__ == '__main__':
    unittest.main()
