# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for BMR.
"""

import copy
import logging
import json
import sys


from baidubce.auth import bce_v1_signer
from baidubce import bce_base_client
from baidubce import compat
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required
from baidubce.utils import aes128_encrypt_16char_key


_logger = logging.getLogger(__name__)

if sys.version_info[0] == 2:
    value_type = (str, unicode)
else:
    value_type = (str, bytes)


class BmrClient(bce_base_client.BceBaseClient):
    """
    Bmr sdk client
    """

    prefix = '/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    @required(image_type=value_type,
              image_version=value_type,
              instance_groups=list)
    def create_cluster(self,
                       image_type,
                       image_version,
                       instance_groups,
                       client_token=None,
                       applications=None,
                       auto_terminate=None,
                       log_uri=None,
                       name=None,
                       steps=None,
                       service_ha_enabled=None,
                       safe_mode_enabled=None,
                       admin_pass=None,
                       vpc_id=None,
                       subnet_id=None,
                       security_group=None,
                       availability_zone=None,
                       templateType=None):
        """
        Create cluster

        :param image_type: the type of virtual machine image
        :type image_type: string

        :param image_version: the version of virtual machine image
        :type image_version: string

        :param instance_groups: instance groups for cluster
        :type instance_groups: array

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster'
        params = None
        if client_token is not None:
            params = {
                'clientToken': client_token
            }
        body = {
            'imageType': compat.convert_to_string(image_type),
            'imageVersion': compat.convert_to_string(image_version),
            'instanceGroups': instance_groups
        }
        if applications is not None:
            body['applications'] = applications
        if auto_terminate is not None:
            body['autoTerminate'] = auto_terminate
        if name is not None:
            body['name'] = name
        if log_uri is not None:
            body['logUri'] = log_uri
        if steps is not None:
            body['steps'] = steps
        if service_ha_enabled is not None:
            body['serviceHaEnabled'] = service_ha_enabled
        if safe_mode_enabled is not None:
            body['safeModeEnabled'] = safe_mode_enabled
        if admin_pass is not None and self.config is not None:
            secret_access_key = self.config.credentials.secret_access_key
            body['adminPassword'] = aes128_encrypt_16char_key(admin_pass, secret_access_key)
        if vpc_id is not None:
            body['vpcId'] = vpc_id
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group is not None:
            body['securityGroup'] = security_group
        if availability_zone is not None:
            body['availabilityZone'] = availability_zone
        if templateType is not None:
            body['templateType'] = templateType

        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def list_clusters(self, marker=None, max_keys=None):
        """
        List clusters

        :param marker:
        :type marker: string

        :param max_keys: max records returned.
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster'
        params = None
        if marker is not None or max_keys is not None:
            params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys

        return self._send_request(http_methods.GET, path, params=params)

    @required(cluster_id=value_type)
    def get_cluster(self, cluster_id):
        """
        Get cluster

        :param cluster_id: cluster id
        :type cluster_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s' % compat.convert_to_string(cluster_id)
        return self._send_request(http_methods.GET, path)
    @required(cluster_id=value_type)
    def list_cluster_hosts(self, cluster_id):
        """
        Get cluster hosts
        :param cluster_id: cluster id
        :type cluster_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/hosts' % compat.convert_to_string(cluster_id)
        return self._send_request(http_methods.GET, path)

    @required(cluster_id=value_type)
    def get_cluster_ambariPassword(self, cluster_id):
        """
        Get cluster ambari password

        :param cluster_id: cluster id
        :type cluster_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/ambaripassword' % compat.convert_to_string(cluster_id)
        return self._send_request(http_methods.GET, path)

    @required(cluster_id=value_type)
    def terminate_cluster(self, cluster_id):
        """
        Terminate cluster

        :param cluster_id: cluster id
        :type cluster_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s' % compat.convert_to_string(cluster_id)
        return self._send_request(http_methods.DELETE, path)



    @required(cluster_id=value_type,
              instance_group_config=list)
    def scale_cluster(self, cluster_id, instance_group_config):
        """
        Scale cluster
        :param cluster_id: cluster id
        :type cluster_id: string

        :param instance_group_id: instance group id
        :type instance_group_id: string

        :param instance_count: instance count
        :type instance_count: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = "/cluster/%s/instanceGroup" % compat.convert_to_string(cluster_id)
        params = None
        body = {
            "instanceGroups": instance_group_config
        }
        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body))


    @required(cluster_id=value_type, steps=list)
    def add_steps(self, cluster_id, steps, client_token=None):
        """
        Add steps

        :param cluster_id: cluster id
        :type cluster_id: string

        :param steps: steps to be added
        :type steps: Array

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/step' % compat.convert_to_string(cluster_id)
        params = None
        if client_token is not None:
            params = {
                'clientToken': client_token
            }
        body = json.dumps({'steps': steps})
        return self._send_request(http_methods.POST, path, params=params, body=body)

    @required(cluster_id=value_type)
    def list_steps(self, cluster_id, pageNo=None, pageSize=None):
        """
        List step

        :param cluster_id: cluster id
        :type cluster_id: string

        :param marker:
        :type marker: string

        :param max_keys: max records returned.
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/step' % compat.convert_to_string(cluster_id)
        params = None
        if pageNo is not None or pageSize is not None:
            params = {}
        if pageNo is not None:
            params['pageNo'] = pageNo
        if pageSize is not None:
            params['pageSize'] = pageSize

        return self._send_request(http_methods.GET, path, params=params)

    @required(cluster_id=value_type, step_id=value_type)
    def get_step(self, cluster_id, step_id):
        """
        Get step

        :param cluster_id: cluster id
        :type cluster_id: string

        :param step_id: step id
        :type step_id: string

        :return: baidubce.bce_response.BceResponse
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/step/%s' % (compat.convert_to_string(cluster_id),
                compat.convert_to_string(step_id))
        return self._send_request(http_methods.GET, path)
    @required(
        clusterId=value_type,
        stepId=value_type
    )
    def cancel_step(self, clusterId, stepId):
        """

        :param clusterId:cluster id
        :param stepId: step id
        :return: baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/step/%s' % (clusterId, stepId)
        return self._send_request(http_methods.DELETE, path)

    @required(cluster_id=value_type, instance_group_id=value_type)
    def list_instances(self, cluster_id, instance_group_id):
        """
        List instances

        :param cluster_id: cluster id
        :type cluster_id: string

        :param instance_group_id: instance group id
        :type instance_group_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/instanceGroup/%s/instance' % (compat.convert_to_string(cluster_id),
                compat.convert_to_string(instance_group_id))
        return self._send_request(http_methods.GET, path)

    @required(cluster_id=value_type)
    def list_instance_groups(self, cluster_id):
        """
        List instance groups

        :param cluster_id: cluster id
        :type cluster_id: string

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = '/cluster/%s/instanceGroup' % compat.convert_to_string(cluster_id)
        return self._send_request(http_methods.GET, path)


    @required(cluster_id=value_type)
    def describe_cluster(self, cluster_id):
        """
        :param cluster_id: clusterId
        :type  cluster_id: string
        :return: baidubce.bce_response.BceResponse
        """
        params = None
        body = {
            'clusterId': cluster_id
        }
        path ='/cluster/detail'
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    @required(clusterId=value_type,
              newName=value_type)
    def rename_cluster(self, clusterId, newName):
        """
        rename a cluster
        :param clusterId: clusterId
        :type  clusterId: string
        :param newName: newName
        :type  newName: string
        :return: baidubce.bce_response.BceResponse
        """
        if newName is None or len(newName.strip(" ")) == 0:
            raise ValueError("newName can not be empty.")
        params = None
        body = {
            'clusterId': clusterId,
            'newName': newName
        }
        path = '/cluster/rename'
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))


    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        config.endpoint = compat.convert_to_bytes(config.endpoint)
        return bce_http_client.send_request(
            config, sign_wrapper([b'host', b'x-bce-date']), [handler.parse_error, body_parser],
            http_method, compat.convert_to_bytes(BmrClient.prefix + path), body, headers, params)


def sign_wrapper(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""
    def _wrapper(credentials, http_method, path, headers, params):
        credentials.access_key_id = compat.convert_to_bytes(credentials.access_key_id)
        credentials.secret_access_key = compat.convert_to_bytes(credentials.secret_access_key)

        return bce_v1_signer.sign(credentials,
                                  compat.convert_to_bytes(http_method),
                                  compat.convert_to_bytes(path), headers, params,
                                  headers_to_sign=headers_to_sign)
    return _wrapper


def instance_group(group_type, instance_type, instance_count,
                   name=None, cds=None, root_DiskSizeInGB=40, root_DiskMediumType='ssd'):
    """
    Construct instance group

    :param group_type: instance group type
    :type group_type: ENUM {'Master', 'Core', 'Task'}

    :param instance_type
    :type instance_type: ENUM {'g.small', 'c.large', 'm.medium', 's.medium', 'c.2xlarge'}

    :param instance_count
    :type instance_count: int

    :param name: instance group name
    :type name: string
    """
    instance_group = {
        'type': group_type,
        'instanceCount': instance_count,
        'instanceType': instance_type,
        'rootDiskSizeInGB': root_DiskSizeInGB,
        'rootDiskMediumType': root_DiskMediumType,
        'cds': cds
    }
    if name is not None:
        instance_group['name'] = name

    return instance_group


def cdsitem(sizeInGB, mediumType):
    """
    :param sizeInGB: sizeInGB
    :type string
    :param mediumType: mediumType
    :type string ssd, sata, premium_ssd
    :return: cds
    """
    cds = {
        'sizeInGB': sizeInGB,
        'mediumType': mediumType
     }
    return cds
def application(name, version, properties=None):
    """
    Construct application

    :param name: application type
    :type name: ENUM {'hadoop', 'spark', 'hive', 'pig', 'hbase', 'hue', 'zeppelin', 'kafka', 'mahout'}

    :param version: application version
    :type version: string

    :param properties: application properties
    :type properties: dict
    """
    application = {
        'name': name,
        'version': version
    }
    if properties is not None:
        application['properties'] = properties
    return application


def step(step_type, action_on_failure, properties, name=None, additional_files=None):
    """
    Create step

    :param step_type: the type of step
    :type step_type: Enum {'Java','Streaming','Hive','Pig', 'Spark'}

    :param action_on_failure
    :type actionOnFailure: Enum {'Continue','TerminateCluster','CancelAndWait'}

    :param properties: step properties
    :type properties: dict

    :param name: the name of the step
    :type name: string

    :param additional_files: list of step additional file
    :type additional_files: list
    """
    step = {
        'actionOnFailure': action_on_failure,
        'type': step_type,
        'properties': properties
    }
    if name is not None:
        step['name'] = name
    if additional_files is not None and len(additional_files) > 0:
        step['additionalFiles'] = additional_files
    return step


def java_step_properties(jar, main_class, arguments=None):
    """
    Create java step properties

    :param jar: the path of .jar file
    :type jar: string

    :param main_class: the package path for main class
    :type main_class: string

    :param arguments: arguments for the step
    :type arguments: string

    :return:
    :rtype map
    """
    java_step = {
        'jar': jar,
        'mainClass': main_class
    }
    if arguments is not None:
        java_step['arguments'] = arguments
    return java_step


def streaming_step_properties(input, output, mapper, reducer=None, arguments=None):
    """
    Create streaming step properties

    :param input: the input path of step
    :type input: string

    :param output: the output path of step
    :type output: string

    :param mapper: the mapper program of step
    :type mapper: string

    :param reducer: the reducer program of step
    :type reducer: string

    :param arguments: arguments for the step
    :type arguments: string

    :return:
    :rtype map
    """
    streaming_step = {
        'mapper': mapper,
        'reducer': '',
        'input': input,
        'output': output
    }
    if reducer is not None:
        streaming_step['reducer'] = reducer
    if arguments is not None:
        streaming_step['arguments'] = arguments
    return streaming_step


def pig_step_properties(script, arguments=None, input=None, output=None):
    """
    Create pig step properties

    :param script: the script path of step
    :type script: string

    :param arguments: arguments for the step
    :type arguments: string

    :param input: the input path of step
    :type input: string

    :param output: the output path of step
    :type output: string

    :return:
    :rtype map
    """
    pig_step = {
        'script': script
    }
    if arguments is not None:
        pig_step['arguments'] = arguments
    if input is not None:
        pig_step['input'] = input
    if output is not None:
        pig_step['output'] = output
    return pig_step


def hive_step_properties(script, arguments=None, input=None, output=None):
    """
    Create hive step properties

    :param script: the script path of step
    :type script: string

    :param arguments: arguments for the step
    :type arguments: string

    :param input: the input path of step
    :type input: string

    :param output: the output path of step
    :type output: string

    :return:
    :rtype map
    """
    hive_step = {
        'script': script
    }
    if arguments is not None:
        hive_step['arguments'] = arguments
    if input is not None:
        hive_step['input'] = input
    if output is not None:
        hive_step['output'] = output
    return hive_step


def spark_step_properties(jar, submitOptions, arguments=None):
    """
    Create spark step properties

    :param jar: the path of .jar file
    :type jar: string

    :param main_class: the package path for main class
    :type main_class: string

    :param arguments: arguments for the step
    :type arguments: string

    :return:
    :rtype map
    """
    spark_step = {
        'jar': jar,
        'submitOptions': submitOptions
    }
    if arguments is not None:
        spark_step['arguments'] = arguments
    return spark_step


def additional_file(remote, local):
    """
    Create step additional file

    :param remote: the remote file of the additional file
    :type remote: string

    :param local: the local file of the additional file
    :type local: string

    :return:
    :rtype map
    """
    return {
        'remote': remote,
        'local': local,
    }
def instancegroup_config(id, instanceCount):
    """
    create instance_group
    :param id: id
    :type id: string
    :param instanceCount: instanceCount
    :type instanceCount: int
    :return: instancegroup_config
    """
    instancegroup_config = {
        'id': id,
        'instanceCount': instanceCount
    }
    return instancegroup_config
@required(
    period=int,
    periodUnit=value_type,
)
def schedule_properties(period, periodUnit, startTime=None, endTime=None):
    """
    :param period: period
    :type id: int
    :param periodUnit: periodUnit
    :type id: string
    :param startTime: startTime
    :param endTime: endTime
    :return: schedule
    """
    schedule = {
        'period': period,
        'periodUnit': periodUnit,
    }
    if startTime is not None:
        schedule['startTime'] = startTime
    if endTime is not None:
        schedule['endTime'] = endTime
    return schedule