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


def local_disk_policy_create(handle, name, descr="",
                             mode="any-configuration",
                             flex_flash_state="enable",
                             flex_flash_raid_reporting_state="enable",
                             protect_config="yes",
                             parent_dn="org-root"):
    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        mode (string): Mode of local disk functioning.
        flex_flash_state (string): "enable" or "disable"
        flex_flash_raid_reporting_state (string): "enable" or "disable"
        protect_config (string): "yes" or "no"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Example:
        local_disk_policy_create(handle, org_name="sample-org",
                                name="sample_l_disk")
    """

    from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import \
        StorageLocalDiskConfigPolicy

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn=parent_dn,
                                          protect_config=protect_config,
                                          name=name,
                                          descr=descr,
                                          flex_flash_raid_reporting_state=
                                          flex_flash_raid_reporting_state,
                                          flex_flash_state=flex_flash_state,
                                          mode=mode)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" % org_name)


def local_disk_policy_modify(handle, org_name, name, descr=None,
                             mode=None,
                             flex_flash_state=None,
                             flex_flash_raid_reporting_state=None,
                             protect_config=None,
                             parent_org="org-root"):
    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the boot policy.
        mode (string): Mode of local disk functioning.
        flex_flash_state (string): "enable" or "disable"
        flex_flash_raid_reporting_state (string): "enable" or "disable"
        protect_config (string): "yes" or "no"
        descr (string): Basic description.
        parent_org (string): Parent of Org.

    Returns:
        None

    Example:
        local_disk_policy_create(handle, org_name="sample-org",
                                name="sample_l_disk")
    """

    org_dn = parent_org + "/org-" + org_name
    policy_dn= org_dn + "/local-disk-config-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
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
    else:
        log.info("Local Disk Policy <%s> not found." % name)


def local_disk_policy_remove(handle, org_name, name, parent_org="org-root"):
    """
    This method removes local disk policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the local disk policy.
        parent_org (string): Parent of Org.

    Returns:
        None

    Example:
        local_disk_policy_remove(handle, org_name="sample_org",
                                name="sample_l_disk")
    """

    org_dn = parent_org + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "/local-disk-config-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Local Disk Policy <%s> not found.Nothing to remove" % name)
        else:
            handle.remove_mo(mo)
            handle.commit()
