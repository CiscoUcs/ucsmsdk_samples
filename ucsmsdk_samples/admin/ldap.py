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
This module performs the operation related to ldap.
"""


def ldap_provider_create(handle, name, order="lowest-available", rootdn="",
                         basedn="", port="389", enable_ssl="no", filter="",
                         attribute="", key="", timeout="30", vendor="OpenLdap",
                         retries="1",  descr=""):
    """
    creates a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        order (string): "lowest-available" or 0-16
        rootdn (string): rootdn
        basedn (string): basedn
        port (string): port
        enable_ssl (string): enable_ssl
        filter (string): filter
        attribute (string): attribute
        key (string): key
        timeout (string): timeout
        vendor (string): vendor
        retries (string): retries
        descr (string): descr

    Returns:
        AaaLdapProvider : Managed Object

    Example:
        ldap_provider_create(handle, name="test_ldap_provider")
    """

    from ucsmsdk.mometa.aaa.AaaLdapProvider import AaaLdapProvider

    mo = AaaLdapProvider(parent_mo_or_dn="sys/ldap-ext",
                         name=name,
                         order=order,
                         rootdn=rootdn,
                         basedn=basedn,
                         port=port,
                         enable_ssl=enable_ssl,
                         filter=filter,
                         attribute=attribute,
                         key=key,
                         timeout=timeout,
                         vendor=vendor,
                         retries=retries,
                         descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_exists(handle, name, order="lowest-available", rootdn="",
                         basedn="", port="389", enable_ssl="no", filter="",
                         attribute="", key="", timeout="30", vendor="OpenLdap",
                         retries="1",  descr=""):
    """
    checks if ldap provider exists

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        order (string): "lowest-available" or 0-16
        rootdn (string): rootdn
        basedn (string): basedn
        port (string): port
        enable_ssl (string): enable_ssl
        filter (string): filter
        attribute (string): attribute
        key (string): key
        timeout (string): timeout
        vendor (string): vendor
        retries (string): retries
        descr (string): descr

    Returns:
        True/False

    Example:
        ldap_provider_exists(handle, name="test_ldap_provider")
    """

    dn = "sys/ldap-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((order and mo.order != order) and
            (rootdn and mo.rootdn != rootdn) and
            (basedn and mo.basedn != basedn) and
            (port and mo.port != port) and
            (enable_ssl and mo.enable_ssl != enable_ssl) and
            (filter and mo.filter != filter) and
            (attribute and mo.attribute != attribute) and
            (key and mo.key != key) and
            (timeout and mo.timeout != timeout) and
            (vendor and mo.vendor != vendor) and
            (retries and mo.retries != retries) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False


def ldap_provider_modify(handle, name, order=None, rootdn=None, basedn=None,
                         port=None, enable_ssl=None, filter=None,
                         attribute=None, key=None, timeout=None,
                         vendor=None, retries=None, descr=None):
    """
    modifies a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        order (string): "lowest-available" or 0-16
        rootdn (string): rootdn
        basedn (string): basedn
        port (string): port
        enable_ssl (string): enable_ssl
        filter (string): filter
        attribute (string): attribute
        key (string): key
        timeout (string): timeout
        vendor (string): vendor
        retries (string): retries
        descr (string): descr

    Returns:
        AaaLdapProvider : Managed Object

    Raises:
        ValueError: If AaaLdapProvider is not present

    Example:
        ldap_provider_modify(handle, name="test_ldap_provider")
    """

    dn = "sys/ldap-ext/provider-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Ldap Provider does not exist")

    if order is not None:
        mo.order = order
    if rootdn is not None:
        mo.rootdn = rootdn
    if basedn is not None:
        mo.basedn = basedn
    if port is not None:
        mo.port = port
    if enable_ssl is not None:
        mo.enable_ssl = enable_ssl
    if filter is not None:
        mo.filter = filter
    if attribute is not None:
        mo.attribute = attribute
    if key is not None:
        mo.key = key
    if timeout is not None:
        mo.timeout = timeout
    if vendor is not None:
        mo.vendor = vendor
    if retries is not None:
        mo.retries = retries
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_delete(handle, name):
    """
    deletes a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider

    Returns:
        None

    Raises:
        ValueError: If AaaLdapProvider is not present

    Example:
        ldap_provider_delete(handle, name="test_ldap_provider")
    """
    dn = "sys/ldap-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Ldap Provider does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_configure_group_rules(handle, ldap_provider_name,
                                        authorization=None, traversal=None,
                                        use_primary_group=None,
                                        target_attr=None, name=None,
                                        descr=None):
    """
    configures group rules of a ldap provider

    Args:
        handle (UcsHandle)
        ldap_provider_name (string): name of ldap provider
        authorization (string): authorization
        traversal (string): traversal
        use_primary_group (string): use_primary_group
        target_attr (string): target_attr
        name (string): name
        descr (string): descr

    Returns:
        AaaLdapGroupRule : Managed Object

    Example:
        ldap_provider_configure_group_rules(handle, name="test_ldap_provider")
    """

    from ucsmsdk.mometa.aaa.AaaLdapGroupRule import AaaLdapGroupRule

    dn = "sys/ldap-ext/provider-" + ldap_provider_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Ldap Provider does not exist.")

    mo = AaaLdapGroupRule(parent_mo_or_dn=obj)
    if authorization is not None:
        mo.authorization = authorization
    if traversal is not None:
        mo.traversal = traversal
    if use_primary_group is not None:
        mo.use_primary_group = use_primary_group
    if target_attr is not None:
        mo.target_attr = target_attr
    if name is not None:
        mo.name = name
    if descr is not None:
        mo.descr = descr

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_create(handle, name, descr=""):
    """
    creates ldap group map

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): descr

    Returns:
        AaaLdapGroup : Managed Object

    Example:
        ldap_group_map_create(handle, name="test_ldap_group_map")
    """

    from ucsmsdk.mometa.aaa.AaaLdapGroup import AaaLdapGroup

    mo = AaaLdapGroup(parent_mo_or_dn="sys/ldap-ext", name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_exists(handle, name, descr=""):
    """
    checks if ldap group map exists

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): descr

    Returns:
        True/False

    Example:
        ldap_group_map_exists(handle, name="test_ldap_group_map")
    """

    dn = "sys/ldap-ext/ldapgroup-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def ldap_group_map_delete(handle, name):
    """
    removes ldap group map

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaLdapGroup is not present

    Example:
        ldap_group_map_delete(handle, name="test_ldap_group_map")
    """

    dn = "sys/ldap-ext/ldapgroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Ldap Group does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_group_map_add_role(handle, ldap_group_map_name, name, descr=""):
    """
    add role to ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name
        descr (string): descr

    Returns:
        AaaUserRole : Managed Object

    Example:
        ldap_group_map_add_role(handle,
                                ldap_group_map_name="test_ldap_group_map",
                                name="test_role")
    """

    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn = "sys/ldap-ext/ldapgroup-" + ldap_group_map_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Ldap Group map '%s' does not exist" % dn)

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_role_exists(handle, ldap_group_map_name, name, descr=""):
    """
    checks if role exists for the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name
        descr (string): descr

    Returns:
        True/False

    Example:
        ldap_group_map_role_exists(handle,
                                ldap_group_map_name="test_ldap_group_map",
                                name="test_role")
    """

    ldap_dn = "sys/ldap-ext/ldapgroup-" + ldap_group_map_name
    dn = ldap_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def ldap_group_map_remove_role(handle, ldap_group_map_name, name):
    """
    removes role from the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name

    Returns:
        None

    Raises:
        ValueError: If AaaUserRole is not present

    Example:
        ldap_group_map_remove_role(handle,
                                ldap_group_map_name="test_ldap_group_map",
                                name="test_role")
    """

    ldap_dn = "sys/ldap-ext/ldapgroup-" + ldap_group_map_name
    dn = ldap_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Ldap Group Role does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_create(handle, name, descr=""):
    """
    creates ldap provider group

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): descr

    Returns:
        AaaProviderGroup : Managed Object

    Example:
        ldap_provider_group_create(handle, name="test_ldap_group_map")
    """

    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn="sys/ldap-ext",
                          name=name,
                          descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_group_exists(handle, name, descr=""):
    """
    checks if ldap provider group exists

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): descr

    Returns:
        True/False

    Example:
        ldap_provider_group_exists(handle, name="test_ldap_group_map")
    """

    dn = "sys/ldap-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def ldap_provider_group_delete(handle, name):
    """
    deletes ldap provider group

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): descr

    Returns:
        True/False

    Raises:
        ValueError: If AaaProviderGroup is not present

    Example:
        ldap_provider_group_delete(handle, name="test_ldap_group_map")
    """

    dn = "sys/ldap-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_add_provider(handle, group_name, name, order,
                                     descr=""):
    """
    adds provider to ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): name
        order (string): order
        descr (string): descr

    Returns:
        AaaProviderRef : Managed Object

    Raises:
        ValueError: If AaaProviderGroup or AaaProvider is not present

    Example:
        ldap_provider_group_add_provider(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_provider",
                                        order="1")
    """

    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("Ldap Provider Group does not exist.")

    provider_dn = "sys/ldap-ext/provider-" + name
    provider_mo = handle.query_dn(provider_dn)
    if not provider_mo:
        raise ValueError("Ldap Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_group_provider_exists(handle, group_name, name, order,
                                        descr=""):
    """
    checks if provider added ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): name
        order (string): order
        descr (string): descr

    Returns:
        True/False

    Example:
        ldap_provider_group_provider_exists(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_provider",
                                        order="1")
    """

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if mo:
        if ((descr and mo.descr != descr) and
            (order and mo.order != order)):
            return False
        return True
    return False


def ldap_provider_group_modify_provider(handle, group_name, name,
                                        order=None, descr=None):
    """
    modify provider of ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): name
        order (string): order
        descr (string): descr

    Returns:
        True/False

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        ldap_provider_group_modify_provider(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_provider",
                                        order="1")
    """

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Provider not available under group.")

    if order is not None:
        mo.order = order
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_group_remove_provider(handle, group_name, name):
    """
    removes provider from ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        ldap_provider_group_modify_provider(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_provider",
                                        order="1")
    """

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    provider_mo = handle.query_dn(provider_dn)
    if not provider_mo:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(provider_mo)
    handle.commit()
