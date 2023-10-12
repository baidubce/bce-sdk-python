# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Unit tests for iam client.
"""
import unittest

import baidubce
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.iam import iam_client

HOST = 'https://iam.bj.baidubce.com:80'
AK = ''
SK = ''


class TestIamClient(unittest.TestCase):
    """
    Test class for iam sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = iam_client.IamClient(config)

    def test_create_user(self):
        """
        test_create_user case
        """
        create_user_request = {"name": "test-user1234", "description": "test"}
        self.assertEqual(type(self.client.create_user(create_user_request=create_user_request)),
                         baidubce.bce_response.BceResponse)

    def get_user(self):
        """
        get_user case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.get_user(user_name=user_name)), baidubce.bce_response.BceResponse)

    def test_update_user(self):
        """
        test_update_user case
        """
        user_name = b"test"
        update_user_request = {"name": "test-user1234", "description": "test"}
        self.assertEqual(type(self.client.update_user(user_name=user_name, update_user_request=update_user_request)),
                         baidubce.bce_response.BceResponse)

    def test_delete_user(self):
        """
        test_delete_user case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.delete_user(user_name)), baidubce.bce_response.BceResponse)

    def test_list_user(self):
        """
        test_list_user case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.list_user()), baidubce.bce_response.BceResponse)

    def test_update_user_login_profile(self):
        """
        test_update_user_login_profile case
        """
        update_user_login_profile_request = {"enabledLoginMfa": True, "loginMfaType": "",
                                             "thirdPartyType": "PASSPORT", "thirdPartyAccount": "test-passportAccount"}
        user_name = b"test_user1234"
        self.assertEqual(type(self
                              .client.update_user_login_profile(user_name=user_name,
                                                                update_user_login_profile_request=
                                                                update_user_login_profile_request)),
                         baidubce.bce_response.BceResponse)

    def test_get_user_login_profile(self):
        """
        test_get_user_login_profile case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.get_user_login_profile(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_delete_user_login_profile(self):
        """
        test_delete_user_login_profile case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.delete_user_login_profile(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_create_user_accesskey(self):
        """
        test_create_user_accesskey case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.create_user_accesskey(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_disable_user_accesskey(self):
        """
        test_disable_user_accesskey case
        """
        user_name = b"test_user"
        accesskey_id = b"test_accesskey_id"
        self.assertEqual(type(self.client.disable_user_accesskey(user_name=user_name, accesskey_id=accesskey_id)),
                         baidubce.bce_response.BceResponse)

    def test_enable_user_accesskey(self):
        """
        test_enable_user_accesskey case
        """
        user_name = b"test_user"
        accesskey_id = b"test_accesskey_id"
        self.assertEqual(type(self.client.enable_user_accesskey(user_name=user_name, accesskey_id=accesskey_id)),
                         baidubce.bce_response.BceResponse)

    def test_delete_user_accesskey(self):
        """
        test_delete_user_accesskey case
        """
        user_name = b"test_user"
        accesskey_id = b"test_accesskey_id"
        self.assertEqual(type(self.client.delete_user_accesskey(user_name=user_name, accesskey_id=accesskey_id)),
                         baidubce.bce_response.BceResponse)

    def test_list_user_accesskey(self):
        """
        test_list_user_accesskey case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.list_user_accesskey(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_unbind_user_mfa_device(self):
        """
        test_list_user_accesskey case
        """
        user_name = b"test_user"
        mfa_type = b"PHONE"
        self.assertEqual(type(self.client.unbind_user_mfa_device(user_name=user_name, mfa_type=mfa_type)),
                         baidubce.bce_response.BceResponse)

    def test_create_group(self):
        """
         test_create_group case
        """
        create_group_request = {"name": "test_group"}
        self.assertEqual(type(self.client.create_group(create_group_request=create_group_request)),
                         baidubce.bce_response.BceResponse)

    def test_get_group(self):
        """
         test_get_group case
        """
        group_name = b"test_group"
        self.assertEqual(type(self.client.get_group(group_name=group_name)),
                         baidubce.bce_response.BceResponse)

    def test_update_group(self):
        """
         test_update_group case
        """
        group_name = b"test_group"
        update_group_request = {"name": "test_group_new"}
        self.assertEqual(type(self.client.update_group(group_name=group_name,
                                                       update_group_request=update_group_request)),
                         baidubce.bce_response.BceResponse)

    def test_delete_group(self):
        """
          test_delete_group case
        """
        group_name = b"test_group"
        self.assertEqual(type(self.client.delete_group(group_name=group_name)),
                         baidubce.bce_response.BceResponse)

    def test_list_group(self):
        """
          test_list_group case
        """
        self.assertEqual(type(self.client.list_group()), baidubce.bce_response.BceResponse)

    def test_add_user_to_group(self):
        """
          test_add_user_to_group case
        """
        group_name = b"test_group"
        user_name = b"test_user"
        self.assertEqual(type(self.client.add_user_to_group(group_name=group_name, user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_remove_user_from_group(self):
        """
          test_remove_user_from_group case
        """
        group_name = b"test_group"
        user_name = b"test_user"
        self.assertEqual(type(self.client.remove_user_from_group(group_name=group_name, user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_list_user_group(self):
        """
          test_list_user_group case
        """
        user_name = b"test_user"
        self.assertEqual(type(self.client.list_user_group(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_list_group_user(self):
        """
          test_list_group_user case
        """
        group_name = b"test_user"
        self.assertEqual(type(self.client.list_group_user(group_name=group_name)),
                         baidubce.bce_response.BceResponse)

    def test_get_role(self):
        """
        test case for get_role
        """
        role_name = b"test_role"

        self.assertEqual(type(self.client.get_role(role_name=role_name)), baidubce.bce_response.BceResponse)

    def test_create_role(self):
        """
        test case for create_role
        """
        create_role_request = {"name": b"test_role_2", "description": b"create role: test_role_2",
                               "assumeRolePolicyDocument": b"{\"version\":\"v1\",\"accessControlList\":[{"
                                                           b"\"service\":\"bce:iam\",\"permission\":[\"AssumeRole\"],"
                                                           b"\"region\":\"*\",\"grantee\":[{"
                                                           b"\"id\":\"test_account_id\"}],"
                                                           b"\"effect\":\"Allow\"}]}"}

        self.assertEqual(type(self.client.create_role(create_role_request=create_role_request)),
                         baidubce.bce_response.BceResponse)

    def test_update_role(self):
        """
        test case for update_role
        """
        role_name = b"test_role_2"
        update_role_request = {"description": "update role: test_role_2",
                               "assumeRolePolicyDocument": b"{\"version\":\"v1\",\"accessControlList\":[{"
                                                           b"\"service\":\"bce:iam\",\"permission\":[\"AssumeRole\"],"
                                                           b"\"region\":\"*\",\"grantee\":[{"
                                                           b"\"id\":\"test_account_id\"}],"
                                                           b"\"effect\":\"Allow\"}]}"}

        self.assertEqual(type(self.client.update_role(role_name=role_name, update_role_request=update_role_request)),
                         baidubce.bce_response.BceResponse)

    def test_delete_role(self):
        """
        test case for delete_role
        """
        role_name = b"test_role_2"
        self.assertEqual(type(self.client.delete_role(role_name=role_name)),
                         baidubce.bce_response.BceResponse)

    def test_list_role(self):
        """
        test case for list_role
        """

        self.assertEqual(type(self.client.list_role()),
                         baidubce.bce_response.BceResponse)

    def test_create_policy(self):
        """
        test case for create_policy
        """
        create_policy_request = {"name": "test_policy", "description": "create policy: test_policy_1",
                             "document": '{ "accessControlList": [ { "region": "bj", "resource": [ "*" ], "effect":'
                                         '"Allow", "service": "bce:bos", "permission": [ "READ" ] } ] } '}

        self.assertEqual(type(self.client.create_policy(create_policy_request=create_policy_request)),
                         baidubce.bce_response.BceResponse)

    def test_get_policy(self):
        """
        test case for get_policy
        """
        policy_name = b"test_policy_2"
        policy_type = b"Custom"

        self.assertEqual(type(self.client.get_policy(policy_name=policy_name, policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_update_policy(self):
        """
        test case for update_policy
        """
        update_policy_request = {"name": "test_policy1", "description": "update policy: test_policy_1",
                                 "document": '{ "accessControlList": [ { "region": "bj", "resource": [ "*" ], "effect":'
                                             '"Allow", "service": "bce:bos", "permission": [ "OPERATE" ] } ] } '}

        self.assertEqual(type(self.client.update_policy(b"test_policy",
                                                        update_policy_request=update_policy_request)),
                         baidubce.bce_response.BceResponse)

    def test_list_policy(self):
        """
        test case for list_policy
        """
        policy_type = b"Custom"
        name_filter = b"t"

        self.assertEqual(type(self.client.list_policy(policy_type=policy_type, name_filter=name_filter)),
                         baidubce.bce_response.BceResponse)

    def test_delete_policy(self):
        """
        test case for delete_policy
        """
        policy_name = b"test_policy_2"

        self.assertEqual(type(self.client.delete_policy(policy_name=policy_name)),
                         baidubce.bce_response.BceResponse)

    def test_attach_policy_to_user(self):
        """
        test case for attach_policy_to_user
        """
        user_name = b"test"
        policy_name = b"FCFullControlPolicy"
        policy_type = b"System"
        self.assertEqual(type(self.client.attach_policy_to_user(user_name=user_name, policy_name=policy_name,
                                                                policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_detach_policy_from_user(self):
        """
        test case for detach_policy_from_user
        """
        user_name = b"test"
        policy_name = b"FCFullControlPolicy"
        policy_type = b"System"

        self.assertEqual(type(self.client.detach_policy_from_user(user_name=user_name, policy_name=policy_name,
                                                                  policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_list_policies_from_user(self):
        """
        test case for list_policies_from_user
        """
        user_name = b"test"

        self.assertEqual(type(self.client.list_policies_from_user(user_name=user_name)),
                         baidubce.bce_response.BceResponse)

    def test_attach_policy_to_group(self):
        """
        test case for attach_policy_to_group
        """
        group_name = b"test"
        policy_name = b"test_policy_1"
        policy_type = b"Custom"

        self.assertEqual(type(self.client.attach_policy_to_group(group_name=group_name, policy_name=policy_name,
                                                                 policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_detach_policy_from_group(self):
        """
        test case for detach_policy_from_group
        """
        group_name = b"test"
        policy_name = b"GlobalOperatePolicy"
        policy_type = b"System"

        self.assertEqual(type(self.client.attach_policy_to_group(group_name=group_name, policy_name=policy_name,
                                                                 policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_list_policies_from_group(self):
        """
        test case for list_policies_from_group
        """
        group_name = b"test"

        self.assertEqual(type(self.client.list_policies_from_group(group_name=group_name)),
                         baidubce.bce_response.BceResponse)

    def test_attach_policy_to_role(self):
        """
        test case for attach_policy_to_role
        """
        role_name = b"test_role"
        policy_name = b"FCFullControlPolicy"
        policy_type = b"System"

        self.assertEqual(type(self.client.attach_policy_to_role(role_name=role_name, policy_name=policy_name,
                                                                policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_detach_policy_from_role(self):
        """
        test case for detach_policy_from_role
        """
        role_name = b"test_role"
        policy_name = b"FCFullControlPolicy"
        policy_type = b"System"

        self.assertEqual(type(self.client.detach_policy_from_role(role_name=role_name, policy_name=policy_name,
                                                                  policy_type=policy_type)),
                         baidubce.bce_response.BceResponse)

    def test_list_policies_from_role(self):
        """
        test case for list_policies_from_role
        """
        role_name = b"test_role"

        self.assertEqual(type(self.client.list_policies_from_role(role_name=role_name)),
                         baidubce.bce_response.BceResponse)

    def test_list_attached_entities_by_grant_type(self):
        """
        test case for list_attached_entities_by_grant_type
        """
        policy_id = b"test_custom_bcepolicy_id"
        grant_type = b"GroupPolicy"

        self.assertEqual(type(self.client.list_attached_entities_by_grant_type(policy_id=policy_id,
                                                                               grant_type=grant_type)),
            baidubce.bce_response.BceResponse)
