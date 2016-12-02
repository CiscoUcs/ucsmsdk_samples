# Copyright 2015 Cisco Systems, Inc.
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

from ucsmsdk.mometa.storage.StorageLocalDisk import StorageLocalDisk


def disk_state_set(handle, rack_id, disk_id, state,
                   controller="storage-SAS-1"):
    """
    This method sets the disk state on rackmount servers
    to either jbod or uncofigured (pre-RAID). This should
    be done before applying  service profile to the server.

    Args:
        handle (UcsHandle)
        rack_id (int): Rack Unit ID of server to configure
        disk_id (int): ID of disk to configure
        state (string): either "unconfigured-good" or "jbod"
        controller (string): The part of the DN string that describes
                             which storage controller to which the disks
                             are connected

    Returns:
       StorageLocalDisk

    Example:
        disk_state_set(handle, 1, 3, "uconfigured-good")

    """

    if state != "unconfigured-good" and state != "jbod":
            raise ValueError('Invalid State: "{0}"'.format(state))

    dn = "sys/rack-unit-{0}/board/{1}".format(rack_id, controller)
    mo = StorageLocalDisk(parent_mo_or_dn=dn, id=str(disk_id),
                          admin_action=state,
                          admin_action_trigger="triggered")
    handle.add_mo(mo, True)
    handle.commit()
    return mo
