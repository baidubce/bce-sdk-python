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
Samples for bmr client.
"""

import logging
import os
import sys
import time

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import bmr_sample_conf
from baidubce.services.bmr import bmr_client as bmr
from baidubce import exception as ex


logging.basicConfig(level=logging.DEBUG, filename='./bmr_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = bmr_sample_conf


def wait_for_cluster_ready(bmr_client, cluster_id):
    """
    wait for the cluster to be active.
    """
    try:
        retry_time = 0
        status = None
        while retry_time <= CONF.check_cluster_max_retry_time:
            response = bmr_client.get_cluster(new_cluster_id)
            status = response.status.state
            LOG.debug('check cluster %s: status %s' % (new_cluster_id, status))
            if status == 'Waiting':
                break
            LOG.debug('wait for cluster getting ready. at %d retry time.' % retry_time)
            retry_time += 1
            time.sleep(CONF.check_cluster_interval_sec)
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('get_cluster failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('get_cluster failed. Unknown exception: %s' % e)

    if retry_time > CONF.check_cluster_max_retry_time or status is None: 
        LOG.error('check cluster status failed. Skip following requests.')
        sys.exit(1)


if __name__ == '__main__':
    bmr_client = bmr.BmrClient(CONF.config)
    try:
        # list clusters
        LOG.debug('\n\n\nSample 1: LIST CLUSTERS\n\n\n')
        response = bmr_client.list_clusters(max_keys=5)
        print response.is_truncated, response.next_marker
        LOG.debug('list total %s clusters' % len(response.clusters))
        for cluster in response.clusters:
            LOG.debug('cluster: %s' % cluster)

        page = 1
        next_marker = None
        max_keys = 5
        is_truncated = True
        while is_truncated:
            response = bmr_client.list_clusters(marker=next_marker, max_keys=max_keys)
            LOG.debug('list %s clusters on Page %s' % (len(response.clusters), page))
            page += 1
            is_truncated = response.is_truncated
            next_marker = response.next_marker

        LOG.debug('\n\n\nSample 2: CREATE CLUSTER\n\n\n')
        new_cluster_id = None
        response = bmr_client.create_cluster(
            image_type='hadoop', 
            image_version='0.1.0',
            instance_groups=[
                bmr.instance_group(
                    group_type='Master',
                    instance_type='g.small',
                    instance_count=1,
                    name='ig-master'
                ),
                bmr.instance_group(
                    group_type='Core',
                    instance_type='g.small',
                    instance_count=2,
                    name='ig-core'
                )
            ],
            applications=[
                bmr.application(name='hive', version='0.13.0'),
                bmr.application(name='pig', version='0.11.0'),
                bmr.application(name='hbase', version='0.98.0',
                                properties={'backupLocation': 'bos://test/hbase_backup',
                                            'backupStartDateTime': '2015-08-18T23:00:00Z',
                                            'backupEnabled': 'true',
                                            'backupIntervalInMinutes': 300})
            ],
            auto_terminate=False,
            log_uri='bos://test01/cluster_logs/',
            name='python-sdk',
            steps=[
                bmr.step(
                    step_type='Java',
                    action_on_failure='Continue',
                    properties=bmr.java_step_properties(
                        'bos://bmr/samples/mapreduce/libs/hadoop-mapreduce-examples.jar',
                        'org.apache.hadoop.examples.WordCount',
                        'bos://bmr/samples/mapreduce/wordcount/hamlet.txt bos://test/output'
                    ),
                    name='sdk-job-00'
                )
            ])
        LOG.debug('create cluster response: %s' % response)
        new_cluster_id = response.cluster_id

        if new_cluster_id is None:
            LOG.error('failed to create cluster. Skip following requests.')
            sys.exit(1)

        # get cluster
        LOG.debug('\n\n\nSample 3: GET CLUSTER\n\n\n')
        response = bmr_client.get_cluster(new_cluster_id)
        status = response.status.state
        LOG.debug('check cluster %s: status %s' % (new_cluster_id, status))
        # wait for the cluster getting ready, then add steps to the cluster.
        wait_for_cluster_ready(bmr_client, new_cluster_id)

        # add steps
        LOG.debug('\n\n\nSample 4: ADD STEPS\n\n\n')

        steps=[
                bmr.step(
                    'Java',
                    'Continue',
                    bmr.java_step_properties(
                        'bos://benchmark/hadoop/hadoop-mapreduce-examples.jar',
                        'org.apache.hadoop.examples.WordCount',
                        'bos://helloworld/input/install.log bos://tester01/sdk/output_java/out1'
                    ),
                    'sdk-job-01'
                ),
                bmr.step(
                    'Streaming',
                    'Continue',
                    bmr.streaming_step_properties(
                        'bos://helloworld/input/install.log',
                        'bos://test/sdk/output_streaming/out1',
                        'cat'
                    ),
                    'sdk-job-02'
                ),
                bmr.step(
                    'Hive',
                    'Continue',
                    bmr.hive_step_properties(
                        'bos://chy3/hive/hql/hive_src.hql',
                        '--hivevar LOCAT=bos://chy3/hive/tables/src',
                        'bos://chy3/hive/data/hive_src.data',
                        'bos://tester01/sdk/output_hive/out1'
                    ),
                    'sdk-job-03'
                ),
                bmr.step(
                    'Pig',
                    'Continue',
                    bmr.pig_step_properties(
                        'bos://chy3/pig/script/pig_grep.pig',
                        input='bos://chy3/pig/data/pig_grep.data',
                        output='bos://tester01/sdk/output_pig/out1'
                    ),
                    'sdk-job-04'
                )
            ]
        response = bmr_client.add_steps(
            cluster_id=new_cluster_id,
            steps=steps
        )
        LOG.debug('add steps response: %s' % response)

        # list steps
        LOG.debug('\n\n\nSample 5: LIST STEPS\n\n\n')
        response = bmr_client.list_steps(new_cluster_id, max_keys=50)
        LOG.debug('list steps response: %s' % response)

        # get step
        steps = response.steps
        if steps is not None and len(steps) > 0:
            LOG.debug('\n\n\nSample 6: GET STEP\n\n\n')
            step_id = steps[0].id
            response = bmr_client.get_step(new_cluster_id, step_id)
            LOG.debug('get step response: %s' % response)

        # terminate cluster
        LOG.debug('\n\n\nSample 7: TERMINATE CLUSTER\n\n\n')
        response = bmr_client.terminate_cluster(new_cluster_id)
        LOG.debug('terminate cluster %s: status %s' % (new_cluster_id, response.status))
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
