"""
Samples for as client.
"""

from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.autoscaling import as_model
from baidubce.services.autoscaling.as_client import AsClient
from sample.autoscaling import as_sample_conf

if __name__ == '__main__':

    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create autoscaling client
    as_client = AsClient(as_sample_conf.config)

    # get_as_group_list
    try:
        keyword = "djw-test"
        keyword_type = "groupName"
        response = as_client.get_as_group_list(page_no=1, page_size=1000, keyword=keyword, keyword_type=keyword_type,
                                               order="", order_by=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_as_group_detail
    try:
        group_id = "asg-FKsD6xmT"
        response = as_client.get_as_group_detail(group_id=group_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_as_group_node_list
    try:
        group_id = "asg-FKsD6xmT"
        response = as_client.get_as_group_node_list(group_id=group_id, page_no=1, page_size=1000, keyword="",
                                                    keyword_type="",
                                                    order="",
                                                    order_by=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_group
    try:
        group_ids = [
            "asg-EDICcmzA"
        ]
        response = as_client.delete_group(group_ids=group_ids)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_group
    try:
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
        response = as_client.create_group(group_name=group_name, config=config, health_check=health_check,
                                          shrinkage_strategy=shrinkage_strategy, zone_infos=zone_info,
                                          assign_tag_info=assign_tag_info,
                                          node_list=nodes, eip=eip, billing=billing, cmd_config=cmd_config,
                                          bcc_name_config=bcc_name_config)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

# detach_node
    try:
        response = as_client.detach_node(group_id="asg-mPWF****", nodes=["i-mPkY****"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create as rule
    try:
        response = as_client.create_rule(rule_name="testRule",
                                         group_id="asg-mPWF****",
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
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update as rule
    try:
        response = as_client.update_rule(rule_id="asrule-u1gU****",
                                         rule_name="testRule_update",
                                         group_id="asg-mPWF****",
                                         rule_type="PERIOD",
                                         action_type="INCREASE",
                                         action_num=1,
                                         cooldown_in_sec=300,
                                         state="ENABLE",
                                         period_type="WEEK",
                                         period_start_time="2023-12-11T11:00:00Z",
                                         period_end_time="2023-12-21T11:00:00Z",
                                         cron_time="12:40",
                                         period_value=2)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get as rule
    try:
        response = as_client.get_rule(rule_id="asrule-u1gU****")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list as rule
    try:
        response = as_client.list_rule(group_id="asg-mPWF****")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete as rule
    try:
        response = as_client.delete_rule(rule_ids=["asrule-u1gU****"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

   # get site once records
    try:
        group_id = "asg-mPWFLu1E"
        res = as_client.get_records(group_id)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # exec rule
    try:
        group_id = "asg-mPWFLu1E"
        rule_id = "asrule-u1gUQ2Zw"
        res = as_client.exec_rule(group_id, rule_id)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # scaling up
    try:
        group_id = "asg-mPWFLu1E"
        node_count = 2
        zone = ["cn-bj-a"]
        res = as_client.scaling_up(group_id, node_count, zone)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # scaling down
    try:
        nodes = ["i-HJEyMtLv"]
        res = as_client.scaling_down("asg-mPWFLu1E", nodes)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    # attach node
    try:
        nodes = ["i-HJEyMtLv"]
        res = as_client.attach_node("asg-mPWFLu1E", nodes)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    # adjust node
    try:
        res = as_client.adjust_node("asg-mPWFLu1E", 1)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)