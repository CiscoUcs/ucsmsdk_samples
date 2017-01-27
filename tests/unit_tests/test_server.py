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
from ucsmsdk_samples.server.local_drive import disk_state_set
from ucsmsdk_samples.server.server_pool import server_pool_create, \
    server_pool_add_rack_unit, server_pool_add_slot
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledRackUnit import ComputePooledRackUnit
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
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


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_invalid_ipmi_policy_create(query_mock, add_mo_mock, commit_mock):
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Invalid Org
    query_mock.return_value = None
    # Verify exception was raised for invalid org
    assert_raises(ValueError, ipmi_policy_create, handle, 'invalid')


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
def test_valid_disk_state(add_mo_mock, commit_mock):
        add_mo_mock.return_value = True
        commit_mock.return_value = True
        handle = UcsHandle('169.254.1.1', 'admin', 'password')

        # Scenario: jbod mode
        test_retval = disk_state_set(handle, 1, 4, "jbod")
        assert test_retval.admin_action == "jbod"
        assert test_retval.dn == "sys/rack-unit-1/board/storage-SAS-1/disk-4"

        # Scenario: unconfigured-good mode
        test_retval = disk_state_set(handle, 2, 5, "unconfigured-good")
        assert test_retval.admin_action == "unconfigured-good"
        assert test_retval.dn == "sys/rack-unit-2/board/storage-SAS-1/disk-5"

        # Scenario: custom controller
        test_retval = disk_state_set(handle, 3, 6, "jbod", "storage-SAS-4")
        assert test_retval.dn == "sys/rack-unit-3/board/storage-SAS-4/disk-6"


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
def test_invalid_disk_state(add_mo_mock, commit_mock):
        add_mo_mock.return_value = True
        commit_mock.return_value = True
        handle = UcsHandle('169.254.1.1', 'admin', 'password')

        # Scenario invalid state
        assert_raises(ValueError, disk_state_set, handle, 16, 1, "blah")


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_valid_server_pool_create(query_mock, add_mo_mock, commit_mock):
    query_mock.return_value = OrgOrg(parent_mo_or_dn="org-root", name="root")
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Default parameters
    pool_retval = server_pool_create(handle, 'valid-pool')
    # Verify we were passed back the correct object type
    assert isinstance(pool_retval, ComputePool)
    # Verify the name we gave it was assigned correctly
    assert pool_retval.name == "valid-pool"


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_invalid_server_pool_create(query_mock, add_mo_mock, commit_mock):
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Invalid Org
    query_mock.return_value = None
    # Verify exception was raised for invalid org
    assert_raises(ValueError, server_pool_create, handle, 'invalid-pool')


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_valid_server_pool_add_rack_unit(query_mock, add_mo_mock, commit_mock):
    query_mock.return_value = ComputePool(parent_mo_or_dn="org-root",
                                          name="test-pool")
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Default parameters
    pool_retval = server_pool_add_rack_unit(handle, 16)
    # Verify we were passed back the correct object type
    assert isinstance(pool_retval, ComputePooledRackUnit)
    # Verify the ID we gave it was assigned correctly
    assert pool_retval.id == str(16)


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_invalid_server_pool_add_rack_unit(query_mock, add_mo_mock,
                                           commit_mock):
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Invalid Org
    query_mock.return_value = None
    # Verify exception was raised for invalid org
    assert_raises(ValueError, server_pool_add_rack_unit, handle, 16,)

    # Scenario: Org is not a ComputePool
    query_mock.return_value = OrgOrg(parent_mo_or_dn="org-root", name="root")
    # Verify exception was raised for invalid type
    assert_raises(TypeError, server_pool_add_rack_unit, handle, 16,)


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_valid_server_pool_add_slot(query_mock, add_mo_mock, commit_mock):
    query_mock.return_value = ComputePool(parent_mo_or_dn="org-root",
                                          name="test-pool")
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Default parameters
    pool_retval = server_pool_add_slot(handle, 1, 8)
    # Verify we were passed back the correct object type
    assert isinstance(pool_retval, ComputePooledSlot)
    # Verify the ID we gave it was assigned correctly
    assert pool_retval.chassis_id == str(1)
    assert pool_retval.slot_id == str(8)


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
# Patch UcsHandle.query_dn to simulate valid/invalid orgs
@patch.object(UcsHandle, 'query_dn')
def test_invalid_server_pool_add_slot(query_mock, add_mo_mock,
                                      commit_mock):
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Invalid Org
    query_mock.return_value = None
    # Verify exception was raised for invalid org
    assert_raises(ValueError, server_pool_add_slot, handle, 1, 8)

    # Scenario: Org is not a ComputePool
    query_mock.return_value = OrgOrg(parent_mo_or_dn="org-root", name="root")
    # Verify exception was raised for invalid type
    assert_raises(TypeError, server_pool_add_slot, handle, 1, 8)
