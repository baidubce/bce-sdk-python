import sys
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.autoscaling import as_client, as_model

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://as.bj.baidubce.com'
AK = b''
SK = b''
group_id = "asg-mPWF****"


class TestAsClient(unittest.TestCase):
    """
    Test class for bcm sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = as_client.AsClient(config)

    def test_get_group_list(self):
        keyword = "djw-test"
        keyword_type = "groupName"
        response = self.client.get_as_group_list(page_no=1, page_size=1000, keyword=keyword, keyword_type=keyword_type,
                                                 order="",
                                                 order_by=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_group_detail(self):
        group_id = "asg-FKsD6xmT"
        response = self.client.get_as_group_detail(group_id=group_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_group_node_list(self):
        group_id = "asg-FKsD6xmT"
        response = self.client.get_as_group_node_list(group_id=group_id, page_no=1, page_size=1000, keyword="",
                                                      keyword_type="",
                                                      order="",
                                                      order_by=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_group(self):
        group_ids = [
            "asg-EDICcmzA"
        ]
        response = self.client.delete_group(group_ids=group_ids)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_group(self):
        group_name = "yyy-test-python2"
        config = as_model.Config(0, -1, 200, 300)
        health_check = as_model.HealthCheck(15, 300)
        shrinkage_strategy = "Earlier"
        zone_info = [as_model.ZoneInfo("zoneA", "sbn-8mghgkzs3ch9")]
        tags = [as_model.Tag("默认项目", "")]
        assign_tag_info = as_model.AssignTagInfo(False, tags)
        nodes = [as_model.Node(8, 32, "enhanced_ssd_pl1",
                               20, 13, "bidding",
                               "24e80264-8a6d-49c1-b415-116d9cf38a75", "custom", "linux",
                               "g-yhryv5vyapb4", "bcc.g4.c8m32", [], "", 1,
                               "[{\"zone\":\"zoneA\",\"subnetId\":\"sbn-8mghgkzs3ch9\","
                               "\"subnetName\":\"lyz2（192.168.0.0/24）\","
                               "\"subnetUuid\":\"5911e194-528f-4153-99a3-3c63b7bc7d7c\"}]",
                               1, "custom", 0.0264944, [])]
        eip = as_model.Eip(False, 0, "")
        billing = as_model.Billing("bidding")
        cmd_config = as_model.CmdConfig(False, "Proceed", "",
                                        3600, True, False,
                                        "Proceed", "", 3600, True)
        bcc_name_config = as_model.BccNameConfig("", "")
        response = self.client.create_group(group_name=group_name, config=config, health_check=health_check,
                                            shrinkage_strategy=shrinkage_strategy, zone_infos=zone_info,
                                            assign_tag_info=assign_tag_info,
                                            node_list=nodes, eip=eip, billing=billing, cmd_config=cmd_config,
                                            bcc_name_config=bcc_name_config)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_detach_node(self):
        """
        test detach node
        """
        response = self.client.detach_node(group_id=group_id, nodes=["i-mPkY5ZG5"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_rule(self):
        """
        test create rule
        """
        response = self.client.create_rule(rule_name="testRule",
                                           group_id=group_id,
                                           rule_type="PERIOD",
                                           action_type="INCREASE",
                                           action_num=1,
                                           cooldown_in_sec=300,
                                           state="ENABLE",
                                           period_type="WEEK",
                                           period_start_time="2023-12-11T11:00:00Z",
                                           period_end_time="2023-12-21T11:00:00Z",
                                           cron_time="12:30",
                                           period_value=2)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_rule(self):
        """
        test update rule
        """
        response = self.client.update_rule(rule_id="asrule-u1gUQ2Zw",
                                           rule_name="testRule_update",
                                           group_id=group_id,
                                           rule_type="PERIOD",
                                           action_type="INCREASE",
                                           action_num=1,
                                           cooldown_in_sec=300,
                                           state="ENABLE",
                                           period_type="WEEK",
                                           period_start_time="2023-12-11T11:00:00Z",
                                           period_end_time="2023-12-21T11:00:00Z",
                                           cron_time="12:40",
                                           period_value=2
                                           )
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_rule(self):
        """
        test get rule
        """
        response = self.client.get_rule(rule_id="asrule-u1gUQ2Zw")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_rule(self):
        """
        test list rule
        """
        response = self.client.list_rule(group_id=group_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_rule(self):
        """
        test delete rule
        """
        response = self.client.delete_rule(rule_ids=["asrule-u1gUQ2Zw"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBcmClient("test_get_metric_data"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
