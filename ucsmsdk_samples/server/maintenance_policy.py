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
        LsmaintMaintPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        maintenance_policy_create(handle, name="sample_maint",
                                    uptime_disr="user-ack",
                                    parent_dn="org-root/org-sub")

    """

    from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = LsmaintMaintPolicy(parent_mo_or_dn=obj, name=name,
                            uptime_disr=uptime_disr, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def maintenance_policy_modify(handle, name, uptime_disr=None, descr=None,
                              parent_dn="org-root"):

    """
    This method modify Maintenance policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the maintenance policy.
        uptime_disr (string): "immediate" or "timer-automatic" or "user-ack"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        LsmaintMaintPolicy: Managed Object

    Raises:
        ValueError: If LsmaintMaintPolicy is not present

    Example:
        maintenance_policy_modify(handle, name="sample_maint",
                                  uptime_disr="user-ack",
                                  parent_dn="org-root/org-sub")

    """

    dn = parent_dn + "/maint-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("maintenance policy '%s' does not exist" % dn)

    if uptime_disr is not None:
        mo.uptime_disr = uptime_disr
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def maintenance_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes maintenance policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the maintenance policy.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If LsmaintMaintPolicy is not present

    Example:
        maintenance_policy_remove(handle, org_name="sample-org",
                                name="sample_maint")
    """

    dn = parent_dn + "/maint-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("maintenance policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def maintenance_policy_exist(handle, name, uptime_disr="user-ack", descr="",
                             parent_dn="org-root"):
    """
    This method checks if maintenance policy does not exist.

    Args:
        handle (UcsHandle)
        name (string): Name of the maintenance policy.
        uptime_disr (string): "immediate" or "timer-automatic" or "user-ack"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        Boolean: True or False

    Example:
        maintenance_policy_exist(handle, name="sample_maint",
                                    uptime_disr="user-ack",
                                    parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/maint-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((uptime_disr and mo.uptime_disr != uptime_disr)
            and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
