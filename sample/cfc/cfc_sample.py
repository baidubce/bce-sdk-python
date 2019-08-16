# -*- coding: UTF-8 -*-
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
Samples for bos client.
"""

import time
import zipfile

from baidubce.services.cfc.cfc_client import CfcClient
from baidubce.services.cfc import models
import cfc_sample_conf

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    crontab_obj = models.CrontabTriggerData(brn='brn')
    print(crontab_obj.Input)
    crontab_obj.serialize()
    function_name = "bce_python_sdk_test_" + str(int(time.time()))
    # create a cfc client
    cfc_client = CfcClient(cfc_sample_conf.config)

    base64_file = "UEsDBBQACAAIAAAAIQAAAAAAAAAAAAAAAAAIABAAaW5kZXgucHlVWAwA7v9nWoAFpBL1ARQAS0lN" \
                  "U8hIzEvJSS3SSC1LzSvRUUjOzytJrSjRtFLgUgACMFGUWlJalKeg5JGak5OvEJ5flJOixAUAUEsH" \
                  "CISiEJQ5AAAAPAAAAFBLAwQKAAAAAAAVnkFMAAAAAAAAAAAAAAAACQAQAF9fTUFDT1NYL1VYDACa" \
                  "/nJamv5yWvUBFABQSwMEFAAIAAgAAAAhAAAAAAAAAAAAAAAAABMAEABfX01BQ09TWC8uX2luZGV4" \
                  "LnB5VVgMAO7/Z1qABaQS9QEUAGNgFWNnYGJg8E1MVvAPVohQgAKQGAMnEBsB8SIgBvGvMBAFHENC" \
                  "gqBMkI4ZQGyDpoQRIS6anJ+rl1hQkJOqV1iaWJSYV5KZl8pQqG9gYGFobZpoZp6Wlmph7ZxRlJ+b" \
                  "am1p5GxqaWZuruvm6mKqa2LmbKhr6WZgpmvp4mTu6mJpYmZuaMAAAFBLBwiwXr/lhwAAANQAAABQ" \
                  "SwECFQMUAAgACAAAACEAhKIQlDkAAAA8AAAACAAMAAAAAAAAAABA7YEAAAAAaW5kZXgucHlVWAgA" \
                  "7v9nWoAFpBJQSwECFQMKAAAAAAAVnkFMAAAAAAAAAAAAAAAACQAMAAAAAAAAAABA/UF/AAAAX19N" \
                  "QUNPU1gvVVgIAJr+clqa/nJaUEsBAhUDFAAIAAgAAAAhALBev+WHAAAA1AAAABMADAAAAAAAAAAA" \
                  "QKSBtgAAAF9fTUFDT1NYLy5faW5kZXgucHlVWAgA7v9nWoAFpBJQSwUGAAAAAAMAAwDSAAAAjgEA" \
                  "AAAA"

    base64_file_with_args = 'UEsDBBQACAAAABWeQUwAAAAAAAAAAAAAAAAJAAwAX19NQUNPU1gvVVgIAJr+clqa/n' \
                            'JaUEsHCAAAAAAAAAAAAAAAAFBLAwQUAAgACAAAACEAAAAAAAAAAAAAAAAAEwAMAF9f' \
                            'TUFDT1NYLy5faW5kZXgucHlVWAgA7v9nWoAFpBJiYBVjZ2BiYPBNTFbwD1aIUIACkB' \
                            'gDJwMDgxEDA8MiBgYw/woDUcAxJCQIygTpmMHAwGCDpoQRIS6anJ+rl1hQkJOqV1ia' \
                            'WJSYV5KZl8pQqG9gYGFobZpoZp6Wlmph7ZxRlJ+bam1p5GxqaWZuruvm6mKqa2LmbK' \
                            'hr6WZgpmvp4mTu6mJpYmZuaMAACAAA//9QSwcIsF6/5ZAAAADUAAAAUEsDBBQACAAI' \
                            'AAAAAAAAAAAAAAAAAAAAAAAIAAAAaW5kZXgucHlKSU1TyEjMS8lJLdJILUvNK9FRSM' \
                            '7PK0mtKNG0UuBSUFBQSFSwVQDLRCslKsWChYpSS0qL8hSUPFJzcvIVwvOLclKUFLQV' \
                            'ErkAAQAA//9QSwcIxL+5xU4AAABOAAAAUEsBAhQDFAAIAAAAFZ5BTAAAAAAAAAAAAA' \
                            'AAAAkADAAAAAAAAAAAQP1BAAAAAF9fTUFDT1NYL1VYCACa/nJamv5yWlBLAQIUAxQA' \
                            'CAAIAAAAIQCwXr/lkAAAANQAAAATAAwAAAAAAAAAAECkgUMAAABfX01BQ09TWC8uX2' \
                            'luZGV4LnB5VVgIAO7/Z1qABaQSUEsBAhQAFAAIAAgAAAAAAMS/ucVOAAAATgAAAAgA' \
                            'AAAAAAAAAAAAAAAAIAEAAGluZGV4LnB5UEsFBgAAAAADAAMAxgAAAKQBAAAAAA=='

    # create zip file
    s = """def handler(event, context):
        return "Hello World"
    """
    f = zipfile.ZipFile('demo.zip', 'w', zipfile.ZIP_DEFLATED)
    f.writestr('index.py', bytes(s))
    f.close()

    # create function with zip_file
    create_response = cfc_client.create_function(function_name,
                                                 description="cfcsdkdemode",
                                                 handler="index.handler",
                                                 memory_size=128,
                                                 region='bj',
                                                 zip_file=base64_file,
                                                 publish=False,
                                                 run_time='python2',
                                                 timeout=3,
                                                 dry_run=False)
    __logger.debug("[Sample CFC] create_response:%s", create_response)
    # delete function
    delete_function_response = cfc_client.delete_function(function_name)
    __logger.debug("[Sample CFC] delete_function_response:%s", delete_function_response)

    # create function by code zip file
    create_response_by_code_zip = cfc_client.create_function(function_name, description="cfcsdkdemode",
                                                             handler="index.handler",
                                                             memory_size=128,
                                                             region='bj',
                                                             # zip_file=base64_file,
                                                             publish=False,
                                                             run_time='python2',
                                                             timeout=3,
                                                             dry_run=False,
                                                             code_zip_file='demo.zip')
    __logger.debug("[Sample CFC] create_response:%s", create_response_by_code_zip)

    # get function use brn
    brn = create_response_by_code_zip.FunctionBrn
    get_function_response = cfc_client.get_function(create_response_by_code_zip.FunctionBrn)
    __logger.debug("[Sample CFC] get_function response:%s", get_function_response)

    # list functions
    list_functions_response = cfc_client.list_functions()
    for k in list_functions_response.Functions:
        __logger.debug("[Sample CFC] function name:%s", k.FunctionName)

    # invocations function return  httplib.httpresponse
    invocations_response = cfc_client.invocations(brn)
    __logger.debug("[Sample CFC] invocations_response tail:%s \n %s", invocations_response.read(),
                   invocations_response.getheaders())
    time.sleep(0.1)

    # invocations function
    invocations_response = cfc_client.invocations(brn)
    __logger.debug("[Sample CFC] invocations_response:%s", invocations_response)
    time.sleep(0.1)

    # update function code
    update_function_code_response = cfc_client.update_function_code(brn,
                                                                    zip_file=base64_file_with_args,
                                                                    publish=True)
    __logger.debug("[Sample CFC] update_function_code_response:%s", update_function_code_response)
    time.sleep(0.1)

    # invocations function with body args return  httplib.httpresponse
    invocations_response = cfc_client.invocations(update_function_code_response.FunctionBrn,
                                                  body={"a": " baidu"})
    __logger.debug("[Sample CFC] invocations_response:%s", invocations_response.read())
    time.sleep(0.1)

    # get_function_configuration_response
    get_function_configuration_response = cfc_client.get_function_configuration(brn)
    __logger.debug("[Sample CFC] get_function_configuration_response:%s",
                   get_function_configuration_response)
    time.sleep(0.1)

    # update_function_configuration
    response = cfc_client.update_function_configuration(brn, description="update config",
                                                        environment={"e1": "1"})
    __logger.debug("[Sample CFC] update_function_configuration_response:%s", response)
    time.sleep(0.1)

    # publish_version
    response = cfc_client.publish_version(brn, description="this is test publish")
    __logger.debug("[Sample CFC] publish_version_re:%s", response)
    time.sleep(0.1)

    # list_versions_by_function
    response = cfc_client.list_versions_by_function(brn)
    __logger.debug("[Sample CFC] list_versions_by_function_re:%s", response)
    time.sleep(0.1)

    response = cfc_client.create_alias(function_name, function_version="1", name="my_alias",
                                       description="this is first alias")
    __logger.debug("[Sample CFC] create_alias:%s", response)
    time.sleep(0.1)

    response = cfc_client.update_alias(brn, function_version="$LATEST",
                                       alias_name="my_alias", description="change")
    __logger.debug("[Sample CFC] update_alias:%s", response)
    time.sleep(0.1)

    response = cfc_client.get_alias(brn, alias_name="my_alias")
    __logger.debug("[Sample CFC] get_alias:%s", response)
    alias_brn = response.AliasBrn

    response = cfc_client.invocations(response.FunctionName, qualifier="my_alias",
                                      body={"a": " baidu"})
    __logger.debug("[Sample CFC] invocations alias_brn :%s", response.read())
    time.sleep(0.1)

    response = cfc_client.list_aliases(alias_brn)
    __logger.debug("[Sample CFC] list_aliases :%s", response)
    time.sleep(0.1)

    response = cfc_client.delete_alias(brn, alias_name="my_alias")
    __logger.debug("[Sample CFC] delete_alias:%s", response)
    time.sleep(0.1)

    crontab_trigger_data = models.CrontabTriggerData(brn=brn, name='test_cron', custom_input='',
                                                     schedule_expression='rate(1 minute)', enabled=True)
    response = cfc_client.create_trigger(function_brn=brn, trigger_data=crontab_trigger_data)
    __logger.debug("[Sample CFC] create_trigger:%s", response)
    relation_id = response.Relation.RelationId
    time.sleep(0.1)

    response = cfc_client.list_triggers(brn)
    __logger.debug("[Sample CFC] list_triggers:%s", response)
    time.sleep(0.1)

    crontab_trigger_data.ScheduleExpression = "rate(2 minutes)"
    crontab_trigger_data.set_status(False)
    response = cfc_client.update_trigger(function_brn=brn, relation_id=relation_id, trigger_data=crontab_trigger_data)
    __logger.debug("[Sample CFC] update_trigger:%s", response)
    time.sleep(0.1)

    response = cfc_client.delete_trigger(function_brn=brn, relation_id=relation_id, source=models.CRONTAB_TRIGGER)
    __logger.debug("[Sample CFC] delete_trigger:%s", response)
    time.sleep(0.1)

    response = cfc_client.create_trigger(function_brn=brn, source=models.DUEROS_TRIGGER)
    __logger.debug("[Sample CFC] create_trigger:%s", response)
    relation_id = response.Relation.RelationId
    time.sleep(0.1)

    response = cfc_client.delete_trigger(function_brn=brn, source=models.DUEROS_TRIGGER, relation_id=relation_id)
    __logger.debug("[Sample CFC] delete_trigger:%s", response)
    time.sleep(0.1)

    # publish_version
    response = cfc_client.publish_version(brn, description="for duedge trigger")
    __logger.debug("[Sample CFC] publish_version_re:%s", response)
    duedge_brn = response.FunctionBrn
    time.sleep(0.1)

    response = cfc_client.create_trigger(function_brn=duedge_brn, source=models.DUEDGE_TRIGGER)
    __logger.debug("[Sample CFC] create_trigger:%s", response)
    relation_id = response.Relation.RelationId
    time.sleep(0.1)

    response = cfc_client.delete_trigger(function_brn=duedge_brn, source=models.DUEDGE_TRIGGER, relation_id=relation_id)
    __logger.debug("[Sample CFC] delete_trigger:%s", response)
    time.sleep(0.1)

    resource_path = 'hello' + str(int(time.time()))
    http_trigger_data = models.HttpTriggerData(auth_type='anonymous', method='GET', resource_path=resource_path)

    response = cfc_client.create_trigger(function_brn=brn, trigger_data=http_trigger_data)
    __logger.debug("[Sample CFC] create_trigger:%s", response)
    relation_id = response.Relation.RelationId
    time.sleep(0.1)

    response = cfc_client.delete_trigger(function_brn=brn, source=models.HTTP_TRIGGER, relation_id=relation_id)
    __logger.debug("[Sample CFC] delete_trigger:%s", response)
    time.sleep(0.1)

    # bos trigger need bos bucket
    # bos_trigger_data = models.BOSTriggerData(bucket='youbucket', event_type=['PutObject'], name='mybos_test',
    #                                          resource='/my.img', status=True)
    # response = cfc_client.create_trigger(function_brn=brn, trigger_data=bos_trigger_data)
    # __logger.debug("[Sample CFC] create_trigger:%s", response)
    # relation_id = response.Relation.RelationId
    # time.sleep(0.1)
    #
    # bos_trigger_data.Resource = '/my*img'
    # response = cfc_client.update_trigger(function_brn=brn, relation_id=relation_id, trigger_data=bos_trigger_data)
    # __logger.debug("[Sample CFC] update_trigger:%s", response)
    # time.sleep(0.1)

    # delete function
    delete_function_response = cfc_client.delete_function(function_name)
    __logger.debug("[Sample CFC] delete_function_response:%s", delete_function_response)
