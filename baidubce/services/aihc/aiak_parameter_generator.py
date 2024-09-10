# -*- coding: utf-8 -*-

import csv
import json
import sys
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# 获取配置信息, 从环境变量中获取,需要先在.env文件中设置环境变量
ak = os.getenv("AK")
sk = os.getenv("SK")
host = os.getenv("HOST")

# print(ak, sk, host)

# 指定文件路径
models_file_path = './aiak_dict/models.csv'
datasets_file_path = './aiak_dict/datasets.csv'
chain_info_template_path = './aiak_dict/chain_info_template.json'


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


def read_chain_info(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        return json.load(f)


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

    chain_info = read_chain_info(chain_info_template_path)
    # print(json.dumps(chain_info, indent=4, ensure_ascii=False))

    # chain_info['config_path'] = chain_job_config

    chain_info['api_config']['ak'] = ak
    chain_info['api_config']['sk'] = sk
    chain_info['api_config']['host'] = host

    ck_job = chain_info['jobs'][0]
    ck_job['jobSpec']['image'] = IMAGE
    ck_job['name'] = CK_JOB_NAME
    ck_job['jobSpec']['envs'] = [
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

    dp_job['jobSpec']['command'] = f'job2_{TRAINING_PHASE}_data_preprocess.sh'

    if TRAINING_PHASE == 'sft':
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


# =${DATA_PATH:-"/mnt/cluster/aiak-training-llm/dataset/sft_aplaca_zh_data.json"}

# =${DATA_CACHE_PATH:-"/mnt/cluster/aiak-training-llm/qwen2/sft_aplaca_zh_data_cache"}

# DATASET_CONFIG_PATH=${DATASET_CONFIG_PATH:-"/workspace/AIAK-Training-LLM/configs/sft_dataset_config.json"}

# =${TOKENIZER_PATH:-"/mnt/cluster/leoli/qwen/Qwen2-7B-HF"}

# =${CHECKPOINT_PATH:-"/mnt/cluster/leoli/qwen/Qwen2_7B_mcore_tp1pp1"}

# TENSORBOARD_PATH=${TENSORBOARD_PATH:-"/mnt/cluster/leoli/qwen/tensorboard-log/qwen2-7b-sft"}

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
        '/workspace/AIAK-Training-LLM/examples/'
        + MODEL_NAME.split("-")[0]
        + '/pretrain/pretrain_'
        + MODEL_NAME.replace("-", "_")
        + '.sh'
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
