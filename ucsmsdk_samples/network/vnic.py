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
This module contains the methods required for creating vNIC templates.
"""


def vnic_template_create(handle, name, vlans=[], con_policy_type=None,
                         con_policy_name=None, mtu=1500, qos_policy_name="",
                         target="", ident_pool_name="", nw_ctrl_policy_name="",
                         pin_to_group_name="", switch_id="A",
                         stats_policy_name="default",
                         templ_type="initial-template",
                         descr="", parent_dn="org-root"):
    """
    Creates vNIC Template

    Args:
        handle (UcsHandle)
        name (String) : vNIC Template name
        vlans (List) : List of tuples - [(vlan_name, native_vlan)]
        con_policy_type (String) : Connection Policy Type
                                   ["dynamic-vnic","usnic","vmq"]
        con_policy_name (String) : Connection Policy name
        mtu (String)
        qos_policy_name (String) : QoS Policy name
        target (String) : ((vm|adaptor|defaultValue),){0,2}
                            (vm|adaptor|defaultValue){0,1}
        ident_pool_name (String) : MAC Address Pool name
        nw_ctrl_policy_name (String) : Network Control Policy name
        pin_to_group_name (String) : Pin Group name
        switch_id (String) : ["A", "A-B", "B", "B-A", "NONE"]
        stats_policy_name (String) : Stats Threshold Policy name
        templ_type (String) : ["initial-template", "updating-template"]
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        VnicLanConnTempl: Managed Object

    Raises:
        ValueError: If con_policy_type is not in ["dynamic-vnic","usnic","vmq"]
                    Or
                    If OrgOrg is not present

    Example:
        sample_vlans = [("my_vlan","yes"),("lab_vlan","no"),
                        ("sample_vlan","no")]
        vnic_template_create(handle, "sample_vnic_template", sample_vlans,
                             "usnic", "sample_usnic_policy", "1500",
                             "samp_qos_policy", "adaptor,vm", "samp_mac_pool")
    """

    from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
    from ucsmsdk.mometa.vnic.VnicDynamicConPolicyRef import \
        VnicDynamicConPolicyRef
    from ucsmsdk.mometa.vnic.VnicUsnicConPolicyRef import VnicUsnicConPolicyRef
    from ucsmsdk.mometa.vnic.VnicVmqConPolicyRef import VnicVmqConPolicyRef

    from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = VnicLanConnTempl(parent_mo_or_dn=obj,
                              templ_type=templ_type,
                              name=name,
                              descr=descr,
                              stats_policy_name=stats_policy_name,
                              switch_id=switch_id,
                              pin_to_group_name=pin_to_group_name,
                              mtu=mtu,
                              policy_owner="local",
                              qos_policy_name=qos_policy_name,
                              target=target,
                              ident_pool_name=ident_pool_name,
                              nw_ctrl_policy_name=nw_ctrl_policy_name)

        # TODO: Query to check if connection policy exists
        if con_policy_name:
            if con_policy_type.lower() == "dynamic-vnic":
                VnicDynamicConPolicyRef(parent_mo_or_dn=mo,
                                        con_policy_name=con_policy_name)
            elif con_policy_type.lower() == "usnic":
                VnicUsnicConPolicyRef(parent_mo_or_dn=mo,
                                      con_policy_name=con_policy_name)
            elif con_policy_type.lower() == "vmq":
                VnicVmqConPolicyRef(parent_mo_or_dn=mo,
                                    con_policy_name=con_policy_name)
            else:
                raise ValueError(con_policy_type +
                                 " is not a valid Connection Policy type.")

        vlan_mo = []
        if vlans is not None:
            for vlan in vlans:
                # TODO: Query to check if VnicEtherIf exists
                if len(vlan) != 2:
                    raise Exception("Invalid number of VLAN properties. "
                                    "Expect 2 properties. Actual:%d"
                                    % (len(vlan)))
                vlan_name = vlan[0]
                is_native_vlan = vlan[1]
                # TODO: Query to check if VnicEtherIf exists
                vlan_mo.append(VnicEtherIf(parent_mo_or_dn=mo,
                                           name=vlan_name,
                                           default_net=is_native_vlan))

        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        raise ValueError(parent_dn + " MO is not available")
    return mo


def vnic_template_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a vNIC Template

    Args:
        handle (UcsHandle)
        name (string): vnic template name
        parent_dn (String) :

    Returns:
        None

    Raises:
        ValueError: If VnicLanConnTempl is not present

    Example:
        vnic_template_delete(handle, "samp-vnic-tmpl")
    """

    dn = parent_dn + '/lan-conn-templ-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("vNIC Template '%s' is not present" % dn)


def vnic_template_exists(handle, name, con_policy_type=None,
                         con_policy_name=None, mtu=None, qos_policy_name=None,
                         target=None, ident_pool_name=None,
                         nw_ctrl_policy_name=None, pin_to_group_name=None,
                         switch_id=None,
                         stats_policy_name=None, templ_type=None,
                         descr=None, parent_dn="org-root"):
    """
    Checks if the given vNIC template already exists with the same params
    Args:
        handle (UcsHandle)
        name (String) : vNIC Template name
        vlans (List) : List of tuples - [(vlan_name, native_vlan)]
        con_policy_type (String) : Connection Policy Type
                                   ["dynamic-vnic","usnic","vmq"]
        con_policy_name (String) : Connection Policy name
        mtu (String)
        qos_policy_name (String) : QoS Policy name
        target (String) : ((vm|adaptor|defaultValue),){0,2}
                           (vm|adaptor|defaultValue){0,1}
        ident_pool_name (String) : MAC Address Pool name
        nw_ctrl_policy_name (String) : Network Control Policy name
        pin_to_group_name (String) : Pin Group name
        switch_id (String) : ["A", "A-B", "B", "B-A", "NONE"]
        stats_policy_name (String) : Stats Threshold Policy name
        templ_type (String) : ["initial-template", "updating-template"]
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        True/False (Boolean)

    Example:
        sample_vlans = [("my_vlan","yes"),("lab_vlan","no"),
                          ("sample_vlan","no")],
                            bool_var = vnic_template_exists(handle,
                            "sample_vnic_template",
                            sample_vlans, "usnic",
                            "sample_usnic_policy", "1500", "samp_qos_policy",
                            "adaptor,vm", "samp_mac_pool")
    """

    dn = parent_dn + '/lan-conn-templ-' + name
    mo = handle.query_dn(dn)
    # TODO: Compare vlans associated with the vnic template
    if mo:
        if ((con_policy_type and mo.con_policy_type != con_policy_type) and
            (con_policy_name and mo.con_policy_name != con_policy_name) and
            (mtu and mo.mtu != mtu) and
            (qos_policy_name and mo.qos_policy_name != qos_policy_name) and
            (target and mo.target != target) and
            (ident_pool_name and mo.ident_pool_name != ident_pool_name) and
            (nw_ctrl_policy_name and mo.nw_ctrl_policy_name
                != nw_ctrl_policy_name) and
            (pin_to_group_name and mo.pin_to_group_name
                != pin_to_group_name) and
            (switch_id and mo.switch_id != switch_id) and
            (stats_policy_name and mo.stats_policy_name
                != stats_policy_name) and
            (templ_type and mo.templ_type != templ_type) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
