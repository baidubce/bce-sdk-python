"""
Samples for ca client.
"""
from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.ca.ca_client import CaClient
from baidubce.services.ca import ca_model
from sample.ca import ca_sample_conf

if __name__ == '__main__':

    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create ca client
    ca_client = CaClient(ca_sample_conf.config)

    # get_ca_agent_info
    try:
        instance_list = [
            ca_model.Instance("i-9y7wPdlG"),
            ca_model.Instance("i-ZCHupg0z")
        ]
        response = ca_client.batch_get_agent(instance_list)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_action
    try:
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
        response = ca_client.create_action(execution, user_id, action, targets, parameter, target_selector,
                                           target_selector_type)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_action
    try:
        id = "c-xadYvQ1FSA5viD4E"
        response = ca_client.delete_action(id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update_action
    try:
        action = ca_model.Action(
            "c-k7zXV794Jjz1WZC8", "", "COMMAND", "yyy-python-test-update", 60,
            ca_model.Command(
                "SHELL", "ls", "INDIVIDUAL", False, [], "root", "/home"
            )
        )
        execution = "SAVE"
        response = ca_client.update_action(action, execution)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_action
    try:
        id = "c-k7zXV794Jjz1WZC8"
        user_id = ""
        response = ca_client.get_action(id, user_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_action_list
    try:
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

        response = ca_client.action_list(action, page_no, page_size, sort, ascending, user_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # action_run
    try:
        user_id = ''
        action = ca_model.Action(
            "c-4cMSvlmdfWp2GdA9"
        )
        parameter = {}
        target_selector = ca_model.TargetSelector("BCC", [])
        target_selector_type = "INSTANCES_LIST"
        targets = [ca_model.Target("BCC", "i-ZCHupg0z")]
        response = ca_client.action_run(action, parameter, user_id, target_selector_type, targets, target_selector)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_action_run
    try:
        user_id = ''
        id = 'r-raUPWwr933Liqe54'
        response = ca_client.get_action_run(id, user_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    try:
        action = ca_model.Action(
            "", "", "COMMAND"
        )
        ascending = False
        page_no = 1
        page_size = 10
        sort = "createTime"
        user_id = ""
        response = ca_client.action_run_list(action, page_no, page_size, sort, ascending, user_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # action_log
    try:
        run_id = "r-raUPWwr933Liqe54"
        child_id = "d-7abflJHODABF"
        response = ca_client.action_log(run_id, child_id, 1)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)