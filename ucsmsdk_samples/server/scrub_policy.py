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


def scrub_policy_create(handle, name, flex_flash_scrub="no",
                        bios_settings_scrub="no", disk_scrub="no", descr="",
                        parent_dn="org-root"):
    """
    This method creates scrub policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the scrub policy.
        flex_flash_scrub (string): "yes" or "no"
        bios_settings_scrub (string): "yes" or "no"
        disk_scrub (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        ComputeScrubPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        scrub_policy_create(handle, name="sample_scrub",
                            flex_flash_scrub="yes", bios_settings_scrub="no",
                            parent_dn="org-root/org-sub")

    """

    from ucsmsdk.mometa.compute.ComputeScrubPolicy import ComputeScrubPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = ComputeScrubPolicy(parent_mo_or_dn=obj,
                            flex_flash_scrub=flex_flash_scrub,
                            name=name,
                            descr=descr,
                            bios_settings_scrub=bios_settings_scrub,
                            disk_scrub=disk_scrub)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def scrub_policy_modify(handle, name, flex_flash_scrub=None,
                        bios_settings_scrub=None, disk_scrub=None, descr=None,
                        parent_dn="org-root"):
    """
    This method modify scrub policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the scrub policy.
        flex_flash_scrub (string): "yes" or "no"
        bios_settings_scrub (string): "yes" or "no"
        disk_scrub (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        ComputeScrubPolicy: Managed Object

    Raises:
        ValueError: If ComputeScrubPolicy is not present

    Example:
        scrub_policy_modify(handle, name="sample_scrub",
                            flex_flash_scrub="yes", bios_settings_scrub="no",
                            parent_dn="org-root/org-sub")

    """

    dn = parent_dn + "/scrub-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("scrub policy '%s' does not exist" % dn)

    if flex_flash_scrub is not None:
        mo.flex_flash_scrub = flex_flash_scrub
    if bios_settings_scrub is not None:
        mo.bios_settings_scrub = bios_settings_scrub
    if disk_scrub is not None:
        mo.disk_scrub = disk_scrub
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def scrub_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes scrub policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the scrub policy.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If ComputeScrubPolicy is not present

    Example:
        scrub_policy_remove(handle, name="sample_scrub",
                            parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/scrub-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("scrub policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def scrub_policy_exist(handle, name, flex_flash_scrub="no",
                       bios_settings_scrub="no", disk_scrub="no", descr="",
                       parent_dn="org-root"):
    """
    This method checks if scrub policy exist.

    Args:
        handle (UcsHandle)
        name (string): Name of the scrub policy.
        flex_flash_scrub (string): "yes" or "no"
        bios_settings_scrub (string): "yes" or "no"
        disk_scrub (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Example:
        scrub_policy_exist(handle, name="sample_scrub",
                           flex_flash_scrub="yes", bios_settings_scrub="no",
                           parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/scrub-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((disk_scrub and mo.disk_scrub != disk_scrub) and
            (flex_flash_scrub and mo.flex_flash_scrub != flex_flash_scrub) and
            (bios_settings_scrub and mo.bios_settings_scrub !=
                bios_settings_scrub) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
