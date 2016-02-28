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
This module contains the methods required for creating LAN Connectivity Policy.
"""


def lan_conn_policy_create(handle, name, descr="", parent_dn="org-root"):
    """
    Creates LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        name (String) : LAN Connectivity Policy name
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        VnicLanConnPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg object is not present

    Example:
        lan_conn_policy_create(handle, "samp_conn_pol2")
        add_vnic(handle, "org-root/lan-conn-pol-samp_conn_pol2",
                "test_vnic", "vinbs_nw", "ANY",
                "any", "default", "wqdwq", "A", "", "1500")
    """

    from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy

    obj = handle.query_dn(parent_dn)
    if obj is None:
        raise ValueError("Org %s not found" % parent_dn)
    mo = VnicLanConnPolicy(parent_mo_or_dn=obj,
                           policy_owner="local",
                           name=name,
                           descr=descr)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def lan_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        name (string): name of lan connection policy
        parent_dn (String) : org dn

    Returns:
        None

    Raises:
        ValueError: If VnicLanConnPolicy object is not present

    Example:
        lan_conn_policy_delete(handle, "sample-lan-conpolicy")
    """

    dn = parent_dn + '/lan-conn-pol-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("LAN Connectivity Policy Mo is not present")


def lan_conn_policy_exists(handle, name, descr=None, parent_dn="org-root"):
    """
    Checks if the given LAN Connectivity Policy already exists with the same
    params

    Args:
        handle (UcsHandle)
        name (String) : LAN Connectivity Policy name
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        True/False (Boolean)

    Example:
        bool_var = lan_conn_policy_exists(handle, "samp_conn_pol2")
    """

    dn = parent_dn + '/lan-conn-pol-' + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def add_vnic(handle, parent_dn,  name, nw_ctrl_policy_name="",
             admin_host_port="ANY", admin_vcon="any",
             stats_policy_name="default", admin_cdn_name="",
             switch_id="A", pin_to_group_name="", mtu="1500",
             qos_policy_name="", adaptor_profile_name="",
             ident_pool_name="", order="1", nw_templ_name="", addr="derived"):

    """
    Adds vNIC to LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        parent_dn (string): dn of VnicLanConnPolicy
        name (string): name of vnic
        nw_ctrl_policy_name (string): network control policy name
        admin_host_port (number): admin host port
        admin_vcon (string): ["1", "2", "3", "4", "any"]
        stats_policy_name (string): stats policy name
        admin_cdn_name (string): admin cdn name
        switch_id (string): ["A", "A-B", "B", "B-A", "NONE"]
        pin_to_group_name (string): pin to group name
        mtu (number):1500-9000
        qos_policy_name (string): qos policy name
        adaptor_profile_name (string): adaptor profile name
        ident_pool_name (string): ident pool name
        order (string):["unspecified"], ["0-256"]
        nw_templ_name (string): network template name
        addr (string): address

    Returns:
        VnicEther: Managed Object

    Raises:
        ValueError: If VnicLanConnPolicy object is not present

    Example:
        add_vnic(handle, "org-root/lan-conn-pol-samp_conn_pol2", "test_vnic",
                "vinbs_nw", "ANY", "any", "default", "wqdwq", "A", "", "1500")
    """

    from ucsmsdk.mometa.vnic.VnicEther import VnicEther

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = VnicEther(parent_mo_or_dn=obj,
                       nw_ctrl_policy_name=nw_ctrl_policy_name,
                       name=name,
                       admin_host_port=admin_host_port,
                       admin_vcon=admin_vcon,
                       stats_policy_name=stats_policy_name,
                       admin_cdn_name=admin_cdn_name,
                       switch_id=switch_id,
                       pin_to_group_name=pin_to_group_name,
                       mtu=mtu,
                       qos_policy_name=qos_policy_name,
                       adaptor_profile_name=adaptor_profile_name,
                       ident_pool_name=ident_pool_name,
                       order=order,
                       nw_templ_name=nw_templ_name,
                       addr=addr)

        handle.add_mo(mo, modify_present=True)
        handle.commit()
        return mo
    else:
        raise ValueError(parent_dn + " MO is not available")


def remove_vnic(handle, name, parent_dn):
    """
    Remove vNIC from LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        name (string): Name of lan connection policy
        parent_dn (String): lan connection policy dn

    Returns:
        None

    Raises:
        ValueError: If VnicEther object is not present

    Example:
        remove_vnic(handle, "sample-vnic",
                    "org-root/lan-conn-pol-samp_conn_pol")
    """

    dn = parent_dn + '/ether-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("vNIC Mo is not present")


def vnic_exists(handle, parent_dn,  name, nw_ctrl_policy_name=None,
                admin_host_port=None, admin_vcon=None, stats_policy_name=None,
                admin_cdn_name=None, switch_id=None, pin_to_group_name=None,
                mtu=None, qos_policy_name=None, adaptor_profile_name=None,
                ident_pool_name=None, order=None, nw_templ_name=None,
                addr=None):
    """
    Checks if the given vNIC already exists with the same params under a
    given Lan Connectivity Policy

    Args:
        handle (UcsHandle)
        parent_dn (string): dn of VnicLanConnPolicy
        name (string): name of vnic
        nw_ctrl_policy_name (string): network control policy name
        admin_host_port (number): admin host port
        admin_vcon (string): ["1", "2", "3", "4", "any"]
        stats_policy_name (string): stats policy name
        admin_cdn_name (string): admin cdn name
        switch_id (string): ["A", "A-B", "B", "B-A", "NONE"]
        pin_to_group_name (string): pin to group name
        mtu (number):1500-9000
        qos_policy_name (string): qos policy name
        adaptor_profile_name (string): adaptor profile name
        ident_pool_name (string): ident pool name
        order (string):["unspecified"], ["0-256"]
        nw_templ_name (string): network template name
        addr (string): address

    Returns:
        True/False (Boolean)

    Example:
        vnic_exists(handle, "org-root/lan-conn-pol-samp_conn_pol2",
                    "test_vnic", "vinbs_nw", "ANY",
                    "any", "default", "wqdwq", "A", "", "1500")
    """

    dn = parent_dn + '/ether-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((nw_ctrl_policy_name
             and mo.nw_ctrl_policy_name != nw_ctrl_policy_name) and
            (admin_host_port and mo.admin_host_port != admin_host_port) and
            (admin_vcon and mo.admin_vcon != admin_vcon) and
            (stats_policy_name and mo.stats_policy_name !=
                stats_policy_name) and
            (admin_cdn_name and mo.admin_cdn_name != admin_cdn_name) and
            (switch_id and mo.switch_id != switch_id) and
            (pin_to_group_name and mo.pin_to_group_name != pin_to_group_name)
            and
            (mtu and mo.mtu != mtu) and
            (qos_policy_name and mo.qos_policy_name != qos_policy_name) and
            (adaptor_profile_name and mo.adaptor_profile_name !=
                adaptor_profile_name) and
            (ident_pool_name and mo.ident_pool_name != ident_pool_name) and
            (order and mo.order != order) and
            (nw_templ_name and mo.nw_templ_name != nw_templ_name) and
            (addr and mo.addr != addr)):
            return False
        return True
    return False


def add_vnic_iscsi(handle, parent_dn, name, addr="derived",
                   admin_host_port="ANY",
                   admin_vcon="any", stats_policy_name="default",
                   admin_cdn_name="",
                   switch_id="A", pin_to_group_name="", vnic_name="",
                   qos_policy_name="", adaptor_profile_name="",
                   ident_pool_name="", order="unspecified",
                   nw_templ_name="", vlan_name="default"):

    """
    Adds iSCSI vNIC to LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        parent_dn (string): dn of VnicLanConnPolicy
        name (string): iSCSI name
        addr (string): address
        admin_host_port (number): admin host port
        admin_vcon (string): ["1", "2", "3", "4", "any"]
        stats_policy_name (string): stats policy name
        admin_cdn_name (string): admin cdn name
        switch_id (string): ["A", "A-B", "B", "B-A", "NONE"]
        pin_to_group_name (string): pin to group name
        vnic_name (string): vnic name
        qos_policy_name (string): qos policy name
        adaptor_profile_name (string): adaptor profile name
        ident_pool_name (string): ident pool name
        order (string):["unspecified"], ["0-256"]
        nw_templ_name (string): network template name
        vlan_name (string): vlan name

    Returns:
        VnicIScsiLCP: Managed Object

    Raises:
        ValueError: If VnicLanConnPolicy object is not present

    Example:
        add_vnic_iscsi(handle, name="sample-vnic-iscsi",
                    parent_dn="org-root/lan-conn-pol-samp_conn_pol")

    """

    from ucsmsdk.mometa.vnic.VnicIScsiLCP import VnicIScsiLCP
    from ucsmsdk.mometa.vnic.VnicVlan import VnicVlan

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = VnicIScsiLCP(parent_mo_or_dn=obj,
                          addr=addr,
                          admin_host_port=admin_host_port,
                          admin_vcon=admin_vcon,
                          stats_policy_name=stats_policy_name,
                          admin_cdn_name=admin_cdn_name,
                          switch_id=switch_id,
                          pin_to_group_name=pin_to_group_name,
                          vnic_name=vnic_name,
                          qos_policy_name=qos_policy_name,
                          adaptor_profile_name=adaptor_profile_name,
                          ident_pool_name=ident_pool_name,
                          order=order,
                          nw_templ_name=nw_templ_name,
                          name=name)

        VnicVlan(parent_mo_or_dn=mo, name="", vlan_name=vlan_name)

        handle.add_mo(mo)
        handle.commit()
        return mo
    else:
        raise ValueError(parent_dn + " MO is not available")


def remove_vnic_iscsi(handle, name, parent_dn):
    """
    Remove iSCSI vNIC from LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        name (string): iSCSI name
        parent_dn (string): dn of VnicLanConnPolicy

    Returns:
        None

    Raises:
        ValueError: If VnicIScsiLCP object is not present

    Example:
        remove_vnic_iscsi(handle, "sample-vnic-iscsi",
                    "org-root/lan-conn-pol-samp_conn_pol")
    """

    dn = parent_dn + '/iscsi-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("iSCSI vNIC Mo is not present")


def vnic_iscsi_exists(handle, parent_dn, name, addr=None, admin_host_port=None,
                      admin_vcon=None, stats_policy_name=None,
                      admin_cdn_name=None, switch_id=None,
                      pin_to_group_name=None, vnic_name=None,
                      qos_policy_name=None, adaptor_profile_name=None,
                      ident_pool_name=None, order=None, nw_templ_name=None,
                      vlan_name=None):
    """
    Checks if the given iSCSI vNIC already exists with the same params
    under a given Lan Connectivity Policy

    Args:
        handle (UcsHandle)
        parent_dn (string): dn of VnicLanConnPolicy
        name (string): iSCSI name
        addr (string): address
        admin_host_port (number): admin host port
        admin_vcon (string): ["1", "2", "3", "4", "any"]
        stats_policy_name (string): stats policy name
        admin_cdn_name (string): admin cdn name
        switch_id (string): ["A", "A-B", "B", "B-A", "NONE"]
        pin_to_group_name (string): pin to group name
        vnic_name (string): vnic name
        qos_policy_name (string): qos policy name
        adaptor_profile_name (string): adaptor profile name
        ident_pool_name (string): ident pool name
        order (string):["unspecified"], ["0-256"]
        nw_templ_name (string): network template name
        vlan_name (string): vlan name

    Returns:
        True/False (Boolean)

    Example:
        vnic_iscsi_exists(handle, "org-root/lan-conn-pol-samp_conn_pol2",
                        "test_iscsi_vnic")
    """

    dn = parent_dn + '/iscsi-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((addr and mo.addr != addr) and
            (admin_host_port and mo.admin_host_port != admin_host_port) and
            (admin_vcon and mo.admin_vcon != admin_vcon) and
            (stats_policy_name and mo.stats_policy_name != stats_policy_name)
            and
            (admin_cdn_name and mo.admin_cdn_name != admin_cdn_name) and
            (switch_id and mo.switch_id != switch_id) and
            (pin_to_group_name and mo.pin_to_group_name != pin_to_group_name)
            and
            (vnic_name and mo.vnic_name != vnic_name) and
            (qos_policy_name and mo.qos_policy_name != qos_policy_name) and
            (adaptor_profile_name and mo.adaptor_profile_name !=
                adaptor_profile_name) and
            (ident_pool_name and mo.ident_pool_name != ident_pool_name) and
            (order and mo.order != order) and
            (nw_templ_name and mo.nw_templ_name != nw_templ_name) and
            (vlan_name and mo.vlan_name != vlan_name)):
            return False
        return True
    return False
