# -*- coding: utf-8 -*-
import sys
import json
import os
import time
import logging
from baidubce.services.aihc.aihc_client import AIHCClient

import baidubce.protocol
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


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


def create_ai_job(api_config, resourcePoolId, payload):
    client_token = 'test-aihc-' + str(int(time.time()))
    logging.info('client_token: %s', client_token)

    config = BceClientConfiguration(
        credentials=BceCredentials(api_config['ak'], api_config['sk']),
        endpoint=api_config['host'],
        protocol=baidubce.protocol.HTTPS
    )

    aihc_client = AIHCClient(config)
    return aihc_client.create_aijob(
        client_token=client_token,
        resourcePoolId=resourcePoolId,
        payload=payload
    )


def create_job_chain(config_file=None, index=None):
    args = sys.argv[1:]
    if config_file is None:
        if len(args) < 1:
            logging.error("Usage: python job_chain.py <config_file> [index]")
            return
        else:
            config_file = args[0]
    if index is None:
        try:
            index = int(args[1]) if len(args) > 1 else 0
        except ValueError:
            logging.error("Invalid index value.")

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

        result = create_ai_job(api_config, resourcePoolId, cur_job_info)
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


if __name__ == "__main__":
    create_job_chain()
