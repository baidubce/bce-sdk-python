# Copyright 2014 Baidu, Inc.

"""
This module provides a client class for TSDB.
"""

import copy
import json
import os
import time
import logging
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services.aihc import aihc_handler
from baidubce.services.aihc import chain_info_temp

import csv
import sys

cur_path = os.path.dirname(os.path.realpath(__file__))
# 指定文件路径
models_file_path = f'{cur_path}/aiak_dict/models.csv'
datasets_file_path = f'{cur_path}/aiak_dict/datasets.csv'

# _logger = logging.getLogger(__name__)
# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_models_from_csv(file_path):
    models = {}
    # 读取 CSV 文件
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # header = next(csv_reader)
        # print(header)
        for row in csv_reader:
            # print(row)
            if row[1] != '' and row[0] != '模型名称':
                models[row[1]] = [row[3], row[4], row[5]]

    return models


def get_datasets_from_csv(file_path):
    datasets = {}
    # 读取 CSV 文件
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # header = next(csv_reader)
        # print(header)
        for row in csv_reader:
            if row[1] != '' and row[0] != '名称':
                datasets[row[0]] = row[1]

    return datasets


def get_command_from_sh(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def write_chain_info(ak, sk, host):
    chain_info_temp.chain_info_temp['jobs'][0]['jobSpec']['envs'] = [
        {
            "key": "AK",
            "value": ak
        },
        {
            "key": "SK",
            "value": sk
        },
        {
            "key": "HOST",
            "value": host
        }]
    chain_info_temp.chain_info_temp['jobs'][1]['jobSpec']['envs'] = [
        {
            "key": "AK",
            "value": ak
        },
        {
            "key": "SK",
            "value": sk
        },
        {
            "key": "HOST",
            "value": host
        }]


def read_chain_info():
    return chain_info_temp.chain_info_temp


def generate_aiak_parameter(chain_job_config=None, aiak_job_config=None):

    args = sys.argv[1:]
    if chain_job_config is None or aiak_job_config is None:
        if len(args) < 2:
            print("Usage: python job_chain.py <config_file> [index]")
            return
        else:
            chain_job_config = args[0]
            aiak_job_config = args[1]

    with open(aiak_job_config, mode='r', encoding='utf-8') as file:
        aiak_job_info = json.load(file)
        # print(json.dumps(aiak_job_info, indent=4, ensure_ascii=False))
        # AIAK任务参数
        VERSION = aiak_job_info['VERSION']
        DATASET_NAME = aiak_job_info['DATASET_NAME']
        MODEL_NAME = aiak_job_info['MODEL_NAME']
        if aiak_job_info['TP'] and aiak_job_info['PP']:
            TP = aiak_job_info['TP']
            PP = aiak_job_info['PP']
        JSON_KEYS = aiak_job_info['JSON_KEYS']
        IMAGE = aiak_job_info['IMAGE']
        TRAINING_PHASE = aiak_job_info['TRAINING_PHASE']
        REPLICAS = aiak_job_info['REPLICAS']
        MOUNT_PATH = aiak_job_info['MOUNT_PATH']

    models = get_models_from_csv(models_file_path)
    # print(json.dumps(models, indent=4, ensure_ascii=False))
    MODEL_BOS_PATH = models[MODEL_NAME][0]
    TP = models[MODEL_NAME][1]
    PP = models[MODEL_NAME][2]
    if aiak_job_info['TP'] and aiak_job_info['PP']:
        TP = aiak_job_info['TP']
        PP = aiak_job_info['PP']
    else:
        TP = models[MODEL_NAME][1]
        PP = models[MODEL_NAME][2]
    # print('MODEL_BOS_PATH：', MODEL_BOS_PATH)

    save_path = '/'.join(MODEL_BOS_PATH.split('/')[2:])

    LOAD = f'{MOUNT_PATH}/models/{MODEL_NAME}/hf/{save_path}'
    # print('LOAD：', LOAD)

    TOKENIZER_PATH = LOAD
    # print('TOKENIZER_PATH：', TOKENIZER_PATH)

    CHECKPOINT_PATH = f'{MOUNT_PATH}/models/{MODEL_NAME}/mcore/{save_path}/tp{TP}_pp{PP}'
    # print('CHECKPOINT_PATH：', CHECKPOINT_PATH)

    datasets = get_datasets_from_csv(datasets_file_path)
    # print(json.dumps(datasets, indent=4, ensure_ascii=False))
    DATASET_BOS_PATH = datasets[DATASET_NAME]
    # print('DATASET_BOS_PATH：', DATASET_BOS_PATH)

    save_path = '/'.join(DATASET_BOS_PATH.split('/')[2:])
    INPUT_DATA = f'{MOUNT_PATH}/datasets/{save_path}'
    # print('INPUT_DATA_PATH：', INPUT_DATA)

    save_path = '.'.join(INPUT_DATA.split('.')[0:-1])

    DATA_CACHE_PATH = f'{save_path}_cache'

    # INPUT_DATA去掉最后的文件名后缀
    OUTPUT_PREFIX = save_path
    # OUTPUT_PREFIX = INPUT_DATA

    # print('OUTPUT_PREFIX：', OUTPUT_PREFIX)

    DATA_PATH = f'{OUTPUT_PREFIX}_text_document'
    # print('DATA_PATH：', DATA_PATH)

    # CHECKPOINT_SAVE_PATH = f'{CHECKPOINT_PATH}/{VERSION}'

    CK_JOB_NAME = f'{TRAINING_PHASE}-{MODEL_NAME}-ck2mc-{VERSION}'
    DP_JOB_NAME = f'{TRAINING_PHASE}-{MODEL_NAME}-dp-{VERSION}'
    TRAIN_JOB_NAME = f'{TRAINING_PHASE}-{MODEL_NAME}-train-{VERSION}'

    chain_info = read_chain_info()
    # print(json.dumps(chain_info, indent=4, ensure_ascii=False))

    ck_job = chain_info['jobs'][0]
    ck_job['jobSpec']['image'] = IMAGE
    ck_job['name'] = CK_JOB_NAME
    sh_path = f'{cur_path}/aiak_dict/job1_convert_checkpoint.sh'

    ck_job['jobSpec']['command'] = get_command_from_sh(sh_path)
    envs = ck_job['jobSpec']['envs']
    ck_job['jobSpec']['envs'] = envs + [
        {
            'name': 'MODEL_BOS_PATH',
            'value': MODEL_BOS_PATH
        },
        {
            'name': 'MODEL_NAME',
            'value': MODEL_NAME
        },
        {
            'name': 'TP',
            'value': TP
        },
        {
            'name': 'PP',
            'value': PP
        },
        {
            'name': 'LOAD',
            'value': LOAD
        },
        {
            'name': 'SAVE',
            'value': CHECKPOINT_PATH
        }
    ]

    # print(json.dumps(ck_job, indent=4, ensure_ascii=False))

    dp_job = chain_info['jobs'][1]
    dp_job['jobSpec']['image'] = IMAGE
    dp_job['name'] = DP_JOB_NAME

    sh_path = f'{cur_path}/aiak_dict/job2_{TRAINING_PHASE}_data_preprocess.sh'

    dp_job['jobSpec']['command'] = get_command_from_sh(sh_path)
    envs = dp_job['jobSpec']['envs']
    if TRAINING_PHASE == 'sft':
        dp_job['jobSpec']['envs'] = envs + [
            {
                'name': 'DATASET_BOS_PATH',
                'value': DATASET_BOS_PATH
            },
            {
                'name': 'TOKENIZER_PATH',
                'value': TOKENIZER_PATH
            },
            {
                'name': 'INPUT_DATA',
                'value': INPUT_DATA
            },
            {
                'name': 'OUTPUT_PATH',
                'value': OUTPUT_PREFIX
            },
            {
                'name': 'CHAT_TEMPLATE',
                'value': (MODEL_NAME.split('-')[0]
                          if MODEL_NAME.startswith('qwen') is not True
                          else 'qwen')
            }
        ]
    else:
        dp_job['jobSpec']['envs'] = [
            {
                'name': 'DATASET_BOS_PATH',
                'value': DATASET_BOS_PATH
            },
            {
                'name': 'TOKENIZER_PATH',
                'value': TOKENIZER_PATH
            },
            {
                'name': 'INPUT_DATA',
                'value': INPUT_DATA
            },
            {
                'name': 'OUTPUT_PREFIX',
                'value': OUTPUT_PREFIX
            },
            {
                'name': 'JSON_KEYS',
                'value': JSON_KEYS
            }
        ]

    # print(json.dumps(dp_job, indent=4, ensure_ascii=False))

    train_job = chain_info['jobs'][2]
    train_job['jobSpec']['image'] = IMAGE
    train_job['name'] = TRAIN_JOB_NAME

    if TRAINING_PHASE == 'sft':
        train_job['jobSpec']['envs'] = [
            {
                'name': 'CUDA_DEVICE_MAX_CONNECTIONS',
                'value': '1'
            },
            {
                'name': 'DATA_PATH',
                'value': INPUT_DATA
            },
            {
                'name': 'DATA_CACHE_PATH',
                'value': DATA_CACHE_PATH
            },
            {
                'name': 'TOKENIZER_PATH',
                'value': TOKENIZER_PATH
            },
            {
                'name': 'CHECKPOINT_PATH',
                'value': CHECKPOINT_PATH
            },
        ]

    else:
        train_job['jobSpec']['envs'] = [
            {
                "name": "CUDA_DEVICE_MAX_CONNECTIONS",
                "value": "1"
            },
            {
                'name': 'DATA_PATH',
                'value': DATA_PATH
            },
            {
                'name': 'TOKENIZER_PATH',
                'value': TOKENIZER_PATH
            },
            {
                'name': 'CHECKPOINT_PATH',
                'value': CHECKPOINT_PATH
            }
        ]

    SH_PATH = (
        f'/workspace/AIAK-Training-LLM/examples/{MODEL_NAME.split("-")[0]}/pretrain/pretrain_{MODEL_NAME.replace("-", "_")}.sh'
    )
    if TRAINING_PHASE == 'sft':
        SH_PATH = '/workspace/AIAK-Training-LLM/examples/' + \
            MODEL_NAME.split('-')[0] \
            + f'/finetuning/sft_{MODEL_NAME.replace("-", "_")}.sh'
    # print('SH_PATH：', SH_PATH)

    train_job['jobSpec']['command'] = f'bash {SH_PATH}'
    train_job['jobSpec']['replicas'] = int(REPLICAS)

    # print(json.dumps(train_job, indent=4, ensure_ascii=False))

    chain_info['jobs'][0] = ck_job
    chain_info['jobs'][1] = dp_job
    chain_info['jobs'][2] = train_job

    print(chain_info)
    # print(json.dumps(chain_info, indent=4, ensure_ascii=False))

    chain_job_config = f'{chain_job_config}/{TRAIN_JOB_NAME}.json'
    with open(chain_job_config, 'w') as f:
        json.dump(chain_info, f, indent=4, ensure_ascii=False)

    run_command = f'python job_chain.py {chain_job_config}'
    print('=============================\n')
    print('任务配置信息：', json.dumps(aiak_job_info, ensure_ascii=False))
    print('任务配置文件已生成：', chain_job_config)
    print('启动任务：', run_command)
    print('\n=============================')

    return {
        chain_job_config: chain_job_config,
        run_command: run_command
    }


def load_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"File {config_file} not found.")
    with open(config_file, 'r') as f:
        return json.load(f)


def validate_index(index, jobs_count):
    if index < 0 or index >= jobs_count:
        raise IndexError(f"Index {index} is out of range.")


# config_dir去掉，相应的看sh脚本如何传递参数
def build_command(jobs, config_dir,
                  index):
    job_info = jobs[index]
    jobs_count = len(jobs)
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
        jobs_str = json.dumps(jobs)

        # 保存配置文件
        command_save_chain_info = f"cat << 'EOF' > chain_info.json\n{jobs_str}\nEOF"

        command_pip_install = r"""
echo "job_chain:The previous task has been completed."
pip install future
pip install pycryptodome
pip install bce-python-sdk-next
pip install python-dotenv
echo "job_chain:Next job is to be continued..."
"""

        with open(f'{cur_path}/job_chain.py', 'r') as f:
            py_str = f.read()

        command_save_py = f"cat << 'EOF' > job_chain.py\n{py_str}\nEOF"
        command_call_py = f'python job_chain.py chain_info.json {index + 1}'

        command += f'{command_save_chain_info}\n{command_pip_install}\n{command_save_py}\n{command_call_py}'

    return command


class AIHCClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def generate_aiak_parameter(self, chain_job_config=None, aiak_job_config=None):
        ak = self.config.credentials.access_key_id.decode('utf-8')
        sk = self.config.credentials.secret_access_key.decode('utf-8')
        host = self.config.endpoint.decode('utf-8')
        write_chain_info(ak, sk, host)
        # print(ak, sk, host)
        return generate_aiak_parameter(chain_job_config, aiak_job_config)

    def create_job_chain(self, config_file=None, index=None):
        # 接收参数或配置文件路径
        try:
            job_info = load_config(config_file)
            jobs = job_info['jobs']
            resourcePoolId = job_info['resourcePoolId']

            validate_index(index, len(jobs))

            config_dir = os.path.dirname(config_file)
            command = build_command(jobs, config_dir,
                                    index)
            jobs[index]['jobSpec']['command'] = command

            logging.info("Job info at index retrieved successfully.")
            logging.info(json.dumps(jobs[index]))

            logging.info("Creating AI job using openapi...")

            cur_job_info = jobs[index]
            client_token = 'test-aihc-' + str(int(time.time()))
            logging.info('client_token: %s', client_token)

            result = self.create_aijob(client_token=client_token,
                                       resourcePoolId=resourcePoolId,
                                       payload=cur_job_info)
            tasks_url = 'https://console.bce.baidu.com/aihc/tasks'
            print('====================================\n')
            print('任务创建结果: ', result)
            print('查看任务列表: https://console.bce.baidu.com/aihc/tasks')
            print('\n====================================')
            return {
                result: result,
                tasks_url: tasks_url
            }
        except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
            logging.error("Error: %s", e)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)

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
