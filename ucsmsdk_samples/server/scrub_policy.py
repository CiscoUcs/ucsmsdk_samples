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


def scrub_policy_create(handle, name, flex_flash_scrub="no",
                        bios_settings_scrub="no",
                        disk_scrub="no", descr="", parent_dn="org-root"):
    """
    This method creates scrub policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the scrub policy.
        flex_flash_scrub (string): "yes" or "no"
        bios_settings_scrub (string): "yes" or "no"
        disk_scrub (string): "yes" or "no"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        scrub_policy_create(handle, org_name="sample-org",
                                name="sample_scrub", flex_flash_scrub="yes",
                                bios_settings_scrub="no")

    """

    obj = handle.query_dn(parent_dn)
    if obj:
        from ucsmsdk.mometa.compute.ComputeScrubPolicy import ComputeScrubPolicy

        mo = ComputeScrubPolicy(parent_mo_or_dn=parent_dn,
                                flex_flash_scrub=flex_flash_scrub,
                                name=name,
                                descr=descr,
                                bios_settings_scrub=bios_settings_scrub,
                                disk_scrub=disk_scrub)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" %org_name)


def scrub_policy_modify(handle, org_name, name, flex_flash_scrub=None,
                        bios_settings_scrub=None,
                        disk_scrub=None, descr=None, org_parent="org-root"):
    """
    This method creates scrub policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the scrub policy.
        flex_flash_scrub (string): "yes" or "no"
        bios_settings_scrub (string): "yes" or "no"
        disk_scrub (string): "yes" or "no"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        scrub_policy_modify(handle, org_name="sample-org",
                                name="sample_scrub", flex_flash_scrub="yes",
                                bios_settings_scrub="no")

    """

    org_dn = org_parent + "/org-" + org_name
    policy_dn= org_dn + "/scrub-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        if flex_flash_scrub is not None:
            mo.flex_flash_scrub= flex_flash_scrub
        if bios_settings_scrub is not None:
            mo.bios_settings_scrub = bios_settings_scrub
        if disk_scrub is not None:
            mo.disk_scrub = disk_scrub
        if descr is not None:
            mo.descr = descr

        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Scrub Policy <%s> not found." % name)


def scrub_policy_remove(handle, org_name, name,org_parent="org-root"):
    """
    This method removes scrub policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the scrub policy.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        scrub_policy_remove(handle, org_name="sample-org",
                                name="sample_scrub")
    """
    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "/scrub-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Scrub Policy <%s> not found.Nothing to remove"%name)
        else:
            handle.remove_mo(mo)
            handle.commit()
