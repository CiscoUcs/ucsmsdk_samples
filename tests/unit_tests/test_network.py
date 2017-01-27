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
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk_samples.network.uplink_port import uplink_port_create
from ucsmsdk_samples.network.server_port import server_port_create


@patch.object(UcsHandle, 'commit')
@patch.object(UcsHandle, 'add_mo')
def test_valid_uplink_port_create(add_mo_mock, commit_mock):
    # Patch UcsHandle.add_mo to simulate CIMC interaction w/o real CIMC
    # Patch UcsHandle.commit to simulate CIMC interaction w/o real CIMC
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Set Fabric-A port Eth1/10 to uplink port
    fabric_dn = 'fabric/lan/A'
    port_id = '10'
    slot_id = '1'
    uplink_port_create(handle, fabric_dn, port_id, slot_id)

    # Assert values of the object passed to add_mo()
    test_uplink_mo = add_mo_mock.call_args[0][0]
    assert test_uplink_mo.port_id == "10"
    assert test_uplink_mo.slot_id == "1"
    assert test_uplink_mo.dn == '{0}/phys-slot-{1}-port-{2}'.format(fabric_dn,
                                                                    slot_id,
                                                                    port_id)

    # Scenario: Set Fabric-B port Eth2/6 to uplink port
    fabric_dn = 'fabric/lan/B'
    port_id = '6'
    slot_id = '2'
    uplink_port_create(handle, fabric_dn, port_id, slot_id)

    # Assert values of the object passed to add_mo()
    test_uplink_mo = add_mo_mock.call_args[0][0]
    assert test_uplink_mo.port_id == "6"
    assert test_uplink_mo.slot_id == "2"
    assert test_uplink_mo.dn == '{0}/phys-slot-{1}-port-{2}'.format(fabric_dn,
                                                                    slot_id,
                                                                    port_id)


@patch.object(UcsHandle, 'commit')
@patch.object(UcsHandle, 'add_mo')
def test_valid_server_port_create(add_mo_mock, commit_mock):
    # Patch UcsHandle.add_mo to simulate CIMC interaction w/o real CIMC
    # Patch UcsHandle.commit to simulate CIMC interaction w/o real CIMC
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Set Fabric-A port Eth1/10 to server port
    fabric_dn = 'fabric/lan/A'
    port_id = '10'
    slot_id = '1'
    server_port_create(handle, fabric_dn, port_id, slot_id)

    # Assert values of the object passed to add_mo()
    test_server_mo = add_mo_mock.call_args[0][0]
    assert test_server_mo.port_id == "10"
    assert test_server_mo.slot_id == "1"
    assert test_server_mo.dn == '{0}/slot-{1}-port-{2}'.format(fabric_dn,
                                                               slot_id,
                                                               port_id)

    # Scenario: Set Fabric-B port Eth2/6 to server port
    fabric_dn = 'fabric/lan/B'
    port_id = '6'
    slot_id = '2'
    server_port_create(handle, fabric_dn, port_id, slot_id)

    # Assert values of the object passed to add_mo()
    test_server_mo = add_mo_mock.call_args[0][0]
    assert test_server_mo.port_id == "6"
    assert test_server_mo.slot_id == "2"
    assert test_server_mo.dn == '{0}/slot-{1}-port-{2}'.format(fabric_dn,
                                                               slot_id,
                                                               port_id)
