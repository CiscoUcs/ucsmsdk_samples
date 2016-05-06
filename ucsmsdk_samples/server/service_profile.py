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



def sp_template_create(handle, name, type, resolve_remote, descr="",
                       usr_lbl="", src_templ_name="", ext_ip_state="none",
                       ext_ip_pool_name="", ident_pool_name="",
                       agent_policy_name="",
                       bios_profile_name="",
                       boot_policy_name="",
                       dynamic_con_policy_name="",
                       host_fw_policy_name="",
                       kvm_mgmt_policy_name="",
                       lan_conn_policy_name="",
                       local_disk_policy_name="",
                       maint_policy_name="",
                       mgmt_access_policy_name="",
                       mgmt_fw_policy_name="",
                       power_policy_name="",
                       san_conn_policy_name="",
                       scrub_policy_name="",
                       sol_policy_name="",
                       stats_policy_name="",
                       vcon_profile_name="",
                       vmedia_policy_name="",
                       parent_dn="org-root"):
    """
    This method creates Service profile template.

    Args:
        handle (UcsHandle)
        name(string): Name of SP template
        type : "initial-template", "updating-template"
        resolve_remote : "no", "yes"
        descr (string): Basic description
        src_templ_name (string): Name of Source template
        ext_ip_state= :none", "pooled", "static"
        ext_ip_pool_name (string): Name of IP Pool
        ident_pool_name (string): Name of Ident pool 
        agent_policy_name (string): Name of agent policy
        bios_profile_name (string): Name of bios profile
        boot_policy_name (string): Name of boot policy
        dynamic_con_policy_name (string): Name of dynamic connection policy
        host_fw_policy_name (string):  Name of Host firmware.
        kvm_mgmt_policy_name (string): KVM management policy
        lan_conn_policy_name (string): LAN connection policy
        local_disk_policy_name (string): Local disk policy
        maint_policy_name (string): Maintenance policy
        mgmt_access_policy_name(string): Access Management policy
        mgmt_fw_policy_name (string): Firmware management policy
        power_policy_name (string): Power policy
        san_conn_policy_name (string): SAN connection policy
        scrub_policy_name (string): Scrub policy
        sol_policy_name (string): SOL policy
        stats_policy_name (string): Statistics Policy
        vcon_profile_name (string): Virtual Connection profile policy
        vmedia_policy_name (string): Virtual media policy
        parent_dn= Parent DN
    
    Returns:
        Service Profile: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        sp_template_create(handle, name="sample_temp", type="initial-template",
            resolve_remote="yes",local_disk_policy="sample_local")
    """
    from ucsmsdk.mometa.ls.LsServer import LsServer
    from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist." % parent_dn)

    mo = LsServer(parent_mo_or_dn=obj,
                  name=name,
                  type=type,
                  resolve_remote=resolve_remote,
                  descr=descr,
                  usr_lbl=usr_lbl,
                  src_templ_name=src_templ_name,
                  ext_ip_state=ext_ip_state,
                  ext_ip_pool_name=ext_ip_pool_name,
                  ident_pool_name=ident_pool_name,
                  vcon_profile_name=vcon_profile_name,
                  agent_policy_name=agent_policy_name,
                  bios_profile_name=bios_profile_name,
                  boot_policy_name=boot_policy_name,
                  dynamic_con_policy_name=dynamic_con_policy_name,
                  host_fw_policy_name=host_fw_policy_name,
                  kvm_mgmt_policy_name=kvm_mgmt_policy_name,
                  local_disk_policy_name=local_disk_policy_name,
                  maint_policy_name=maint_policy_name,
                  mgmt_access_policy_name=mgmt_access_policy_name,
                  mgmt_fw_policy_name=mgmt_fw_policy_name,
                  power_policy_name=power_policy_name,
                  scrub_policy_name=scrub_policy_name,
                  sol_policy_name=sol_policy_name,
                  stats_policy_name=stats_policy_name,
                  vmedia_policy_name=vmedia_policy_name
                  )

    vnic_conn_def_mo = VnicConnDef(
        parent_mo_or_dn=mo,
        lan_conn_policy_name=lan_conn_policy_name,
        san_conn_policy_name=san_conn_policy_name)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def sp_template_modify(handle, name, type=None, resolve_remote=None,
                       descr=None, usr_lbl=None, src_templ_name=None,
                       ext_ip_state=None, ext_ip_pool_name=None,
                       ident_pool_name=None, vcon_profile_name=None,
                       agent_policy_name=None, bios_profile_name=None,
                       boot_policy_name=None, dynamic_con_policy_name=None,
                       host_fw_policy_name=None, kvm_mgmt_policy_name=None,
                       local_disk_policy_name=None, maint_policy_name=None,
                       mgmt_access_policy_name=None, mgmt_fw_policy_name=None,
                       power_policy_name=None, scrub_policy_name=None,
                       sol_policy_name=None, stats_policy_name=None,
                       vmedia_policy_name=None,
                       parent_dn="org-root"):
    """
    This method creates Service profile template.

    Args:
        handle (UcsHandle)
        name(string): Name of SP template
        type : "initial-template", "updating-template"
        resolve_remote : "no", "yes"
        descr (string): Basic description
        src_templ_name (string): Name of Source template
        ext_ip_state= :none", "pooled", "static"
        ext_ip_pool_name (string): Name of IP Pool
        ident_pool_name (string): Name of Ident pool 
        agent_policy_name (string): Name of agent policy
        bios_profile_name (string): Name of bios profile
        boot_policy_name (string): Name of boot policy
        dynamic_con_policy_name (string): Name of dynamic connection policy
        host_fw_policy_name (string):  Name of Host firmware.
        kvm_mgmt_policy_name (string): KVM management policy
        lan_conn_policy_name (string): LAN connection policy
        local_disk_policy_name (string): Local disk policy
        maint_policy_name (string): Maintenance policy
        mgmt_access_policy_name(string): Access Management policy
        mgmt_fw_policy_name (string): Firmware management policy
        power_policy_name (string): Power policy
        san_conn_policy_name (string): SAN connection policy
        scrub_policy_name (string): Scrub policy
        sol_policy_name (string): SOL policy
        stats_policy_name (string): Statistics Policy
        vcon_profile_name (string): Virtual Connection profile policy
        vmedia_policy_name (string): Virtual media policy
        parent_dn= Parent DN
    
    Returns:
        LsServer: Managed Object

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_template_modify(handle, name="sample_temp",
                local_disk_policy="sample_local1")
    """

    dn = parent_dn + "/ls-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("SP '%s' does not exist" % dn)

    if type is not None:
        mo.type = type
    if resolve_remote is not None:
        mo.resolve_remote = resolve_remote
    if descr is not None:
        mo.descr = descr
    if usr_lbl is not None:
        mo.usr_lbl = usr_lbl
    if src_templ_name is not None:
        mo.src_templ_name = src_templ_name
    if ext_ip_state is not None:
        mo.ext_ip_state = ext_ip_state
    if ext_ip_pool_name is not None:
        mo.ext_ip_pool_name = ext_ip_pool_name
    if ident_pool_name is not None:
        mo.ident_pool_name = ident_pool_name
    if vcon_profile_name is not None:
        mo.vcon_profile_name = vcon_profile_name
    if agent_policy_name is not None:
        mo.agent_policy_name = agent_policy_name
    if bios_profile_name is not None:
        mo.bios_profile_name = bios_profile_name
    if boot_policy_name is not None:
        mo.boot_policy_name = boot_policy_name
    if dynamic_con_policy_name is not None:
        mo.dynamic_con_policy_name = dynamic_con_policy_name
    if host_fw_policy_name is not None:
        mo.host_fw_policy_name = host_fw_policy_name
    if kvm_mgmt_policy_name is not None:
        mo.kvm_mgmt_policy_name = kvm_mgmt_policy_name
    if local_disk_policy_name is not None:
        mo.local_disk_policy_name = local_disk_policy_name
    if maint_policy_name is not None:
        mo.maint_policy_name = maint_policy_name
    if mgmt_access_policy_name is not None:
        mo.mgmt_access_policy_name = mgmt_access_policy_name
    if mgmt_fw_policy_name is not None:
        mo.mgmt_fw_policy_name = mgmt_fw_policy_name
    if power_policy_name is not None:
        mo.power_policy_name = power_policy_name
    if scrub_policy_name is not None:
        mo.scrub_policy_name = scrub_policy_name
    if sol_policy_name is not None:
        mo.sol_policy_name = sol_policy_name
    if stats_policy_name is not None:
        mo.stats_policy_name = stats_policy_name
    if vmedia_policy_name is not None:
        mo.vmedia_policy_name = vmedia_policy_name

    handle.set_mo(mo)
    handle.commit()
    return mo


def set_inband_mgmt(handle, sp_dn, vlan_name):
    """
    Set mgmt interface mode to "in-band"

    Args:
        handle (UcsHandle)
        sp_dn (string): dn of service profile
        vlan_name (string): name of vlan

    Returns:
        MgmtInterface: Managed Object

    Raises:
        ValueError: If LsServer is not present

    Example:
        set_inband_mgmt(handle, "org-root/ls-testsp", "test_vlan")
    """

    from ucsmsdk.mometa.mgmt.MgmtInterface import MgmtInterface
    from ucsmsdk.mometa.mgmt.MgmtVnet import MgmtVnet
    from ucsmsdk.mometa.vnic.VnicIpV4MgmtPooledAddr import \
        VnicIpV4MgmtPooledAddr

    obj = handle.query_dn(sp_dn)
    if not obj:
        raise ValueError("SP '%s' does not exist" % sp_dn)

    mo = MgmtInterface(parent_mo_or_dn=obj, mode="in-band")
    mo_1 = MgmtVnet(parent_mo_or_dn=mo, name=vlan_name)
    mo_2 = VnicIpV4MgmtPooledAddr(parent_mo_or_dn=mo, name="hyperflex")

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def sp_vcon_assign_vnic(handle, sp_name, vnic_name, admin_vcon, order,
                        transport="ethernet", parent_dn="org-root"):
    """
    Assign vnic to service profile

    Args:
        handle (UcsHandle)
        sp_name (string): dn of service profile
        vnic_name (string): name of vnic
        admin_vcon (string): ["1", "2", "3", "4", "any"]
        order (string): ["unspecified"], ["0-256"]
        transport (string): transport medium
        parent_dn (string): org dn

    Returns:
        LsVConAssign

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_vcon_assign_vnic(handle, sp_name="testsp", vnic_name="testvnic",
                            admin_vcon="1", order="100")
    """

    from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign

    sp_dn = parent_dn + "/ls-" + sp_name
    obj = handle.query_dn(sp_dn)

    if not obj:
        raise ValueError("SP '%s' does not exist" % sp_dn)

    mo = LsVConAssign(parent_mo_or_dn=obj, admin_vcon=admin_vcon,
                      order=order, transport=transport, vnic_name=vnic_name)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def sp_vcon_deassign_vnic(handle, sp_name, vnic_name,
                          transport="ethernet",
                          parent_dn="org-root"):
    """
    Deassign vnic from service profile

    Args:
        handle (UcsHandle)
        sp_name (string): dn of service profile
        vnic_name (string): name of vnic
        transport (string): transport medium
        parent_dn (string): org dn

    Returns:
        LsVConAssign

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_vcon_deassign_vnic(handle, sp_name="testsp", vnic_name="testvnic",
                            transport="ethernet")
    """

    from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign

    sp_dn = parent_dn + "/ls-" + sp_name
    sp = handle.query_dn(sp_dn)
    if not sp:
        raise ValueError("SP '%s' does not exist" % sp_dn)

    mo = LsVConAssign(parent_mo_or_dn=sp, admin_vcon="any",
                      order="unspecified", transport=transport,
                      vnic_name=vnic_name)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def sp_create_from_template(handle,
                            naming_prefix,
                            name_suffix_starting_number,
                            number_of_instance,
                            sp_template_name,
                            in_error_on_existing="true",
                            parent_dn="org-root"):
    """
    This method instantiate Service profile from a template.

    Args:
        handle (UcsHandle)
        naming_prefix (string): Suffix name of service profile.
        name_suffix_starting_number (string): Starting Number for Suffix
        number_of_instance (string): Total number of instances to be created.
        sp_template_name (string): SP template name.
        in_error_on_existing (string): "true" or "false"
        parent_dn (string): Org dn in which service profile template resides.

    Returns:
        None or List of LsServer Objects

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_create_from_template(handle, naming_prefix="sample_sp",
                                name_suffix_starting_number="1",
                                number_of_instance="3",
                                sp_template_name="sample_temp",
                                in_error_on_existing="true",
                                parent_dn="org-root/ls-org_sample")

    """

    import os 

    from ucsmsdk.ucsmethodfactory import ls_instantiate_n_named_template
    from ucsmsdk.ucsbasetype import DnSet, Dn

    mo = None
    org_dn = parent_dn
    while mo is None:
        sp_template_dn = org_dn + "/ls-" + sp_template_name
        mo = handle.query_dn(sp_template_dn)
        if mo:
            break
        elif not mo and org_dn == 'org-root':
            raise ValueError("SP template does not exist.")
        org_dn = os.path.dirname(org_dn)

    dn_set = DnSet()
    for num in range(int(name_suffix_starting_number),
                     int(number_of_instance) +
                     int(name_suffix_starting_number)):
        dn = Dn()
        sp_name = naming_prefix + str(num)
        dn.attr_set("value", sp_name)
        dn_set.child_add(dn)

    elem = ls_instantiate_n_named_template(
        cookie=handle.cookie,
        dn=sp_template_dn,
        in_error_on_existing=in_error_on_existing,
        in_name_set=dn_set,
        in_target_org=parent_dn)
    return handle.process_xml_elem(elem)


def sp_delete(handle, sp_name, parent_dn="org-root"):
    """
    This method delete Service profile.

    Args:
        handle (UcsHandle)

        sp_name (string): Service Profile  name.
        org_parent (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If LsServer is not present

    Example:
        a. If service profile or template is under some Sub-Org
            sp_delete(handle, org_name="sample-org",sp_name="sample_sp")

        b. If service profile or template is not under any sub-org.
            sp_delete(handle, org_name="", sp_name="sample_sp")
    """

    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def sp_power_on(handle, sp_name, parent_dn="org-root"):
    """
    This function will power on a service profile

    Args:
        handle (UcsHandle)

        sp_name (string): Service Profile  name.
        parent_dn (string): Org.

    Returns:
        None

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_power_on(handle, sp_name="sample_sp", parent_dn="org-root")
        sp_power_on(handle, sp_name="sample_sp", parent_dn="org-root/sub-org")
    """

    from ucsmsdk.mometa.ls.LsPower import LsPowerConsts
    from ucsmsdk.mometa.ls.LsPower import LsPower

    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    power_change = LsPower(parent_mo_or_dn=mo, state=LsPowerConsts.STATE_UP)
    handle.set_mo(mo)
    handle.commit()

def sp_power_off(handle, sp_name, parent_dn="org-root"):
    """
    This function will power off a service profile

    Args:
        handle (UcsHandle)

        sp_name (string): Service Profile  name.
        parent_dn (string): Org.

    Returns:
        None

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_power_off(handle, sp_name="sample_sp", parent_dn="org-root")
        sp_power_off(handle, sp_name="sample_sp", parent_dn="org-root/sub-org")
    """

    from ucsmsdk.mometa.ls.LsPower import LsPowerConsts
    from ucsmsdk.mometa.ls.LsPower import LsPower

    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    power_change = LsPower(parent_mo_or_dn=mo, state=LsPowerConsts.STATE_DOWN)
    handle.set_mo(mo)
    handle.commit()

def sp_wwpn(handle, sp_name, parent_dn="org-root"):
    """
    This function will return the fibre channel wwpn addresses of a service profile

    Args:
        handle (UcsHandle)
        sp_name (string): Service Profile  name.
        parent_dn (string): Org.

    Returns:
        dict containing:
        adaptor name
        wwpn address

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_wwpn(handle, sp_name="sample_sp", parent_dn="org-root")
        sp_wwpn(handle, sp_name="sample_sp", parent_dn="org-root/sub-org")
    """

    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    wwpn_dict = {}

    query_data = handle.query_children(in_mo=mo, class_id='VnicFc')
    for item in query_data:
        wwpn_dict[item.name] = item.addr

    return wwpn_dict


def sp_macaddress(handle, sp_name, parent_dn="org-root"):
    """
    This function will return the mac addresses of a service profile

    Args:
        handle (UcsHandle)
        sp_name (string): Service Profile  name.
        parent_dn (string): Org.

    Returns:
        dict containing:
        adaptor name
        mac address

    Raises:
        ValueError: If LsServer is not present

    Example:
        sp_macaddress(handle, sp_name="sample_sp", parent_dn="org-root")
        sp_macaddress(handle, sp_name="sample_sp", parent_dn="org-root/sub-org")
    """
    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    mac_dict = {}

    query_data = handle.query_children(in_mo=mo, class_id='VnicEther')
    for item in query_data:
        mac_dict[item.name] = item.addr

    return mac_dict
