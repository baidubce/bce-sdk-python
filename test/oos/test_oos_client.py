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
Unit tests for oos client.
"""
import sys
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.oos import oos_client, oos_model

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://oos.bj.baidubce.com'
AK = b'your access key'
SK = b'your secret key'


class TestOosClient(unittest.TestCase):
    """
    Test class for oos sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.client = oos_client.OosClient(config)

    def test_create_template(self):
        """
        test create template
        """
        property1 = {
            "instances": [
                {
                    "instanceId": "i-khWMkTxx"
                }
            ]
        }
        operator1 = oos_model.OperatorModel("stop_bcc", "BCE::BCC::StopInstance", property1)
        response = self.client.create_template("test_template_02", [operator1])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_check_template(self):
        """
        test check template
        """
        property1 = {
            "instances": [
                {
                    "instanceId": "i-khWMkTxx"
                }
            ]
        }
        operator1 = oos_model.OperatorModel("stop_bcc", "BCE::BCC::StopInstance", property1)
        response = self.client.check_template("test_template_02", [operator1])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_template(self):
        """
        test update template
        """
        property1 = {
            "instances": [
                {
                    "instanceId": "i-khWMkTxx"
                }
            ]
        }
        operator1 = oos_model.OperatorModel("start_bcc", "BCE::BCC::StartInstance", property1)
        response = self.client.update_template("tpl-MtBUanxL", "test_template_02", [operator1])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_template_detail(self):
        """
        test get template detail
        """
        response = self.client.get_template_detail("test_template_02")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response.result)

    def test_get_template_list(self):
        """
        test get template list
        """
        response = self.client.get_template_list(1, 10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response.result)

    def test_get_operator_list(self):
        """
        test get operator list
        """
        response = self.client.get_operator_list(1, 10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response.result)

    def test_create_execution(self):
        """
        test create execution
        """
        property1 = {
            "content": "ls /",
            "user": "root",
            "workDir": "/",
            "__workerSelectors__": [
                {
                    "instanceId": "i-VZIunExx"
                }
            ]
        }
        operator1 = oos_model.OperatorModel("run_script", "BCE::Agent::ExecuteShell", property1)
        template1 = oos_model.TemplateModel("test1", [operator1])
        response = self.client.create_execution(template1)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response.result)

    def test_get_execution_detail(self):
        """
        test get execution detail
        """
        response = self.client.get_execution_detail("d-bdJ4NxNbtdxs")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response.result)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
