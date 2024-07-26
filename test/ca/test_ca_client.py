import sys
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.ca import ca_client, ca_model

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://ca.bj.baidubce.com'
AK = b''
SK = b''


class TestCaClient(unittest.TestCase):
    """
     Test class for ca sdk client
     """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = ca_client.CaClient(config)

    def test_batch_get_agent(self):
        instance_list = [
            ca_model.Instance("i-9y7wPdlG"),
            ca_model.Instance("i-ZCHupg0z")
        ]
        response = self.client.batch_get_agent(instance_list)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_action(self):
        user_id = ''
        execution = 'SAVE_AND_RUN'
        action = ca_model.Action(
            "", "", "COMMAND", "yyy-python-test", 60,
            ca_model.Command(
                "SHELL", "ls", "INDIVIDUAL", False, [], "root", "/home"
            )
        )
        parameter = {}
        target_selector = ca_model.TargetSelector("BCC", [])
        target_selector_type = "INSTANCES_LIST"
        targets = [ca_model.Target("BCC", "i-kBdE8Tav")]
        response = self.client.create_action(execution, user_id, action, targets, parameter, target_selector,
                                             target_selector_type)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_action(self):
        id = "c-xadYvQ1FSA5viD4E"
        response = self.client.delete_action(id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_action(self):
        action = ca_model.Action(
            "c-k7zXV794Jjz1WZC8", "", "COMMAND", "yyy-python-test-update", 60,
            ca_model.Command(
                "SHELL", "ls", "INDIVIDUAL", False, [], "root", "/home"
            )
        )
        execution = "SAVE"
        response = self.client.update_action(action, execution)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_action(self):
        id = "c-k7zXV794Jjz1WZC8"
        user_id = ""
        response = self.client.get_action(id, user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_action_list(self):
        action = ca_model.Action(
            "", "", "COMMAND", "", 0,
            ca_model.Command(
                None, "", "INDIVIDUAL", False, {}, "", ""
            )
        )
        ascending = False
        page_no = 1
        page_size = 10
        sort = "createTime"
        user_id = ""

        response = self.client.action_list(action, page_no, page_size, sort, ascending, user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_action_run(self):
        user_id = ''
        action = ca_model.Action(
            "c-4cMSvlmdfWp2GdA9"
        )
        parameter = {}
        target_selector = ca_model.TargetSelector("BCC", [])
        target_selector_type = "INSTANCES_LIST"
        targets = [ca_model.Target("BCC", "i-ZCHupg0z")]
        response = self.client.action_run(action, parameter, user_id, target_selector_type, targets, target_selector)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_action_run(self):
        user_id = ''
        id = 'r-raUPWwr933Liqe54'
        response = self.client.get_action_run(id, user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_action_run_list(self):
        action = ca_model.Action(
            "", "", "COMMAND"
        )
        ascending = False
        page_no = 1
        page_size = 10
        sort = "createTime"
        user_id = ""
        response = self.client.action_run_list(action, page_no, page_size, sort, ascending, user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_action_log(self):
        run_id = "r-raUPWwr933Liqe54"
        child_id = "d-7abflJHODABF"
        response = self.client.action_log(run_id, child_id, 1)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
