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


def domain_create(handle, name, refresh_period="600", session_timeout="7200",
                  descr=""):
    """
    Adds a domain

    Args:
        handle (UcsHandle)
        name (string): name of domain
        refresh_period: refresh period in seconds. Default 600.
        session_timeout: timeout in seconds. Default 7200.
        descr (string): description

    Returns:
        AaaDomain : Managed Object

    Example:
        domain_create(handle, name="ciscoucs")
    """

    from ucsmsdk.mometa.aaa.AaaDomain import AaaDomain

    mo = AaaDomain(parent_mo_or_dn="sys/auth-realm",
                   name=name,
                   refresh_period=refresh_period,
                   session_timeout=session_timeout,
                   descr=descr)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def domain_exists(handle, name, refresh_period="600", session_timeout="7200",
                  descr=""):
    """
    checks if domain exists

    Args:
        handle (UcsHandle)
        name (string): name of domain
        refresh_period: refresh period in seconds. Default 600.
        session_timeout: timeout in seconds. Default 7200.
        descr (string): description

    Returns:
        True/False

    Example:
        domain_exists(handle, name="ciscoucs")
    """

    dn = "sys/svc-ext/dns-svc/dns-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((descr and (mo.descr != descr))
            and
            (refresh_period and (mo.refresh_period != refresh_period))
            and
            (session_timeout and (mo.session_timeout != session_timeout))):
            return False
        return True
    return False


def domain_modify(handle, name, refresh_period=None, session_timeout=None,
                  descr=None):
    """
    Modifies a domain

    Args:
        handle (UcsHandle)
        name (string): name of domain
        refresh_period: refresh period in seconds. Default 600.
        session_timeout: timeout in seconds. Default 7200.
        descr (string): description

    Returns:
        AaaDomain : Managed Object

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        domain_modify(handle, name="ciscoucs", descr="modified")
    """

    dn = "sys/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Domain '%s' does not exist." % dn)

    if refresh_period is not None:
        mo.refresh_period = refresh_period
    if session_timeout is not None:
        mo.session_timeout = session_timeout
    if descr is not None:
        mo.desc = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def domain_delete(handle, name):
    """
    deletes a domain.

    Args:
        handle (UcsHandle)
        name (string): domain name

    Returns:
        None

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        domain_delete(handle, name="ciscoucs")
    """

    dn = "sys/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Domain '%s' does not exist." % dn)

    handle.remove_mo(mo)
    handle.commit()


def domain_realm_configure(handle, domain_name, realm, provider_group="",
                           name="", descr="", use2_factor="no"):
    """
    configure realm of a domain.

    Args:
        handle (UcsHandle)
        domain_name (string): domain name
        realm (string): realm ["ldap", "local", "none", "radius", "tacacs"]
        provider_group (string): provider group name
        name (string): name
        descr (string): description
        use2_factor (string): ["false", "no", "true", "yes"]

    Returns:
        AaaDomainAuth : Managed Object

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        domain_realm_configure(handle, domain_name="ciscoucs", realm="ldap")
    """

    from ucsmsdk.mometa.aaa.AaaDomainAuth import AaaDomainAuth

    dn = "sys/auth-realm/domain-" + domain_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Domain '%s' does not exist" % dn)

    mo = AaaDomainAuth(parent_mo_or_dn=obj)
    if realm is not None:
        mo.realm = realm
    if provider_group is not None:
        mo.provider_group = provider_group
    if name is not None:
        mo.name = name
    if descr is not None:
        mo.descr = descr
    if use2_factor is not None:
        mo.use2_factor = use2_factor

    handle.set_mo(mo)
    handle.commit()
    return mo


def native_authentication_configure(handle, def_role_policy=None,
                                    def_login=None, con_login=None,
                                    policy_owner=None, descr=None):
    """
    configure native authentication.

    Args:
        handle (UcsHandle)
        def_role_policy (string): def_role_policy
        def_login (string): def_login
        con_login (string): con_login
        policy_owner (string): policy_owner
        descr (string): description

    Returns:
        AaaAuthRealm : Managed Object

    Raises:
        ValueError: If AaaAuthRealm is not present

    Example:
        native_authentication_configure(handle, descr="modified")
    """

    mo = handle.query_dn("sys/auth-realm")
    if not mo:
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
    return mo


def native_authentication_default(handle, realm=None, session_timeout=None,
                                  refresh_period=None, provider_group=None,
                                  use2_factor=None, name=None, descr=None):
    """
    configure default native authentication.

    Args:
        handle (UcsHandle)
        realm (string): realm
        session_timeout (string): session_timeout
        refresh_period (string): refresh_period
        provider_group (string): provider_group
        use2_factor (string): use2_factor
        name (string): name
        descr (string): description

    Returns:
        AaaDefaultAuth : Managed Object

    Raises:
        ValueError: If AaaDefaultAuth is not present

    Example:
        native_authentication_default(handle, descr="modified")
    """

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
    return mo


def native_authentication_console(handle, realm=None, provider_group=None,
                                  use2_factor=None, name=None, descr=None):
    """
    configure console native authentication.

    Args:
        handle (UcsHandle)
        realm (string): realm
        provider_group (string): provider_group
        use2_factor (string): use2_factor
        name (string): name
        descr (string): description

    Returns:
        AaaConsoleAuth : Managed Object

    Raises:
        ValueError: If AaaConsoleAuth is not present

    Example:
        native_authentication_console(handle, descr="modified")
    """

    mo = handle.query_dn("sys/auth-realm/console-auth")
    if not mo:
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
    return mo
