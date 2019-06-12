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
import sys
import random
import string
import time

if sys.version_info[0] == 2 :
    reload(sys)
    sys.setdefaultencoding('utf-8')

import tsdb_sample_conf
from baidubce.exception import BceServerError
from baidubce.services.tsdb.tsdb_client import TsdbClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    __logger = logging.getLogger(__name__)

    ######################################################################################################
    #            create client samples
    ######################################################################################################
    
    # create a client, if you want to use https, you can setting it in tsdb_sample_conf
    tsdb_client = TsdbClient(tsdb_sample_conf.config)

    ######################################################################################################
    #            write operation samples
    ######################################################################################################

    # write single field
    datapoints = [{
        "metric": "wind",
        "tags": {
            "city": "ShangHai"
        },
        "field": "direction",
        "timestamp": 1531985379000,
        "type": "Long",
        "value": 1
    }]
    try:
        print(tsdb_client.write_datapoints(datapoints))
    except BaseException as e:
        print(e)

    # write multiple fields
    datapoints = [{
        "metric": "wind",
        "tags": {
            "city": "ShangHai"
        },
        "field": "direction",
        "timestamp": 1531985380000,
        "type": "Long",
        "value": 1
    }, {
        "metric": "wind",
        "tags": {
            "city": "ShangHai"
        },
        "field": "speed",
        "timestamp": 1531985380000,
        "type": "Double",
        "value": 4.5
    }]

    try:
        print(tsdb_client.write_datapoints(datapoints)) 
    except BaseException as e:
        print(e)

    # ######################################################################################################
    # #            query operation samples
    # ######################################################################################################

    # get metrics
    result = tsdb_client.get_metrics()
    print(result.metrics)

    # get fields
    result = tsdb_client.get_fields(b'wind')
    print(result.fields)

    # get tags
    result = tsdb_client.get_tags(b'wind')
    print(result.tags)

    #single field query datapoints
    query_list = [{
        "metric": "wind",
        "field": "direction",
        "filters": {
            "start": 1531985370000,
            "end": 1531985400000,
            "tags": {
                "city": ["ShangHai"]
            },
            "value": ">= 0"
        },
        "groupBy": [{
            "name": "Tag",
            "tags": ["city"]
        }],
        "limit": 1000,
        "aggregators": [{
            "name": "Sum",
            "sampling": "10 minutes"
        }]
    }]
    result = tsdb_client.get_datapoints(query_list)
    print(result.results)

    # multiple fields query datapoints
    query_list = [{
        "metric": "wind",
        "fields": ["direction", "speed"],
        "filters": {
            "start": 1531985370000,
            "end": 1531985400000,
            "tags": {
                "city": ["ShangHai"]
            },
            "value": ">= 0"
        },
        "groupBy": [{
            "name": "Tag",
            "tags": ["city"]
        }],
        "limit": 1000,
        "aggregators": [{
            "name": "Sum",
            "sampling": "10 minutes"
        }]
    }]
    result = tsdb_client.get_datapoints(query_list)
    print(result.results)

    # query datapoints with fill
    query_list = [{
        "metric": "wind",
        "fields": ["direction", "speed"],
        "filters": {
            "start": 1531985370000,
            "end": 1532985370000,
            "tags": {
                "city": ["ShangHai"]
            },
            "value": ">= 0"
        },
        "fill": {
            "type": "Linear",
            "interval": "1 day",
            "maxWriteInterval": "30 minutes"
        },
        "groupBy": [{
            "name": "Tag",
            "tags": ["city"]
        }],
        "limit": 1000,
        "aggregators": [{
            "name": "Sum",
            "sampling": "10 minutes"
        }]
    }]

    result = tsdb_client.get_datapoints(query_list)
    print(result.results)

    # query datapoints with partition page
    query_list = [{
        "metric": "wind",
        "field": "direction",
        "filters": {
            "start": 1531985300000,
            "end": 1531985400000,
            "tags": {
                "city": ["ShangHai"]
            }
        },
        "limit": 1
    }]
    count = 0
    while True:
        count += 1
        if len(query_list) > 0:
            result = tsdb_client.get_datapoints(query_list)
            print(count, result.results)
        else:
            print('end query')
            break
        next_query = []
        for i in range(len(query_list)):
            if result.results[i].truncated:
                query_list[i]['marker'] = result.results[i].next_marker
                next_query.append(query_list[i])
        query_list = next_query

    # query datapoints with sql
    sql = b"select * from wind" 
    result = tsdb_client.get_rows_with_sql(sql)
    print(result)

    # generate pre signed url sample
    timestamp = int(time.time())
    per_signed_url = tsdb_client.generate_pre_signed_url(query_list,
            timestamp=timestamp, expiration_in_seconds=1800)
    print(per_signed_url)

    # generate pre signed url with sql sample
    sql = b"select * from wind"
    timestamp = int(time.time())
    per_signed_url_sql = tsdb_client.generate_pre_signed_url_with_sql(sql,
            timestamp=timestamp, expiration_in_seconds=1800)
    print(per_signed_url_sql)

    # write datapoint don't use gzip compress
    response = tsdb_client.write_datapoints(datapoints, use_gzip=False)
    print(response)

