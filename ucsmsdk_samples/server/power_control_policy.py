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


def power_control_policy_create(handle, name, prio="no-cap", descr="",
                                parent_dn="org-root"):
    """
    This method creates power control policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the power control policy.
        prio (string): ."no-cap" or "utility"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        PowerPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        power_control_policy_create(handle, name="sample_power",
                                   prio="no-cap", parent_dn="org-root/org-sub")
    """

    from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = PowerPolicy(parent_mo_or_dn=obj, name=name, prio=prio,
                     descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def power_control_policy_modify(handle,  name, prio=None, descr=None,
                                parent_dn="org-root"):
    """
    This method modify power control policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the power control policy.
        prio (string): ."no-cap" or "utility"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        PowerPolicy: Managed Object

    Raises:
        ValueError: If PowerPolicy is not present

    Example:
        power_control_policy_modify(handle, name="sample_power",
                                    prio="no-cap",
                                    parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/power-policy-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("power control policy '%s' does not exist" % dn)

    if prio is not None:
        mo.prio = prio
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def power_control_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes power control policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the power control policy.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If PowerPolicy is not present

    Example:
        power_control_policy_remove(handle, name="sample_power",
                                    parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/power-policy-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("power control policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def power_control_policy_exist(handle, name, prio="no-cap", descr="",
                               parent_dn="org-root"):
    """
    This method checks if power control policy exist.

    Args:
        handle (UcsHandle)
        name (string): Name of the power control policy.
        prio (string): ."no-cap" or "utility"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        Boolean: True or False

    Example:
        power_control_policy_exist(handle, name="sample_power", prio="no-cap",
                                    parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/power-policy-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((prio and mo.prio != prio) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
