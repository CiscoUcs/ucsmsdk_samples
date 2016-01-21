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


def maintenance_policy_create(handle, name,
                              uptime_disr="user-ack",
                              descr="", parent_dn="org-root"):

    """
    This method creates Maintenance policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the maintenance policy.
        uptime_disr (string): "immediate" or "timer-automatic" or "user-ack"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Example:
        maintenance_policy_create(handle,
                                name="sample_maint", uptime_disr="user-ack")

    """

    obj = handle.query_dn(parent_dn)
    if obj:
        from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

        mo = LsmaintMaintPolicy(parent_mo_or_dn=parent_dn,
                                uptime_disr=uptime_disr,
                                name=name, descr=descr)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" %org_name)


def maintenance_policy_modify(handle, org_name, name,
                              uptime_disr=None,
                              descr=None, org_parent="org-root"):

    """
    This method creates Maintenance policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the maintenance policy.
        uptime_disr (string): "immediate" or "timer-automatic" or "user-ack"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        maintenance_policy_modify(handle, org_name="sample-org",
                                name="sample_maint", uptime_disr="user-ack")

    """
    org_dn = org_parent + "/org-" + org_name
    policy_dn= org_dn + "/maint-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        if uptime_disr is not None:
            mo.uptime_disr = uptime_disr
        if descr is not None:
            mo.descr = descr

        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Maintenance policy <%s> not found." % name)


def maintenance_policy_remove(handle, org_name, name, org_parent="org-root"):
    """
    This method removes maintenance policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the maintenance policy.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        maintenance_policy_remove(handle, org_name="sample-org",
                                name="sample_maint")
    """

    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "/maint-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Maintenance policy <%s> not found.Nothing to remove"
                     %name)
        else:
            handle.remove_mo(mo)
            handle.commit()
