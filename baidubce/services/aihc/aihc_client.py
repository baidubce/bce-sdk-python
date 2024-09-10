# Copyright 2014 Baidu, Inc.

"""
This module provides a client class for TSDB.
"""

import copy
import json
import os
import logging
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services.aihc import aihc_handler
from baidubce.services.aihc import generate_aiak_parameter


# _logger = logging.getLogger(__name__)
# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"File {config_file} not found.")
    with open(config_file, 'r') as f:
        return json.load(f)


def validate_index(index, jobs_count):
    if index < 0 or index >= jobs_count:
        raise IndexError(f"Index {index} is out of range.")


def build_command(job_info, config_dir, scrips_path, config_path,
                  index, jobs_count):
    command = job_info['jobSpec']['command']
    if (command.endswith('.sh') and
        len(command.split('.')) == 2 and
            command.startswith('bash') is not True):
        command_path = os.path.join(config_dir, command)
        if not os.path.exists(command_path):
            raise FileNotFoundError(f"File {command_path} not found.")

        with open(command_path, 'r') as f:
            command = f.read()

    if index != jobs_count - 1:
        command += (
            '\n' + 'echo "job_chain:The previous task has been completed."'
            '\n' + 'pip install future'
            '\n' + 'pip install pycryptodome'
            '\n' + 'pip install bce-python-sdk-next'
            '\n' + 'echo "job_chain:Next job is to be continued..."'
        )
        next_command = f'python {scrips_path} {config_path} {index + 1}'
        command += f'\n{next_command}'

    return command


class AIHCClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def generate_aiak_parameter(self, chain_job_config=None, aiak_job_config=None):
        return generate_aiak_parameter.generate_aiak_parameter(chain_job_config, aiak_job_config)

    def create_aijob(
            self,
            client_token,
            resourcePoolId,
            payload):
        # print('create_aijob is called')
        path = b"/api/v1/aijobs"
        params = {
            "clientToken": client_token,
            "resourcePoolId": resourcePoolId
        }

        body = json.dumps(payload).encode('utf-8')
        return self._send_request(http_methods.POST, path=path, body=body,
                                  params=params,
                                  body_parser=aihc_handler.parse_json)

    def create_job_chain(self, config_file=None, index=None):
        try:
            job_info = load_config(config_file)
            jobs = job_info['jobs']
            api_config = job_info['api_config']
            resourcePoolId = job_info['resourcePoolId']
            scrips_path = job_info['scrips_path']
            config_path = job_info['config_path']

            validate_index(index, len(jobs))

            config_dir = os.path.dirname(config_file)
            command = build_command(jobs[index], config_dir, scrips_path,
                                    config_path, index, len(jobs))
            jobs[index]['jobSpec']['command'] = command

            logging.info("Job info at index retrieved successfully.")
            logging.info(json.dumps(jobs[index]))

            logging.info("Creating AI job using openapi...")

            cur_job_info = jobs[index]

            result = self.create_ai_job(api_config, resourcePoolId, cur_job_info)
            tasks_url = 'https://console.bce.baidu.com/aihc/tasks'
            print('====================================\n')
            logging.info('任务创建结果: %s', result)
            logging.info('查看任务列表: https://console.bce.baidu.com/aihc/tasks')
            print('\n====================================')
            return {
                result: result,
                tasks_url: tasks_url
            }
        except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
            logging.error("Error: %s", e)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)

    def delete_aijob(self, aijob_id):
        """
        delete job

        :param job_id: job id to delete
        :type job_id: string

        :return: bce_request_id
        :rtype: baidubce.bce_response.BceResponses
        """
        path = b'/api/v1/aijobs/' + aijob_id
        return self._send_request(http_methods.DELETE, path,
                                  body_parser=aihc_handler.parse_json)

    def get_aijob(self, aijob_id):
        """
        get aijob

        :param aijob_id: aijob id to delete
        :type aijob_id: string

        :return: aijob info
        :rtype: baidubce.bce_response.BceResponse
        """

        path = b'/api/v1/aijobs/' + aijob_id
        return self._send_request(http_methods.GET, path,
                                  body_parser=aihc_handler.parse_json)

    def get_all_aijobs(self, resourcePoolId):
        """
        get all aijobs

        :return: aijob dict
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {
            "resourcePoolId": resourcePoolId
        }
        path = b'/api/v1/aijobs'
        return self._send_request(http_methods.GET, path,
                                  params=params,
                                  body_parser=aihc_handler.parse_json)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, path,
            body=None,
            params=None,
            headers=None,
            config=None,
            body_parser=None):
        config = self._merge_config(config)
        if headers is None:
            headers = {http_headers.CONTENT_TYPE: http_content_types.JSON}
        if body_parser is None:
            body_parser = handler.parse_json
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)
