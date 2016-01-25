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
This module performs the operation under LAN -> LAN Cloud.
"""
import logging
log = logging.getLogger('ucs')


def vlan_create(handle, name, vlan_id, sharing="none",
                mcast_policy_name="", compression_type="included",
                default_net="no", pub_nw_name="", parent_dn="fabric/lan"):
    """
    # LAN
    # - LAN Cloud

    Creates VLAN

    Args:
        handle (UcsHandle)
        sharing (String) : ["community", "isolated", "none", "primary"]
        name (String) : VLAN Name
        vlan_id (String): VLAN ID
        mcast_policy_name (String) : Multicast Policy Name
        compression_type (string) : ["excluded", "included"]
        default_net (String) : ["false", "no", "true", "yes"]
        pub_nw_name (String) :
        parent_dn (String) :

    Returns:
        None

    Example:
        vlan_create(handle, "none", "vlan-lab", "123",  "sample_mcast_policy", "included")
    """
    from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan

    obj = handle.query_dn(parent_dn)
    if obj:
        vlan = FabricVlan(parent_mo_or_dn=obj,
                          sharing=sharing,
                          name=name,
                          id=vlan_id,
                          mcast_policy_name=mcast_policy_name,
                          policy_owner="local",
                          default_net=default_net,
                          pub_nw_name=pub_nw_name,
                          compression_type=compression_type)

        handle.add_mo(vlan, modify_present=True)
        handle.commit()
    else:
        log.info(parent_dn + " MO is not available")


def vlan_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a VLAN
    Args:
        handle (UcsHandle)
        name (string)
        parent_dn (String) :
    Returns:
        None
    Example:
        vlan_delete(handle, "lab-vlan")
    """

    dn = parent_dn + '/net-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("VLAN Mo is not present")


def vlan_exists(handle, name, vlan_id=None, sharing=None,
                mcast_policy_name=None, compression_type=None,
                default_net=None, pub_nw_name=None, parent_dn="fabric/lan"):
    """
    Checks if the given VLAN already exists with the same params
    Args:
        handle (UcsHandle)
        sharing (String) : ["community", "isolated", "none", "primary"]
        name (String) : VLAN Name
        vlan_id (String): VLAN ID
        mcast_policy_name (String) : Multicast Policy Name
        compression_type (string) : ["excluded", "included"]
        default_net (String) : ["false", "no", "true", "yes"]
        pub_nw_name (String) :
        parent_dn (String) :
    Returns:
        True/False (Boolean)
    Example:
        bool_var = vlan_exists(handle, "none", "vlan-lab", "123",  "sample_mcast_policy", "included")
    """
    dn = parent_dn + '/net-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((vlan_id and mo.vlan_id != vlan_id) and
            (sharing and mo.sharing != sharing) and
            (mcast_policy_name and mo.mcast_policy_name != mcast_policy_name) and
            (compression_type and mo.compression_type != compression_type) and
            (default_net and mo.default_net != default_net) and
            (pub_nw_name and mo.pub_nw_name != pub_nw_name)):
            return False
        return True
    return False