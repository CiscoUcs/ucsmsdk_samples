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


def local_disk_policy_create(handle, name, mode="any-configuration",
                             flex_flash_state="enable",
                             flex_flash_raid_reporting_state="enable",
                             protect_config="yes", descr="",
                             parent_dn="org-root"):
    """
    This method creates local disk policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the local disk policy.
        mode (string): Mode of local disk functioning.
        flex_flash_state (string): "enable" or "disable"
        flex_flash_raid_reporting_state (string): "enable" or "disable"
        protect_config (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        StorageLocalDiskConfigPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        local_disk_policy_create(handle, name="sample_l_disk",
                                parent_dn="org-root/org-sub")
    """

    from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import \
        StorageLocalDiskConfigPolicy

    mo = handle.query_dn(parent_dn)
    if not mo:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = StorageLocalDiskConfigPolicy(
        parent_mo_or_dn=mo,
        protect_config=protect_config,
        name=name,
        descr=descr,
        flex_flash_raid_reporting_state=flex_flash_raid_reporting_state,
        flex_flash_state=flex_flash_state,
        mode=mode)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def local_disk_policy_modify(handle, name, mode=None, flex_flash_state=None,
                             flex_flash_raid_reporting_state=None,
                             protect_config=None, descr=None,
                             parent_dn="org-root"):
    """
    This method modify local disk policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the local disc policy.
        mode (string): Mode of local disk functioning.
        flex_flash_state (string): "enable" or "disable"
        flex_flash_raid_reporting_state (string): "enable" or "disable"
        protect_config (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn(string): Parent of Org.

    Returns:
        StorageLocalDiskConfigPolicy: Managed Object

    Raises:
        ValueError: If StorageLocalDiskConfigPolicy is not present

    Example:
        local_disk_policy_modify(handle, name="sample_l_disk",
                                parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/local-disk-config-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("local disk policy '%s' does not exist" % dn)

    if descr is not None:
        mo.descr = descr
    if mode is not None:
        mo.mode = mode
    if flex_flash_state is not None:
        mo.flex_flash_state = flex_flash_state
    if flex_flash_raid_reporting_state is not None:
        mo.flex_flash_raid_reporting_state = flex_flash_raid_reporting_state
    if protect_config is not None:
        mo.protect_config = protect_config

    handle.set_mo(mo)
    handle.commit()
    return mo


def local_disk_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes local disk policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the local disk policy.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If StorageLocalDiskConfigPolicy is not present

    Example:
        local_disk_policy_remove(handle, name="sample_l_disk")
    """

    dn = parent_dn + "/local-disk-config-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("local disk policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def local_disk_policy_exist(handle, name, mode="any-configuration",
                            flex_flash_state="enable",
                            flex_flash_raid_reporting_state="enable",
                            protect_config="yes", descr="",
                            parent_dn="org-root"):
    """
    This method checks if local disk policy exist.

    Args:
        handle (UcsHandle)
        name (string): Name of the local disk policy.
        mode (string): Mode of local disk functioning.
        flex_flash_state (string): "enable" or "disable"
        flex_flash_raid_reporting_state (string): "enable" or "disable"
        protect_config (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        Boolean: True or False

    Example:
        local_disk_policy_exist(handle, name="sample_l_disk",
                                parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/local-disk-config-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((mode and mo.mode != mode)
            and
            (flex_flash_state and mo.flex_flash_state != flex_flash_state)
            and
            (flex_flash_raid_reporting_state and
                mo.flex_flash_raid_reporting_state !=
                     flex_flash_raid_reporting_state)
            and
            (protect_config and mo.protect_config != protect_config)
            and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
