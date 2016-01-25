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

import logging
log = logging.getLogger('ucs')


def ldap_provider_create(handle, name, order="lowest-available", rootdn="",
                         basedn="", port="389", enable_ssl="no", filter="",
                         attribute="", key="", timeout="30", vendor="OpenLdap",
                         retries="1",  descr=""):

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
    handle.add_mo(mo)
    handle.commit()


def ldap_provider_modify(handle, name, order=None, rootdn=None, basedn=None,
                         port=None, enable_ssl=None, filter=None,
                         attribute=None, key=None, timeout=None,
                         vendor=None, retries=None, descr=None):

    dn = "sys/ldap-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
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


def ldap_provider_delete(handle, name):

    dn = "sys/ldap-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Ldap Provider does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_configure_group_rules(handle, ldap_provider_name=None,
                                        authorization=None, traversal=None,
                                        use_primary_group=None,
                                        target_attr=None, name=None,
                                        descr=None):

    from ucsmsdk.mometa.aaa.AaaLdapGroupRule import AaaLdapGroupRule

    dn = "sys/ldap-ext/provider-" + ldap_provider_name
    obj = handle.query_dn(dn)
    if obj is None:
        raise ValueError("Ldap Provider does not exist.")

    mo = AaaLdapGroupRule(parent_mo_or_dn=obj)
    if ldap_provider_name is not None:
        mo.ldap_provider_name = ldap_provider_name
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


def ldap_group_map_create(handle, name, descr=""):

    from ucsmsdk.mometa.aaa.AaaLdapGroup import AaaLdapGroup

    mo = AaaLdapGroup(parent_mo_or_dn="sys/ldap-ext", name=name, descr=descr)
    handle.add_mo(mo)
    handle.commit()


def ldap_group_map_add_role(handle, ldap_group_map_name, name, descr=""):

    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn="sys/ldap-ext/ldapgroup-" + ldap_group_map_name
    obj = handle.query_dn(dn)
    if obj is None:
        raise ValueError("Ldap Group map does not exist")

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()


def ldap_group_map_remove_role(handle, ldap_group_map_name, name):

    ldap_dn = "sys/ldap-ext/ldapgroup-" + ldap_group_map_name
    dn = ldap_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Ldap Group Role does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_group_map_delete(handle, name):

    dn = "sys/ldap-ext/ldapgroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Ldap Group does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_create(handle, name, descr=""):

    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn="sys/ldap-ext",
                          name=name,
                          descr=descr)
    handle.add_mo(mo)
    handle.commit()


def ldap_provider_group_add_provider(handle, group_name, name, order,
                                     descr=""):

    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if group_mo is None:
        raise ValueError("Ldap Provider Group does not exist.")

    provider_dn = "sys/ldap-ext/provider-" + name
    provider_mo = handle.query_dn(provider_dn)
    if provider_mo is None:
        raise ValueError("Ldap Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)
    handle.add_mo(mo)


def ldap_provider_group_modify_provider(handle, group_name, name,
                                        order=None, descr=None):

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    provider_mo = handle.query_dn(provider_dn)
    if provider_mo is None:
        raise ValueError("Provider not available under group.")

    if order is not None:
        provider_mo.order = order
    if descr is not None:
        provider_mo.descr = descr

    handle.set_mo(provider_mo)
    handle.commit()


def ldap_provider_group_remove_provider(handle, group_name, name):

    group_dn = "sys/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    provider_mo = handle.query_dn(provider_dn)
    if provider_mo is None:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(provider_mo)
    handle.commit()

def ldap_provider_group_delete(handle, name):

    dn = "sys/ldap-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()
