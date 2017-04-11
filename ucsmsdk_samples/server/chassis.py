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

from ucsmsdk.mometa.equipment.EquipmentChassis import EquipmentChassis


def chassis_acknowledge(handle, chassis_id):
    """
    This method will acknowledge a given chassis attached
    to the fabric.  When new chassis are added to the system,
    they must be acknowledged before the blades within them
    will be discovered.  So this step should be performed
    just after configure the server ports that connect to
    the chassis.

    Args:
        handle (UcsHandle)
        chassis_id (int): Rack Unit ID of server to configure

    Returns:
       EquipmentChassis

    Example:
        chassis_acknowledge(handle, 1)

    """

    mo = EquipmentChassis(parent_mo_or_dn="sys", admin_state="re-acknowledge",
                          id=str(chassis_id))
    handle.add_mo(mo, True)
    handle.commit()
    return mo
