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


def sol_policy_create(handle, name, admin_state, speed="9600", descr="",
                      parent_dn="org-root"):
    """
    This method creates SoL policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the SoL policy.
        admin_state (string): "enable" or "disable"
        speed (string): Speed on SoL e.g. "9600"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        SolPolicy: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        sol_policy_create(handle, name="sample_SoL", admin_state="enable",
                         speed="9600", parent_dn="org-root/org-sub")

    """

    from ucsmsdk.mometa.sol.SolPolicy import SolPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = SolPolicy(parent_mo_or_dn=obj, name=name,
                   admin_state=admin_state, speed=speed, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def sol_policy_modify(handle, name, admin_state=None, speed=None, descr=None,
                      parent_dn="org-root"):
    """
    This method modify SoL policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the SoL policy.
        admin_state (string): "enable" or "disable"
        speed (string): Speed on SoL e.g. "9600"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        SolPolicy: Managed Object

    Raises:
        ValueError: If SolPolicy is not present

    Example:
        sol_policy_modify(handle, name="sample_SoL", admin_state="enable",
                         speed="9600", parent_dn="org-root")

    """

    dn = parent_dn + "sol/-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sol policy '%s' does not exist" % dn)

    if admin_state is not None:
        mo.admin_state = admin_state
    if speed is not None:
        mo.speed = speed
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def sol_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes SoL policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the SoL policy.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If SolPolicy is not present

    Example:
        sol_policy_remove(handle, name="sample_SoL",
                            parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "sol/-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sol policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def sol_policy_exist(handle, name, admin_state, speed="9600", descr="",
                     parent_dn="org-root"):
    """
    This method checks if sol policy exist.

    Args:
        handle (UcsHandle)
        name (string): Name of the SoL policy.
        admin_state (string): "enable" or "disable"
        speed (string): Speed on SoL e.g. "9600"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        Boolean: True or False

    Example:
        sol_policy_exist(handle, name="sample_SoL", admin_state="enable",
                         speed="9600", parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/scrub-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((admin_state and mo.admin_state != admin_state)
            and
            (speed and mo.speed != speed)
            and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
