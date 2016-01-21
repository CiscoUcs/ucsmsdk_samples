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


def tacacsplus_provider_create(handle, name, order="lowest-available", key="",
                               port="49", timeout="5", retries="1", enc_key="",
                               descr=""):

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
    handle.add_mo(mo)
    handle.commit()


def tacacsplus_provider_modify(handle, name, order=None, key=None, port=None,
                               timeout=None, retries=None, enc_key=None,
                               descr=None):

    dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        raise ValueError("TacacsPlus Provider does not exist")

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


def tacacsplus_provider_delete(handle, name):

    dn = "sys/tacacs-ext/provider-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        raise ValueError("TacacsPlus Provider does not exist")

    handle.set_mo(mo)
    handle.commit()


def tacacsplus_provider_group_create(handle, name, descr=""):

    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn="sys/tacacs-ext",
                          name=name, descr=descr)
    handle.add_mo(mo)
    handle.commit()


def tacacsplus_provider_group_add_provider(handle, group_name, name, order,
                                           descr=""):

    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if group_mo is None:
        raise ValueError("TacacsPlus Provider Group does not exist.")

    provider_dn = "sys/tacacs-ext/provider-" + name
    provider_mo = handle.query_dn(provider_dn)
    if provider_mo is None:
        raise ValueError("TacacsPlus Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)
    handle.add_mo(mo)


def tacacsplus_provider_group_modify_provider(handle, group_name, name,
                                              order=None, descr=None):

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
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


def tacacsplus_provider_group_remove_provider(handle, group_name, name):

    group_dn = "sys/tacacs-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    provider_mo = handle.query_dn(provider_dn)
    if provider_mo is None:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(provider_mo)
    handle.commit()

def tacacsplus_provider_group_delete(handle, name):

    dn = "sys/tacacs-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()
