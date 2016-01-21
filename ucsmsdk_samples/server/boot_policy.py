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


def boot_policy_create(handle, name, descr="",
                       reboot_on_update="yes",
                       enforce_vnic_name="yes",
                       boot_mode="legacy",
                       parent_dn="org-root"):

    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        parent_dn (string): Org DN.
        descr (string): Basic description.

    Returns:
        None

    Example:
        boot_policy_create(handle,
                                name="sample_boot",
                                reboot_on_update="yes",
                                boot_mode="legacy",
								parent_dn="org-root/org-finance")
    """

    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = LsbootPolicy(parent_mo_or_dn=parent_dn,
                          name=name, descr=descr,
                          reboot_on_update=reboot_on_update,
                          enforce_vnic_name=enforce_vnic_name,
                          boot_mode=boot_mode)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" %org_name)


def boot_policy_modify(handle, org_name, name, descr=None,
                       reboot_on_update=None,
                       enforce_vnic_name=None,
                       boot_mode=None,
                       parent_dn=None):

    """
    This method modifies boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        org_parent (string): Parent of Org.
        descr (string): Basic description.

    Returns:
        None

    Example:
        boot_policy_modify(handle, org_name="sample_org",
                                name="sample_boot",
                                reboot_on_update="yes",
                                boot_mode="legacy")
    """

    org_dn = org_parent+ "/org-" + org_name
    policy_dn= org_dn + "/boot-policy-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        if descr is not None:
            mo.descr = descr
        if reboot_on_update is not None:
            mo.reboot_on_update = reboot_on_update
        if enforce_vnic_name is not None:
            mo.enforce_vnic_name = enforce_vnic_name
        if boot_mode is not None:
            mo.boot_mode = boot_mode
        if org_parent is not None:
            mo.org_parent = org_parent
    else:
        log.info("Boot Policy <%s> not found." % name)


def boot_policy_remove(handle, org_name, name,org_parent="org-root"):
    """
    This method removes boot policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the boot policy.
        org_parent (string): Parent of Org

    Returns:
        None

    Example:
        boot_policy_remove(handle, org_name="sample_org",
                                name="sample_boot")
    """

    org_dn = org_parent+ "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "/boot-policy-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Boot Policy <%s> not found.Nothing to remove" % name)
        else:
            handle.remove_mo(mo)
            handle.commit()


def boot_policy_add_device(handle, name, parent_dn):
    "Need to add code to this method"
    pass
