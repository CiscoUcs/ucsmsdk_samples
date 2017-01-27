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

"""
This module contains the methods required for creating uplink ports.
"""


def uplink_port_create(handle, dn, port_id, slot_id):
    """
    This method configures the port as an uplink port

    Args:
         handle (Handle)
         dn (string): parent_dn
         port_id (number): Port id of the port
         slot_id (number): Slot id of the port

    Returns:
        FabricEthLanEp

    Example:
        uplink_port_create(handle, dn=fabric/lan/A, port_id=10,
                          slot_id=1)
    """

    from ucsmsdk.mometa.fabric.FabricEthLanEp import \
        FabricEthLanEp

    mo = FabricEthLanEp(parent_mo_or_dn=dn, slot_id=slot_id, port_id=port_id)
    handle.add_mo(mo, modify_present=False)
    handle.commit()
    return mo
