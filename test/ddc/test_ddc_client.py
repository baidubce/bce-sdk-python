# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
Unit tests for ddc client.
"""

import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.ddc import ddc_client


class TestDdcClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = 'ddc.su.baidubce.com'
        AK = 'your-access-key-id'
        SK = 'your-secret-access-key'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = ddc_client.DdcClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.the_client = None

    def test_lazydrop_create_hard_link(self):
        """
        test case for create hard link
        """
        instance_id = 'ddc-mox9l5gy'
        db_name = 'xyltest'
        table_name = 'test05'
        
        self.the_client.lazydrop_create_hard_link(instance_id=instance_id, db_name=db_name, table_name=table_name)
        
    def test_lazydrop_delete_hard_link(self):
        """
        test case for delete hard link
        """
        instance_id = 'ddc-mox9l5gy'
        db_name = 'xyltest'
        table_name = 'test05'
        
        self.the_client.lazydrop_delete_hard_link(instance_id=instance_id, db_name=db_name, table_name=table_name)
        
    def test_list_log_by_instance_id(self):
        """
        test case for list log by instanceId
        """
        instance_id = 'ddc-mox9l5gy'
        log_type = 'slow'
        datetime = '2021-03-16'
        
        self.the_client.list_log_by_instance_id(instance_id=instance_id, log_type=log_type, datetime=datetime)
        
    def test_get_log_by_id(self):
        """
        test case for get log by logid
        """
        instance_id = 'ddc-mox9l5gy'
        log_id = 'ddc-mox9l5gy_errlog.202103172000'
        download_valid_time_in_sec = '1000'
        
        self.the_client.get_log_by_id(instance_id=instance_id, log_id=log_id, download_valid_time_in_sec=download_valid_time_in_sec)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDdcClient("test_lazydrop_create_hard_link"))
    suite.addTest(TestDdcClient("test_lazydrop_delete_hard_link"))
    # suite.addTest(TestDccClient("test_get_dedicated_host"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
