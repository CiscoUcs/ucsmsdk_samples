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
This module performs the operation related to dns server management.
"""


def locale_create(handle, name, descr="", policy_owner="local"):
    """
    creates a locale

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        descr (string): descr
        policy_owner (string): policy_owner

    Returns:
        AaaLocale : Managed Object

    Example:
        locale_create(handle, name="test_locale")
    """

    from ucsmsdk.mometa.aaa.AaaLocale import AaaLocale

    mo = AaaLocale(parent_mo_or_dn="sys/user-ext",
                   name=name,
                   descr=descr,
                   policy_owner=policy_owner)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_exists(handle, name, descr="", policy_owner="local"):
    """
    checks if locale exists

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        descr (string): descr
        policy_owner (string): policy_owner

    Returns:
        True/False

    Example:
        locale_create(handle, name="test_locale")
    """

    dn = "sys/user-ext/locale-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((descr and mo.descr != descr) and
            (policy_owner and mo.policy_owner != policy_owner)):
            return False
        return True
    return False


def locale_modify(handle, name, descr="", policy_owner="local"):
    """
    modifies a locale

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        descr (string): descr
        policy_owner (string): policy_owner

    Returns:
        AaaLocale : Managed Object

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_modify(handle, name="test_locale")
    """

    dn = "sys/user-ext/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Locale does not exist")

    if descr is not None:
        mo.descr = descr
    if policy_owner is not None:
        mo.policy_owner = policy_owner

    handle.set_mo(mo)
    handle.commit()
    return mo


def locale_delete(handle, name):
    """
    deletes locale

    Args:
        handle (UcsHandle)
        name (string): locale name

    Returns:
        None

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_delete(handle, name="test_locale")
    """

    dn = "sys/user-ext/locale-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Locale does not exist")

    handle.remove_mo(mo)
    handle.commit()


def locale_assign_org(handle, locale_name, name, org_dn="org-root", descr=""):
    """
    assigns a locale

    Args:
        handle (UcsHandle)
        locale_name(string): org name
        name (string): name of ldap provider
        org_dn (string): org_dn
        descr (string): descr

    Returns:
        AaaOrg : Managed Object

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_assign_org(handle, name="test_locale")
    """

    from ucsmsdk.mometa.aaa.AaaOrg import AaaOrg

    dn = "sys/user-ext/locale-" + locale_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Locale does not exist")

    mo = AaaOrg(parent_mo_or_dn=obj, name=name, org_dn=org_dn, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_deassign_org(handle, locale_name, name):
    """
    deassigns a locale

    Args:
        handle (UcsHandle)
        locale_name(string): org name
        name (string): name of ldap provider
        org_dn (string): org_dn
        descr (string): descr

    Returns:
        None

    Raises:
        ValueError: If AaaOrg is not present

    Example:
        locale_deassign_org(handle, locale_name="test_locale,
                            name="org_name")
    """

    locale_dn = "sys/user-ext/locale-" + locale_name
    dn = locale_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("No Org assigned to Locale")

    handle.remove_mo(mo)
    handle.commit()
