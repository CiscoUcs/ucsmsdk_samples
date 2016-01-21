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


def domain_create(handle, name, refresh_period="600", session_timeout="7200",
                  descr=""):

    from ucsmsdk.mometa.aaa.AaaDomain import AaaDomain

    mo = AaaDomain(parent_mo_or_dn="sys/auth-realm",
                   name=name,
                   refresh_period=refresh_period,
                   session_timeout=session_timeout,
                   descr=descr)

    handle.add_mo(mo, True)
    handle.commit()


def domain_assign_realm(handle, domain_name, realm, provider_group="",
                        name="", descr="", use2_factor="no"):

    from ucsmsdk.mometa.aaa.AaaDomainAuth import AaaDomainAuth

    dn = "sys/auth-realm/domain-" + domain_name
    obj = handle.query_dn(dn)
    if obj is None:
        raise ValueError("Domain does not exist")

    mo = AaaDomainAuth(parent_mo_or_dn=obj,
                       realm=realm,
                       provider_group=provider_group,
                       name=name,
                       descr=descr,
                       use2_factor=use2_factor)

    handle.add_mo(mo, True)
    handle.commit()


def domain_modify(handle, name, refresh_period=None, session_timeout=None,
                  descr=None):

    dn = "sys/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Domain does not exist.")

    if refresh_period is not None:
        mo.refresh_period = refresh_period
    if session_timeout is not None:
        mo.session_timeout = session_timeout
    if descr is not None:
        mo.desc = descr

    handle.set_mo(mo)
    handle.commit()


def domain_delete(handle, name):

    dn = "sys/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Domain does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def native_authentication_configure(handle, def_role_policy=None,
                                    def_login=None, con_login=None,
                                    policy_owner=None, descr=None):

    mo = handle.query_dn("sys/auth-realm")
    if mo is None:
        raise ValueError("Native Authentication does not exist.")

    if def_role_policy is not None:
        mo.def_role_policy = def_role_policy
    if def_login is not None:
        mo.def_login = def_login
    if con_login is not None:
        mo.con_login = con_login
    if policy_owner is not None:
        mo.policy_owner = policy_owner
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()


def native_authentication_default(handle, realm=None, session_timeout=None,
                                  refresh_period=None, provider_group=None,
                                  use2_factor=None, name=None, descr=None):

    mo = handle.query_dn("sys/auth-realm/default-auth")
    if mo is None:
        raise ValueError("Native Default Authentication does not exist")

    if realm is not None:
        mo.realm = realm
    if session_timeout is not None:
        mo.session_timeout = session_timeout
    if refresh_period is not None:
        mo.refresh_period = refresh_period
    if provider_group is not None:
        mo.provider_group = provider_group
    if use2_factor is not None:
        mo.use2_factor = use2_factor
    if name is not None:
        mo.name = name
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()

def native_authentication_console(handle, realm=None, provider_group=None,
                                  use2_factor=None, name=None, descr=None):

    mo = handle.query_dn("sys/auth-realm/console-auth")
    if mo is None:
        raise ValueError("Native Console Authentication does not exist")

    if realm is not None:
        mo.realm = realm
    if provider_group is not None:
        mo.provider_group = provider_group
    if use2_factor is not None:
        mo.use2_factor = use2_factor
    if name is not None:
        mo.name = name
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
