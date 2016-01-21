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
import logging
log = logging.getLogger('ucs')


def lan_conn_policy_create(handle, name, descr="", parent_dn="org-root"):

    """
    Creates LAN Connectivity Policy

    Args:
        handle (UcsHandle)
        name (String) : LAN Connectivity Policy name
        descr (String) :
        parent_dn (String) :

    Returns:
        None

    Example:
        lan_conn_policy_create(handle, "samp_conn_pol2")
        add_vnic(handle, "org-root/lan-conn-pol-samp_conn_pol2", "test_vnic", "vinbs_nw", "ANY",
                "any", "default", "wqdwq", "A", "", "1500")
    """

    from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = VnicLanConnPolicy(parent_mo_or_dn=obj,
                               policy_owner="local",
                               name=name,
                               descr=descr)

        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info(parent_dn + " MO is not available")


def lan_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a LAN Connectivity Policy
    Args:
        handle (UcsHandle)
        name (string)
        parent_dn (String) :
    Returns:
        None
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
    Checks if the given LAN Connectivity Policy already exists with the same params
    Args:
        handle (UcsHandle)
        name (String) : LAN Connectivity Policy name
        descr (String) :
        parent_dn (String) :
    Returns:
        True/False (Boolean)
    Example:
        bool_var = lan_conn_policy_exists(handle, "samp_conn_pol2")
    """
    dn = parent_dn + '/lan-conn-pol-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((descr and mo.descr != descr)):
            return False
        return True
    return False

def add_vnic(handle, parent_dn,  name, nw_ctrl_policy_name="", admin_host_port="ANY",
             admin_vcon="any", stats_policy_name="default", admin_cdn_name="",
             switch_id="A", pin_to_group_name="", mtu="1500", qos_policy_name="",
             adaptor_profile_name="", ident_pool_name="", order="1", nw_templ_name="", addr="derived"):

    """
    Adds vNIC to LAN Connectivity Policy

    Args:
        handle
        parent_dn
        name
        nw_ctrl_policy_name
        admin_host_port
        admin_vcon
        stats_policy_name
        admin_cdn_name
        switch_id
        pin_to_group_name
        mtu
        qos_policy_name
        adaptor_profile_name
        ident_pool_name
        order
        nw_templ_name
        addr

    Returns:
        None

    Example:
        add_vnic(handle, "org-root/lan-conn-pol-samp_conn_pol2", "test_vnic", "vinbs_nw", "ANY",
                "any", "default", "wqdwq", "A", "", "1500")
    """

    from ucsmsdk.mometa.vnic.VnicEther import VnicEther

    obj = handle.query_dn(parent_dn)
    if obj:
        mo_1 = VnicEther(parent_mo_or_dn=obj,
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

        handle.add_mo(mo_1, modify_present=True)
        handle.commit()
    else:
        log.info(parent_dn + " MO is not available")


def remove_vnic(handle, name, parent_dn):
    """
    Remove vNIC from LAN Connectivity Policy
    Args:
        handle (UcsHandle)
        name (string)
        parent_dn (String) :
    Returns:
        None
    Example:
        remove_vnic(handle, "sample-vnic","org-root/lan-conn-pol-samp_conn_pol")
    """

    dn = parent_dn + '/ether-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("vNIC Mo is not present")


def vnic_exists(handle, parent_dn,  name, nw_ctrl_policy_name=None, admin_host_port=None,
             admin_vcon=None, stats_policy_name=None, admin_cdn_name=None,
             switch_id=None, pin_to_group_name=None, mtu=None, qos_policy_name=None,
             adaptor_profile_name=None, ident_pool_name=None, order=None, nw_templ_name=None, addr=None):
    """
    Checks if the given vNIC already exists with the same params under a given Lan Connectivity Policy
    Args:
        handle
        parent_dn
        name
        nw_ctrl_policy_name
        admin_host_port
        admin_vcon
        stats_policy_name
        admin_cdn_name
        switch_id
        pin_to_group_name
        mtu
        qos_policy_name
        adaptor_profile_name
        ident_pool_name
        order
        nw_templ_name
        addr
    Returns:
        True/False (Boolean)
    Example:
        vnic_exists(handle, "org-root/lan-conn-pol-samp_conn_pol2", "test_vnic", "vinbs_nw", "ANY",
                "any", "default", "wqdwq", "A", "", "1500")
    """
    dn = parent_dn + '/ether-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((nw_ctrl_policy_name and mo.nw_ctrl_policy_name != nw_ctrl_policy_name) and
            (admin_host_port and mo.admin_host_port != admin_host_port) and
            (admin_vcon and mo.admin_vcon != admin_vcon) and
            (admin_cdn_name and mo.admin_cdn_name != admin_cdn_name) and
            (switch_id and mo.switch_id != switch_id) and
            (pin_to_group_name and mo.pin_to_group_name != pin_to_group_name) and
            (mtu and mo.mtu != mtu) and
            (qos_policy_name and mo.qos_policy_name != qos_policy_name) and
            (adaptor_profile_name and mo.adaptor_profile_name != adaptor_profile_name) and
            (ident_pool_name and mo.ident_pool_name != ident_pool_name) and
            (order and mo.order != order) and
            (nw_templ_name and mo.nw_templ_name != nw_templ_name) and
            (addr and mo.addr != addr)):
            return False
        return True
    return False


def add_vnic_iscsi(handle, parent_dn, name, addr="derived", admin_host_port="ANY",
                     admin_vcon="any", stats_policy_name="default", admin_cdn_name="",
                     switch_id="A", pin_to_group_name="", vnic_name="", qos_policy_name="",
                     adaptor_profile_name="", ident_pool_name="", order="unspecified",
                     nw_templ_name="", vlan_name="default"):

    """
    Adds iSCSI vNIC to LAN Connectivity Policy

    Args:
        handle
        parent_dn
        name
        addr
        admin_host_port
        admin_vcon
        stats_policy_name
        admin_cdn_name
        switch_id
        pin_to_group_name
        vnic_name
        qos_policy_name
        adaptor_profile_name
        ident_pool_name
        order
        nw_templ_name
        vlan_name

    Returns:
        None

    Example:

    """

    from ucsmsdk.mometa.vnic.VnicIScsiLCP import VnicIScsiLCP
    from ucsmsdk.mometa.vnic.VnicVlan import VnicVlan

    obj = handle.query_dn(parent_dn)
    if obj:
        mo_1 = VnicIScsiLCP(parent_mo_or_dn=obj,
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

        mo_1_1 = VnicVlan(parent_mo_or_dn=mo_1, name="", vlan_name=vlan_name)

        handle.add_mo(mo_1)
        handle.commit()
    else:
        log.info(parent_dn + " MO is not available")


def remove_vnic_iscsi(handle, name, parent_dn):
    """
    Remove iSCSI vNIC from LAN Connectivity Policy
    Args:
        handle (UcsHandle)
        name (string)
        parent_dn (String) :
    Returns:
        None
    Example:
        remove_vnic_iscsi(handle, "sample-vnic-iscsi","org-root/lan-conn-pol-samp_conn_pol")
    """

    dn = parent_dn + '/iscsi-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("iSCSI vNIC Mo is not present")


def vnic_iscsi_exists(handle, parent_dn, name, addr=None, admin_host_port=None,
                     admin_vcon=None, stats_policy_name=None, admin_cdn_name=None,
                     switch_id=None, pin_to_group_name=None, vnic_name=None, qos_policy_name=None,
                     adaptor_profile_name=None, ident_pool_name=None, order=None,
                     nw_templ_name=None, vlan_name=None):
    """
    Checks if the given iSCSI vNIC already exists with the same params under a given Lan Connectivity Policy
    Args:
        handle
        parent_dn
        name
        addr
        admin_host_port
        admin_vcon
        stats_policy_name
        admin_cdn_name
        switch_id
        pin_to_group_name
        vnic_name
        qos_policy_name
        adaptor_profile_name
        ident_pool_name
        order
        nw_templ_name
        vlan_name
    Returns:
        True/False (Boolean)
    Example:
        vnic_iscsi_exists(handle, "org-root/lan-conn-pol-samp_conn_pol2", "test_iscsi_vnic")
    """
    dn = parent_dn + '/iscsi-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((addr and mo.addr != addr) and
            (admin_host_port and mo.admin_host_port != admin_host_port) and
            (admin_vcon and mo.admin_vcon != admin_vcon) and
            (stats_policy_name and mo.stats_policy_name != stats_policy_name) and
            (admin_cdn_name and mo.admin_cdn_name != admin_cdn_name) and
            (switch_id and mo.switch_id != switch_id) and
            (pin_to_group_name and mo.pin_to_group_name != pin_to_group_name) and
            (vnic_name and mo.vnic_name != vnic_name) and
            (qos_policy_name and mo.qos_policy_name != qos_policy_name) and
            (adaptor_profile_name and mo.adaptor_profile_name != adaptor_profile_name) and
            (ident_pool_name and mo.ident_pool_name != ident_pool_name) and
            (order and mo.order != order) and
            (nw_templ_name and mo.nw_templ_name != nw_templ_name) and
            (vlan_name and mo.vlan_name != vlan_name)):
            return False
        return True
    return False