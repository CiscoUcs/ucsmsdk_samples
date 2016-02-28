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
This module performs the operation under
LAN -> Policies -> root -> Multicast Policies.
"""


def mcast_policy_create(handle, name, querier_state, snooping_state,
                        querier_ip_addr="0.0.0.0",
                        querier_ip_addr_peer="0.0.0.0",
                        descr="", parent_dn="org-root"):
    """
    Creates Multicast Policy

    Args:
        handle (UcsHandle)
        name (string)
        querier_state (String) : ["disabled", "enabled"]
        snooping_state (String) : ["disabled", "enabled"]
        querier_ip_addr (String)
        querier_ip_addr_peer (String)
        descr (String)
        parent_dn (String) :

    Returns:
        FabricMulticastPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        mcast_policy_create(handle, "my_mcast", "disabled", "enabled")
    """

    from ucsmsdk.mometa.fabric.FabricMulticastPolicy import \
        FabricMulticastPolicy

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = FabricMulticastPolicy(
            parent_mo_or_dn=obj,
            querier_ip_addr=querier_ip_addr,
            querier_ip_addr_peer=querier_ip_addr_peer,
            name=name,
            descr=descr,
            querier_state=querier_state,
            snooping_state=snooping_state,
            policy_owner="local")

        handle.add_mo(mo, modify_present=True)
        handle.commit()
        return mo
    else:
        raise ValueError(parent_dn + " MO is not available")


def mcast_policy_exists(handle, name, snooping_state=None, querier_state=None,
                        querier_ip_addr=None, descr=None,
                        parent_dn="org-root"):
    """
    Checks if the mcast policy object exists

    Args:
        handle (Ucshandle)
        name (string): name of the policy
        parent_dn (string): org in which to create the policy

    Returns:
        True/False: Boolean

    Example:
        bool_var = mcast_policy_exists(handle, "demo")
        bool_var = mcast_policy_exists(handle, "demo", "org-root/org-demo")
    """

    dn = parent_dn + '/mc-policy-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((snooping_state and mo.snooping_state != snooping_state) and
                (querier_state and mo.querier_state != querier_state) and
                (querier_ip_addr and mo.querier_ip_addr != querier_ip_addr) and
                (descr and mo.descr != descr)):
            return False
        return True
    return False


def mcast_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a Multicast Policy

    Args:
        handle (UcsHandle)
        name (string)
        parent_dn (String) :

    Returns:
        None

    Raises:
        ValueError: If FabricMulticastPolicy is not present

    Example:
        mcast_policy_delete(handle, "my_mcast")
        mcast_policy_delete(handle, "my_mcast", "org-root/org-demo")
    """

    dn = parent_dn + '/mc-policy-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Mcast policy Mo is not present")
