# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for tsdb client.
"""

import os
import random
import string
import time
import sys

if sys.version_info[0] == 2 :
    reload(sys)
    sys.setdefaultencoding('utf-8')

import tsdb_admin_sample_conf
from baidubce.exception import BceServerError
from baidubce.services.tsdb.tsdb_admin_client import TsdbAdminClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    __logger = logging.getLogger(__name__)

    ######################################################################################################
    #            create tsdb admin client samples
    ######################################################################################################
    
    # create a client, if you want to use https, you can setting it in tsdb_sample_conf
    tsdb_admin_client = TsdbAdminClient(tsdb_admin_sample_conf.config)

    # create database sample
    database_name = b'pythonsdksample'  # instance name
    description = b'descriptionchen'    # optional
    ingest_datapoints_monthly = 1  # write quota
    store_bytes_quota = 0 # optional, byte quota
    purchase_length = 1 # unit: month
    coupon_name = b'xxxxxxxxxx'    # optional, use the coupon to purchase
    
    client_token = b'testxx' # when you retry, please use the same client_token
    try:
        result = tsdb_admin_client.create_database(
                client_token=client_token,
                description=description,
                database_name=database_name,
                ingest_datapoints_monthly=ingest_datapoints_monthly,
                purchase_length=purchase_length,
                store_bytes_quota=store_bytes_quota,
                coupon_name=coupon_name)
        print(result)
    except BaseException as e:
        print(e)

    # delete database
    database_id = b'tsdb-xxxxxxxxxxx'
    try:
        response = tsdb_admin_client.delete_database(database_id)
        print(response)
    except BaseException as e:
        print(e)

    # get database info
    database_id = b'tsdb-xxxxxxxxxxx'
    print(tsdb_admin_client.get_database(database_id))

    # get all databases
    result = tsdb_admin_client.get_all_databases()
    print(result)

    
        