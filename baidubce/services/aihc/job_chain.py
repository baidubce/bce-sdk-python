# -*- coding: utf-8 -*-
import sys
import os
import time
from baidubce.services.aihc.aihc_client import AIHCClient
import baidubce.protocol
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from dotenv import load_dotenv

load_dotenv()

ak = os.getenv("AK") if os.getenv("AK") else ''
sk = os.getenv("SK") if os.getenv("SK") else ''
host = os.getenv("HOST") if os.getenv("HOST") else ''


def create_job_chain(config_file=None, index=None):
    args = sys.argv[1:]
    if config_file is None:
        if len(args) < 1:
            print("Usage: python job_chain.py <config_file> [index]")
            return
        else:
            config_file = args[0]
    if index is None:
        try:
            index = int(args[1]) if len(args) > 1 else 0
        except ValueError:
            print("Invalid index value.")

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"File {config_file} not found.")

    client_token = 'test-aihc-' + str(int(time.time()))
    print('client_token: ', client_token)
    config = BceClientConfiguration(
        credentials=BceCredentials(ak, sk),
        endpoint=host,
        protocol=baidubce.protocol.HTTPS
    )

    aihc_client = AIHCClient(config)
    chain_job_info = aihc_client.create_job_chain(config_file, index)
    print('chain_job_info: ', chain_job_info)
    return chain_job_info


if __name__ == "__main__":
    create_job_chain()