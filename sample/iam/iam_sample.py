# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Samples for iam client.
"""
# -- coding:utf-8 --

import iam_sample_conf

from baidubce.services.iam.iam_client import IamClient


# ###################################### #role management# ########################################### #

def get_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    response = iam_client.get_role(role_name=role_name)

    print(response)


def create_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    create_role_request = {"name": "test_role", "description": "create role: test_role",
                           "assumeRolePolicyDocument": "{\"version\":\"v1\",\"accessControlList\":[{"
                                                       "\"service\":\"bce:iam\",\"permission\":[\"AssumeRole\"],"
                                                       "\"region\":\"*\",\"grantee\":[{"
                                                       "\"id\":\"test_account_id\"}],"
                                                       "\"effect\":\"Allow\"}]}"}
    response = iam_client.create_role(create_role_request)

    print(response)


def update_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    update_role_request = {"description": "update role: test_role",
                           "assumeRolePolicyDocument": "{\"version\":\"v1\",\"accessControlList\":[{"
                                                       "\"service\":\"bce:iam\",\"permission\":[\"AssumeRole\"],"
                                                       "\"region\":\"*\",\"grantee\":[{"
                                                       "\"id\":\"test_account_id\"}],"
                                                       "\"effect\":\"Allow\"}]}"}
    response = iam_client.update_role(role_name, update_role_request)

    print(response)


def delete_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    response = iam_client.delete_role(role_name=role_name)

    print(response)


def list_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    response = iam_client.list_role()

    print(response)


# #################################### #policy management# ########################################## #

def create_policy():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    create_policy_request = {"name": "test_policy", "description": "create policy: test_policy_1",
                             "document": '{ "accessControlList": [ { "region": "bj", "resource": [ "*" ], "effect":'
                                         '"Allow", "service": "bce:bos", "permission": [ "READ" ] } ] } '}
    response = iam_client.create_policy(create_policy_request)

    print(response)


def get_policy():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.get_policy(policy_name=policy_name, policy_type=policy_type)

    print(response)


def update_policy():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)
    policy_name = b"test_policy"
    update_policy_request = {"name": "test_policy", "description": "update policy: test_policy_2",
                             "document": '{ "accessControlList": [ { "region": "bj", "resource": [ "*" ], "effect":'
                                         '"Allow", "service": "bce:bos", "permission": [ "READ" ] } ] } '}
    response = iam_client.update_policy(policy_name, update_policy_request)

    print(response)


def delete_policy():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    policy_name = b"test_policy"
    response = iam_client.delete_policy(policy_name=policy_name)

    print(response)


def list_policy():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    policy_type = b"Custom"
    name_filter = b"t"
    response = iam_client.list_policy(policy_type=policy_type, name_filter=name_filter)

    print(response)


def attach_policy_to_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.attach_policy_to_user(user_name, policy_name, policy_type)

    print(response)


def detach_policy_from_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.detach_policy_from_user(user_name, policy_name, policy_type)

    print(response)


def list_policies_from_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.list_policies_from_user(user_name)

    print(response)


def attach_policy_to_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.attach_policy_to_group(group_name, policy_name, policy_type)

    print(response)


def detach_policy_from_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.detach_policy_from_group(group_name, policy_name, policy_type)

    print(response)


def list_policies_from_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    response = iam_client.list_policies_from_group(group_name)

    print(response)


def attach_policy_to_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.attach_policy_to_role(role_name, policy_name, policy_type)

    print(response)


def detach_policy_from_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    policy_name = b"test_policy"
    policy_type = b"Custom"
    response = iam_client.detach_policy_from_role(role_name, policy_name, policy_type)

    print(response)


def list_policies_from_role():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    role_name = b"test_role"
    response = iam_client.list_policies_from_role(role_name)

    print(response)


def list_attached_entities_by_grant_type():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    policy_id = b"test_policy_id"
    grant_type = b"UserPolicy"
    response = iam_client.list_attached_entities_by_grant_type(policy_id, grant_type)

    print(response)


# ##################################### #user management# ########################################## #

def create_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    create_user_request = {"name": "test_user", "description": "create user: test_user"}
    response = iam_client.create_user(create_user_request)

    print(response)


def get_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b'test_user'
    response = iam_client.get_user(user_name)

    print(response)


def update_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    update_user_request = {"name": "test_user", "description": "test-new"}
    response = iam_client.update_user(user_name, update_user_request)

    print(response)


def delete_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.delete_user(user_name)

    print(response)


def list_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    response = iam_client.list_user()

    print(response)


def update_user_login_profile():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)
    update_user_login_profile_request = {"enabledLoginMfa": True, "loginMfaType": "",
                                         "thirdPartyType": "PASSPORT", "thirdPartyAccount": "testPassportAccount"}
    user_name = b"test_user"
    response = iam_client.update_user_login_profile(user_name, update_user_login_profile_request)

    print(response)


def get_user_login_profile():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.get_user_login_profile(user_name)

    print(response)


def delete_user_login_profile():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.delete_user_login_profile(user_name)

    print(response)


def create_user_accesskey():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.create_user_accesskey(user_name)

    print(response)


def disable_user_accesskey():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    accesskey_id = b"test_access_key_id"

    response = iam_client.disable_user_accesskey(user_name, accesskey_id)
    print(response)


def enable_user_accesskey():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    accesskey_id = b"test_access_key_id"
    response = iam_client.enable_user_accesskey(user_name, accesskey_id)

    print(response)


def delete_user_accesskey():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    accesskey_id = b"test_access_key_id"
    response = iam_client.delete_user_accesskey(user_name, accesskey_id)

    print(response)


def list_user_accesskey():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.list_user_accesskey(user_name)

    print(response)


def unbind_user_mfa_device():
    """
        Args:
            None
        Returns:
            None
        """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test2"
    mfa_type = b"TOTP"
    response = iam_client.unbind_user_mfa_device(user_name, mfa_type)

    print(response)


def create_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    create_group_request = {"name": "test_group", "description": "create test_group"}
    response = iam_client.create_group(create_group_request)

    print(response)


def get_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    response = iam_client.get_group(group_name)

    print(response)


def update_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    update_group_request = {"name": "test_group", "description": "update test_group"}
    response = iam_client.update_group(group_name, update_group_request)

    print(response)


def delete_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    response = iam_client.delete_group(group_name)

    print(response)


def list_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    response = iam_client.list_group()

    print(response)


def add_user_to_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    user_name = b"test_user"
    response = iam_client.add_user_to_group(group_name, user_name)

    print(response)


def remove_user_from_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    user_name = b"test_user"
    response = iam_client.remove_user_from_group(group_name, user_name)

    print(response)


def list_user_group():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    user_name = b"test_user"
    response = iam_client.list_user_group(user_name)

    print(response)


def list_group_user():
    """
    Args:
        None
    Returns:
        None
    """
    iam_client = IamClient(iam_sample_conf.config)

    group_name = b"test_group"
    response = iam_client.list_group_user(group_name)

    print(response)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create_user()
    # get_user()
    # update_user()
    # list_user()
    # update_user_login_profile()
    # get_user_login_profile()
    # delete_user_login_profile()
    # create_user_accesskey()
    # disable_user_accesskey()
    # enable_user_accesskey()
    # list_user_accesskey()
    # delete_user_accesskey()
    # delete_user()
    # unbind_user_mfa_device()

    # create_group()
    # get_group()
    # update_group()
    # list_group()
    # add_user_to_group()
    # list_user_group()
    # list_group_user()
    # remove_user_from_group()
    # delete_group()

    # create_role()
    # get_role()
    # update_role()
    # list_role()
    # delete_role()

    # create_policy()
    # get_policy()
    # list_policy()
    # attach_policy_to_user()
    # list_policies_from_user()
    # detach_policy_from_user()
    # attach_policy_to_group()
    # list_policies_from_group()
    # detach_policy_from_group()
    # attach_policy_to_role()
    # list_policies_from_role()
    # detach_policy_from_role()
    # delete_policy()
    # update_policy()
    # list_attached_entities_by_grant_type()
