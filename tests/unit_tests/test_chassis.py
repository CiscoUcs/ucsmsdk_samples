# Copyright 2017 Cisco Systems, Inc.
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
from ucsmsdk_samples.server.chassis import chassis_acknowledge
from ucsmsdk.mometa.equipment.EquipmentChassis import EquipmentChassis


# Patch UcsHandle.commit to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'commit')
# Patch UcsHandle.add_mo to simulate ucsm interaction w/o real ucsm
@patch.object(UcsHandle, 'add_mo')
def test_valid_chassis_acknowledge(add_mo_mock, commit_mock):
    add_mo_mock.return_value = True
    commit_mock.return_value = True
    handle = UcsHandle('169.254.1.1', 'admin', 'password')

    # Scenario: Chassis 1
    chassis_retval = chassis_acknowledge(handle, 1)
    # Verify we were passed back the correct object type
    assert isinstance(chassis_retval, EquipmentChassis)
    # Verify the id we requested was assigned correctly
    assert chassis_retval.id == "1"
    # Verify the state we requested is "re-acknowledge"
    assert chassis_retval.admin_state == "re-acknowledge"
