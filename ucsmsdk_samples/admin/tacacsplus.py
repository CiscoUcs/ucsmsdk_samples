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


def tacacsplus_provider_create(handle, name, order="lowest-available", key="",
                               port="49", timeout="5", retries="1", enc_key="",
                               descr=""):
    """
    Creates a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider
        order (string): order
        key (string): key
        port (string): port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): descr

    Returns:
        AaaTacacsPlusProvider: Managed Object

    Example:
        tacacsplus_provider_create(handle, name="tacacsplus_provider")
    """

    from ucsmsdk.mometa.aaa.AaaTacacsPlusProvider import AaaTacacsPlusProvider

    mo = AaaTacacsPlusProvider(parent_mo_or_dn="sys/tacacs-ext",
                               name=name,
                               order=order,
                               key=key,
                               port=port,
                               timeout=timeout,
                               retries=retries,
                               enc_key=enc_key,
                               descr=descr
                               )
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_exists(handle, name, order="lowest-available", key="",
                               port="49", timeout="5", retries="1", enc_key="",
                               descr=""):
    """
    checks if a tacacsplus provider exists

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider
        order (string): order
        key (string): key
        port (string): port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): descr

    Returns:
        True/False

    Example:
        tacacsplus_provider_exists(handle, name="tacacsplus_provider")
    """

    dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((order and mo.order != order) and
            (key and mo.key != key) and
            (port and mo.port != port) and
            (timeout and mo.timeout != timeout) and
            (retries and mo.retries != retries) and
            (enc_key and mo.enc_key != enc_key) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False


def tacacsplus_provider_modify(handle, name, order=None, key=None, port=None,
                               timeout=None, retries=None, enc_key=None,
                               descr=None):
    """
    modifies a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider
        order (string): order
        key (string): key
        port (string): port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): descr

    Returns:
        AaaTacacsPlusProvider: Managed Object

    Raises:
        ValueError: If AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_modify(handle, name="tacacsplus_provider")
    """

    dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("TacacsPlus Provider '%s' does not exist" % dn)

    if order is not None:
        mo.order = order
    if key is not None:
        mo.key = key
    if port is not None:
        mo.port = port
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


def tacacsplus_provider_delete(handle, name):
    """
    deletes a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider

    Returns:
        None

    Raises:
        ValueError: If AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_delete(handle, name="tacacsplus_provider")
    """

    dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        raise ValueError("TacacsPlus Provider does not exist")

    handle.set_mo(mo)
    handle.commit()


def tacacsplus_provider_group_create(handle, name, descr=""):
    """
    Creates a tacacsplus provider group

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider group
        descr (string): descr

    Returns:
        AaaTacacsPlusProvider: Managed Object

    Example:
        tacacsplus_provider_create(handle, name="tacacsplus_provider")
    """

    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn="sys/tacacs-ext",
                          name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_group_exists(handle, name, descr=""):
    """
    checks if a tacacsplus provider group exists

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider group
        descr (string): descr

    Returns:
        True/False

    Example:
        tacacsplus_provider_group_exists(handle, name="tacacsplus_provider")
    """

    dn = "sys/tacacs-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def tacacsplus_provider_group_delete(handle, name):
    """
    deletes a tacacsplus provider group

    Args:
        handle (UcsHandle)
        name (string): name of tacacsplus provider group

    Returns:
        None

    Raises:
        ValueError: If AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_delete(handle, name="tacacsplus_provider")
    """

    dn = "sys/tacacs-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def tacacsplus_provider_group_add_provider(handle, group_name, name, order,
                                           descr=""):
    """
    adds a tacacsplus provider to a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): name of tacacsplus provider group
        order (string): order
        name (string): name of tacacsplus provider
        descr (string): descr

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderGroup Or AaaProvider is not present

    Example:
        tacacsplus_provider_group_add_provider(handle,
                                    group_name="tacacsplus_provider_group",
                                    name="tacacsplus_provider")
    """

    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("TacacsPlus Provider Group does not exist.")

    provider_dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("TacacsPlus Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_group_provider_exists(handle, group_name, name, order,
                                              descr=""):
    """
    checks if a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): name of tacacsplus provider group
        order (string): order
        name (string): name of tacacsplus provider
        descr (string): descr

    Returns:
        True/False

    Raises:
        ValueError: If AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_add_provider(handle,
                                    group_name="tacacsplus_provider_group",
                                    name="tacacsplus_provider")
    """

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("TacacsPlus Provider Group does not exist.")

    provider_dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if mo:
        if ((descr and mo.descr != descr) and
            (order and mo.order != order)):
            return False
        return True
    return False


def tacacsplus_provider_group_modify_provider(handle, group_name, name,
                                              order=None, descr=None):
    """
    modifies a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): name of tacacsplus provider group
        order (string): order
        name (string): name of tacacsplus provider
        descr (string): descr

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_add_provider(handle,
                                    group_name="tacacsplus_provider_group",
                                    name="tacacsplus_provider")
    """

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
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


def tacacsplus_provider_group_remove_provider(handle, group_name, name):
    """
    removes a tacacsplus provider from a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): name of tacacsplus provider group
        name (string): name of tacacsplus provider

    Returns:
        None

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_remove_provider(handle,
                                    group_name="tacacsplus_provider_group",
                                    name="tacacsplus_provider")
    """

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if mo is None:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(mo)
    handle.commit()
