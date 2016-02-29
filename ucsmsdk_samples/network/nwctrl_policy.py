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
This module contains methods required for creating network control policies.
"""


def nw_control_policy_create(handle, name, cdp, mac_register_mode,
                             uplink_fail_action, forge, lldp_transmit,
                             lldp_receive, descr="", parent_dn="org-root"):
    """
    Creates Network Control Policy

    Args:
        handle (UcsHandle)
        name (String) : Network Control Policy Name
        cdp (String) : ["disabled", "enabled"]
        mac_register_mode (String): ["all-host-vlans", "only-native-vlan"]
        uplink_fail_action (String) : ["link-down", "warning"]
        forge (string) : ["allow", "deny"]
        lldp_transmit (String) : ["disabled", "enabled"]
        lldp_receive (String) : ["disabled", "enabled"]
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        NwctrlDefinition: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        nw_control_policy_create(handle, "sample_nwcontrol_policy",
                                "enabled", "all-host-vlans",
                                "link-down", "allow", "disabled", "disabled")
    """

    from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
    from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = NwctrlDefinition(parent_mo_or_dn=obj,
                              lldp_transmit=lldp_transmit,
                              name=name,
                              lldp_receive=lldp_receive,
                              mac_register_mode=mac_register_mode,
                              policy_owner="local",
                              cdp=cdp,
                              uplink_fail_action=uplink_fail_action,
                              descr=descr)
        DpsecMac(parent_mo_or_dn=mo,
                 forge=forge,
                 policy_owner="local",
                 name="",
                 descr="")

        handle.add_mo(mo, modify_present=True)
        handle.commit()
        return mo
    else:
        raise ValueError("Org %s is not available" % parent_dn)


def nw_control_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a Network Control Policy

    Args:
        handle (UcsHandle)
        name (string): name of network control policy
        parent_dn (String) : ord dn

    Returns:
        None

    Raises:
        ValueError: If NwctrlDefinition is not present

    Example:
        nw_control_policy_delete(handle, "my_nw_policy")
        nw_control_policy_delete(handle, "my_nw_policy", "org-root/org-demo")
    """

    dn = parent_dn + '/nwctrl-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Network Control policy Mo is not present")


def nw_control_policy_exists(handle, name, cdp=None, mac_register_mode=None,
                             uplink_fail_action=None, forge=None,
                             lldp_transmit=None, lldp_receive=None,
                             descr=None, parent_dn="org-root"):
    """
    Checks if the given Network Control Policy already exists with the
    same params

    Args:
        handle (UcsHandle)
        name (String) : Network Control Policy Name
        cdp (String) : ["disabled", "enabled"]
        mac_register_mode (String): ["all-host-vlans", "only-native-vlan"]
        uplink_fail_action (String) : ["link-down", "warning"]
        forge (string) : ["allow", "deny"]
        lldp_transmit (String) : ["disabled", "enabled"]
        lldp_receive (String) : ["disabled", "enabled"]
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        True/False (Boolean)

    Example:
        bool_var = nw_control_policy_exists(handle, "sample_nwcontrol_policy",
                                            "enabled", "all-host-vlans",
                                            "link-down", "allow", "disabled",
                                            "disabled")
    """

    dn = parent_dn + '/nwctrl-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((cdp and mo.cdp != cdp) and
            (mac_register_mode and mo.mac_register_mode
                != mac_register_mode) and
            (uplink_fail_action and mo.uplink_fail_action
                != uplink_fail_action) and
            (forge and mo.forge != forge) and
            (lldp_transmit and mo.lldp_transmit != lldp_transmit) and
            (lldp_receive and mo.lldp_receive != lldp_receive) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
