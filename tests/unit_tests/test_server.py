# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from mock import patch
from nose.tools import assert_raises
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.org.OrgOrg import OrgOrg
from ucsmsdk_samples.server.ipmi_policy import ipmi_policy_create
from ucsmsdk.mometa.aaa.AaaEpAuthProfile import AaaEpAuthProfile


# Patch UcsHandle.commit to simulate CIMC interaction w/o real CIMC
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate CIMC interaction w/o real CIMC
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate orgs
@patch.object(UcsHandle, 'query_dn')
def test_valid_ipmi_policy_create(query_mock, add_mo_mock, commit_mock):
    # Create a root org as a return value to query_dn
    query_mock.return_value = OrgOrg(parent_mo_or_dn="org-root", name="root")
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Default parameters
    ipmi_retval = ipmi_policy_create(handle, name="test_ipmi_policy")
    # Verify we were passed back the correct object type
    assert isinstance(ipmi_retval, AaaEpAuthProfile)
    # Verify the name we gave it was assigned correctly
    assert ipmi_retval.name == "test_ipmi_policy"
    # Verify the retruned object has no users (children)
    assert len(ipmi_retval.child) == 0

    # Scenario: default user, custom password
    ipmi_retval = ipmi_policy_create(handle, name="test_ipmi_policy",
                                     password="password")
    user_retval = ipmi_retval.child[0]
    # Verify the returned policy has a user (child)
    assert user_retval is not None
    # Verify the username is the default 'admin'
    assert user_retval.name is 'admin'
    # Verify the password was assigned correctly
    assert user_retval.pwd is 'password'

    # Scenario: custom user, custom password
    ipmi_retval = ipmi_policy_create(handle, name="test_ipmi_policy",
                                     username="myuser", password="password")
    user_retval = ipmi_retval.child[0]
    # Verify the returned policy has a user (child)
    assert user_retval is not None
    # Verify the username was assigned correctly
    assert user_retval.name is 'myuser'
    # Verify the password was assigned correctly
    assert user_retval.pwd is 'password'


@patch.object(UcsHandle, 'commit')
@patch.object(UcsHandle, 'add_mo')
@patch.object(UcsHandle, 'query_dn')
def test_invalid_ipmi_policy_create(query_mock, add_mo_mock, commit_mock):
    # Patch UcsHandle.query_dn to simulate valid/invalid orgs
    # Patch UcsHandle.add_mo to simulate CIMC interaction w/o real CIMC
    # Patch UcsHandle.commit to simulate CIMC interaction w/o real CIMC
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Invalid Org
    query_mock.return_value = None
    # Verify exception was raised for invalid org
    assert_raises(ValueError, ipmi_policy_create, handle, 'invalid')
