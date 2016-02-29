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
This module performs the operation related to radius configuration.
"""


def radius_provider_create(handle, name, order="lowest-available", key="",
                           auth_port="1812", timeout="5", retries="1",
                           enc_key="", descr=""):
    """
    Creates a radius provider

    Args:
        handle (UcsHandle)
        name (string): name
        order (string): order
        key (string): key
        auth_port (string): auth_port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): description

    Returns:
        AaaRadiusProvider: Managed Object

    Example:
        radius_provider_create(handle, name="test_radius_provider")
    """

    from ucsmsdk.mometa.aaa.AaaRadiusProvider import AaaRadiusProvider

    mo = AaaRadiusProvider(parent_mo_or_dn="sys/radius-ext",
                           name=name,
                           order=order,
                           key=key,
                           auth_port=auth_port,
                           timeout=timeout,
                           retries=retries,
                           enc_key=enc_key,
                           descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_exists(handle, name, order="lowest-available", key="",
                           auth_port="1812", timeout="5", retries="1",
                           enc_key="", descr=""):
    """
    checks if radius provider exists

    Args:
        handle (UcsHandle)
        name (string): name
        order (string): order
        key (string): key
        auth_port (string): auth_port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): description

    Returns:
        True/False

    Example:
        radius_provider_exists(handle, name="test_radius_provider")
    """

    dn = "sys/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((order and mo.order != order) and
            (key and mo.key != key) and
            (auth_port and mo.auth_port != auth_port) and
            (timeout and mo.timeout != timeout) and
            (retries and mo.retries != retries) and
            (enc_key and mo.enc_key != enc_key) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False


def radius_provider_modify(handle, name, order=None, key=None,
                           auth_port=None, timeout=None, retries=None,
                           enc_key=None, descr=None):
    """
    modifies a radius provider

    Args:
        handle (UcsHandle)
        name (string): name
        order (string): order
        key (string): key
        auth_port (string): auth_port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): description

    Returns:
        AaaRadiusProvider: Managed Object

    Raises:
        ValueError: If AaaRadiusProvider is not present

    Example:
        radius_provider_modify(handle, name="test_radius_provider")
    """

    dn = "sys/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        raise ValueError("Radius Provider does not exist")

    if order is not None:
        mo.order = order
    if key is not None:
        mo.key = key
    if auth_port is not None:
        mo.auth_port = auth_port
    if timeout is not None:
        mo.timeout = timeout
    if retries is not None:
        mo.retries = retries
    if enc_key is not None:
        mo.enc_key = enc_key
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_delete(handle, name):
    """
    deletes a radius provider

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaRadiusProvider is not present

    Example:
        radius_provider_delete(handle, name="test_radius_provider")
    """

    dn = "sys/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        raise ValueError("Radius Provider does not exist")

    handle.set_mo(mo)
    handle.commit()


def radius_provider_group_create(handle, name, descr=""):
    """
    Creates a radius provider group

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): description

    Returns:
        AaaProviderGroup: Managed Object

    Example:
        radius_provider_group_create(handle, name="test_radius_provider_group")
    """

    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn="sys/radius-ext",
                          name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_exists(handle, name, descr=""):
    """
    checks if radius provider group exists

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): description

    Returns:
        True/False

    Example:
        radius_provider_group_exists(handle, name="test_radius_provider_group")
    """

    dn = "sys/radius-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def radius_provider_group_delete(handle, name):
    """
    deletes a radius provider group

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaProviderGroup is not present

    Example:
        radius_provider_group_delete(handle, name="test_radius_provider_group")
    """

    dn = "sys/radius-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_add_provider(handle, group_name, name, order,
                                       descr=""):
    """
    adds a provider to a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): group_name
        name (string): name
        order (string): order
        descr (string): description

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_add_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = "sys/radius-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if group_mo is None:
        raise ValueError("Radius Provider Group does not exist.")

    provider_dn = "sys/radius-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Radius Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_provider_exists(handle, group_name, name, order,
                                          descr=""):
    """
    checks if a provider exists under a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): group_name
        name (string): name
        order (string): order
        descr (string): description

    Returns:
        True/False

    Raises:
        ValueError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_provider_exists(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = "sys/radius-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("Radius Provider Group does not exist.")

    provider_dn = "sys/radius-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Radius Provider does not exist.")

    if mo:
        if ((order and mo.order != order) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False


def radius_provider_group_modify_provider(handle, group_name, name,
                                          order=None, descr=None):
    """
    modifies a provider to a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): group_name
        name (string): name
        order (string): order
        descr (string): description

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        radius_provider_group_modify_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = "sys/radius-ext/providergroup-" + group_name
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


def radius_provider_group_remove_provider(handle, group_name, name):
    """
    removes a provider from a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): group_name
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        radius_provider_group_remove_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = "sys/radius-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(mo)
    handle.commit()
