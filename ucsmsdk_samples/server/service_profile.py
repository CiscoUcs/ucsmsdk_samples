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

import logging
log = logging.getLogger('ucs')


def sp_template_create(handle,
                       name, type, resolve_remote,
                       vmedia_policy_name="",
                       ext_ip_state="none",
                       bios_profile_name="",
                       mgmt_fw_policy_name="",
                       agent_policy_name="",
                       mgmt_access_policy_name="",
                       dynamic_con_policy_name="",
                       kvm_mgmt_policy_name="",
                       sol_policy_name="",
                       descr="",
                       stats_policy_name="",
                       ext_ip_pool_name="",
                       boot_policy_name="",
                       usr_lbl="",
                       host_fw_policy_name="",
                       vcon_profile_name="",
                       ident_pool_name="",
                       src_templ_name="",
                       local_disk_policy_name="",
                       scrub_policy_name="",
                       power_policy_name="",
                       maint_policy_name="",
                       lan_conn_policy_name="",
                       san_conn_policy_name="",
                       parent_dn="org-root"):

    from ucsmsdk.mometa.ls.LsServer import LsServer
    from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = LsServer(parent_mo_or_dn=parent_dn,
                      vmedia_policy_name=vmedia_policy_name,
                      ext_ip_state=ext_ip_state,
                      bios_profile_name=bios_profile_name,
                      mgmt_fw_policy_name=mgmt_fw_policy_name,
                      agent_policy_name=agent_policy_name,
                      mgmt_access_policy_name=mgmt_access_policy_name,
                      dynamic_con_policy_name=dynamic_con_policy_name,
                      kvm_mgmt_policy_name=kvm_mgmt_policy_name,
                      sol_policy_name=sol_policy_name,
                      descr=descr,
                      stats_policy_name=stats_policy_name,
                      ext_ip_pool_name=ext_ip_pool_name,
                      boot_policy_name=boot_policy_name,
                      usr_lbl=usr_lbl,
                      host_fw_policy_name=host_fw_policy_name,
                      vcon_profile_name=vcon_profile_name,
                      ident_pool_name=ident_pool_name,
                      src_templ_name=src_templ_name,
                      type=type,
                      local_disk_policy_name=local_disk_policy_name,
                      scrub_policy_name=scrub_policy_name,
                      power_policy_name=power_policy_name,
                      maint_policy_name=maint_policy_name,
                      name=name,resolve_remote=resolve_remote)
        handle.add_mo(mo, modify_present=True)
        vnicConnDefMo = VnicConnDef(
					parent_mo_or_dn=mo,
					lan_conn_policy_name=lan_conn_policy_name,
					san_conn_policy_name=san_conn_policy_name)
        handle.add_mo(vnicConnDefMo, modify_present=True)
        handle.commit()
    else:
        log.info("Parent Org not found")

def sp_template_modify(handle,org_name,
                       name, type=None, resolve_remote=None,
                       vmedia_policy_name=None,
                       ext_ip_state=None,
                       bios_profile_name=None,
                       mgmt_fw_policy_name=None,
                       agent_policy_name=None,
                       mgmt_access_policy_name=None,
                       dynamic_con_policy_name=None,
                       kvm_mgmt_policy_name=None,
                       sol_policy_name=None,
                       descr=None,
                       stats_policy_name=None,
                       ext_ip_pool_name=None,
                       boot_policy_name=None,
                       usr_lbl=None,
                       host_fw_policy_name=None,
                       vcon_profile_name=None,
                       ident_pool_name=None,
                       src_templ_name=None,
                       local_disk_policy_name=None,
                       scrub_policy_name=None,
                       power_policy_name=None,
                       maint_policy_name=None,
                       org_parent="org-root"):

    from ucsmsdk.mometa.ls.LsServer import LsServer

    if org_name != "":
        sp_dn = org_parent + "/org-" + org_name + "/ls-" + name
    else:
        sp_dn = org_parent + "/ls-" + name
    mo = handle.query_dn(sp_dn)
    if mo is not None:
        if vmedia_policy_name is not None:
            mo.vmedia_policy_name = vmedia_policy_name
        if ext_ip_state is not None:
            mo.ext_ip_state=ext_ip_state
        if bios_profile_name is not None:
            mo.bios_profile_name=bios_profile_name
        if mgmt_fw_policy_name is not None:
            mo.mgmt_fw_policy_name=mgmt_fw_policy_name
        if agent_policy_name is not None:
            mo.agent_policy_name=agent_policy_name
        if mgmt_access_policy_name is not None:
            mo.mgmt_access_policy_name=mgmt_access_policy_name
        if dynamic_con_policy_name is not None:
            mo.dynamic_con_policy_name=dynamic_con_policy_name
        if kvm_mgmt_policy_name is not None:
            mo.kvm_mgmt_policy_name=kvm_mgmt_policy_name
        if sol_policy_name is not None:
            mo.sol_policy_name=sol_policy_name
        if descr is not None:
            mo.descr=descr
        if stats_policy_name is not None:
            mo.stats_policy_name=stats_policy_name
        if ext_ip_pool_name is not None:
            mo.ext_ip_pool_name=ext_ip_pool_name
        if boot_policy_name is not None:
            mo.boot_policy_name=boot_policy_name
        if usr_lbl is not None:
            mo.usr_lbl=usr_lbl
        if host_fw_policy_name is not None:
            mo.host_fw_policy_name=host_fw_policy_name
        if vcon_profile_name is not None:
            mo.vcon_profile_name=vcon_profile_name
        if ident_pool_name is not None:
            mo.ident_pool_name=ident_pool_name
        if src_templ_name is not None:
            mo.src_templ_name=src_templ_name
        if type is not None:
            mo.type=type
        if local_disk_policy_name is not None:
            mo.local_disk_policy_name=local_disk_policy_name
        if scrub_policy_name is not None:
            mo.scrub_policy_name=scrub_policy_name
        if power_policy_name is not None:
            mo.power_policy_name=power_policy_name
        if maint_policy_name is not None:
            mo.maint_policy_name=maint_policy_name
        if resolve_remote is not None:
            mo.resolve_remote=resolve_remote
        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Service Profile Template not found.")


def sp_vcon_assign_vnic(handle, sp_name, admin_vcon, vnic_name,
                   order, transport="ethernet", org_dn="org-root"):

    from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
    ls_dn = org_dn + "/ls-" + sp_name
    obj = handle.query_dn(ls_dn)
    if obj:
        mo = LsVConAssign(parent_mo_or_dn=ls_dn, admin_vcon=admin_vcon,
                          order=order, transport=transport,
                          vnic_name=vnic_name)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("SP not found.Can not add.")


def sp_vcon_remove_vnic(handle, org_name, sp_name, vnic_name,
                        transport="ethernet",
                        org_parent="org-root"):
    from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
    if org_name != "":
        org_dn = org_parent + "/org-" + org_name + "/ls-" + sp_name
    else:
        org_dn = org_parent + "/ls-" + sp_name
    parent_mo = handle.query_dn(org_dn)
    if parent_mo:
        mo = LsVConAssign(parent_mo_or_dn=org_dn, admin_vcon="any",
                          order="unspecified",transport=transport,
                          vnic_name=vnic_name)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("SP not found.")


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
        org_name (string): Name of the organization
        naming_prefix (string): Suffix name of service profile.
        name_suffix_starting_number (string): Starting Number for Suffix
        number_of_instance (string): Total number of instances to be created.
        sp_template_name (string): SP template name.
        in_error_on_existing (string): "true" or "false"
        parent_dn (string): Parent of Org.

    Returns:
        None

    Example:
        sp_create_from_template(handle, org_name="sample-org",
                         naming_prefix="sample_sp",name_suffix_starting_number="1",
                         number_of_instance="3",sp_template_name="sample_temp",
                         in_error_on_existing="true")

    """

    from ucsmsdk.ucsmethodfactory import ls_instantiate_n_named_template
    from ucsmsdk.ucsbasetype import DnSet, Dn

    sp_template_dn = parent_dn + "/ls-" + sp_template_name
    mo = handle.query_dn(sp_template_dn)
    if mo is None:
        raise ValueError("SP template does not exist.")

    dn_set = DnSet()
    for num in range(int(name_suffix_starting_number),
                     int(number_of_instance) +
                     int(name_suffix_starting_number)):
        dn = Dn()
        sp_name = naming_prefix + str(num)
        dn.attr_set("value", sp_name)
        dn_set.child_add(dn)

    elem = ls_instantiate_n_named_template(cookie=handle.cookie,
                                   dn=sp_template_dn,
                                   in_error_on_existing=in_error_on_existing,
                                   in_name_set=dn_set,
                                   in_target_org=parent_dn)
    return handle.process_xml_elem(elem)


def sp_remove(handle, org_name, sp_name, org_parent="org-root"):
    """
    This method instantiate Service profile from a template.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        sp_name (string): Service Profile  name.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        a. If service profile or template is under some Sub-Org
            sp_remove(handle, org_name="sample-org",sp_name="sample_sp")

        b. If service profile or template is not under any sub-org.
            sp_remove(handle, org_name="", sp_name="sample_sp")
    """

    if org_name != "":
        dn = org_parent + "/org-" + org_name + "/ls-" + sp_name
    else:
        dn = org_parent + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if mo is not None:
        handle.remove_mo(mo)
        handle.commit()
    else:
        log.info("SP  %s not found.Nothing to remove" % sp_name)
