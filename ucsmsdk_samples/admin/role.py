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

"""
This module performs the operation related to role.
"""


def role_create(handle, name, priv, descr="", policy_owner="local"):
    """
    creates a role

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        policy_owner (string): policy owner

    Returns:
        AaaRole: Managed Object

    Example:
        role_create(handle, name="testrole", priv="read-only")

    """

    from ucsmsdk.mometa.aaa.AaaRole import AaaRole

    mo = AaaRole(parent_mo_or_dn="sys/user-ext",
                 name=name,
                 priv=priv,
                 descr=descr,
                 policy_owner=policy_owner)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def role_exists(handle, name, priv, descr="", policy_owner="local"):
    """
    checks if a role exists

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        policy_owner (string): policy owner

    Returns:
        True/False

    Example:
        role_exists(handle, name="testrole", priv="read-only")
    """

    dn = "sys/user-ext/role-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((priv and mo.priv != priv) and
            (descr and mo.descr != descr) and
            (policy_owner and mo.policy_owner != policy_owner)):
            return False
        return True
    return False


def role_modify(handle, name, priv=None, descr=None, policy_owner=None):
    """
    modifies role

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        policy_owner (string): policy owner

    Returns:
        AaaRole: Managed Object

    Raises:
        ValueError: If AaaRole is not present

    Example:
        role_modify(handle, name="testrole", priv="read-only")
    """

    dn = "sys/user-ext/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Role does not exist")

    if priv is not None:
        mo.priv = priv
    if descr is not None:
        mo.descr = descr
    if policy_owner is not None:
        mo.policy_owner = policy_owner

    handle.set_mo(mo)
    handle.commit()
    return mo


def role_delete(handle, name):
    """
    deletes role

    Args:
        handle (UcsHandle)
        name (string): role name

    Returns:
        None

    Raises:
        ValueError: If AaaRole is not present

    Example:
        role_delete(handle, name="testrole")
    """

    dn = "sys/user-ext/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Role does not exist")

    handle.remove_mo(mo)
    handle.commit()
