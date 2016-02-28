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
This module performs the operation related to snmp server, user and traps.
"""


def snmp_enable(handle, community=None, sys_contact=None, sys_location=None,
                descr=None, is_set_snmp_secure=None):
    """
    Enables SNMP.

    Args:
        handle (UcsHandle)
        community (string): community
        sys_contact (string): sys_contact
        sys_location (string): sys_location
        descr (string): descr
        policy_owner (string): policy_owner
        is_set_snmp_secure (string): "yes" or "no"

    Returns:
        CommSnmp: Managed object

    Raises:
        ValueError: If CommSnmp Mo is not present

    Example:
        mo = snmp_enable(handle,
                    community="username",
                    sys_contact="user contact",
                    sys_location="user location",
                    descr="SNMP Service",
                    is_set_snmp_secure="no")

    """

    from ucsmsdk.mometa.comm.CommSnmp import CommSnmpConsts

    dn = "sys/svc-ext/snmp-svc"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp config '%s' does not exist" % dn)

    mo.admin_state = CommSnmpConsts.ADMIN_STATE_ENABLED

    if community is not None:
        mo.community = community
    if sys_contact is not None:
        mo.sys_contact = sys_contact
    if sys_location is not None:
        mo.sys_location = sys_location
    if descr is not None:
        mo.descr = descr
    if is_set_snmp_secure is not None:
        mo.is_set_snmp_secure = is_set_snmp_secure

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_disable(handle):
    """
    Disables SNMP.

    Args:
        handle (UcsHandle)

    Returns:
        CommSnmp: Managed Object

    Raises:
        ValueError: If CommSnmp Mo is not present

    Example:
        snmp_disable(handle)
    """

    from ucsmsdk.mometa.comm.CommSnmp import CommSnmpConsts

    dn = "sys/svc-ext/snmp-svc"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp config '%s' does not exist" % dn)

    mo.admin_state = CommSnmpConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_trap_add(handle, hostname, community, port, version="v3",
                  notification_type="traps", v3_privilege="noauth"):
    """
    Adds snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): ip address
        community (string): community
        port (number): port
        version (string): "v1", "v2c", "v3"
        notification_type (string): "informs", "traps"
            Required only for version "v2c" and "v3"
        v3_privilege (string): "auth", "noauth", "priv"
            Required only for version "v3"

    Returns:
        CommSnmpTrap: Managed Object

    Example:
        snmp_trap_add(handle, hostname="10.10.10.10",
                      community="username", port="162",
                      version="v2c",
                      notification_type="informs")

    """

    from ucsmsdk.mometa.comm.CommSnmpTrap import CommSnmpTrap
    mo = CommSnmpTrap(parent_mo_or_dn="sys/svc-ext/snmp-svc",
                      hostname=hostname,
                      community=community,
                      port=port,
                      version=version,
                      notification_type=notification_type,
                      v3_privilege=v3_privilege)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def snmp_trap_exists(handle, hostname, community, port, version="v3",
                     notification_type="traps", v3_privilege="noauth"):
    """
    checks if snmp trap exists

    Args:
        handle (UcsHandle)
        hostname (string): ip address
        community (string): community
        port (number): port
        version (string): "v1", "v2c", "v3"
        notification_type (string): "informs", "traps"
            Required only for version "v2c" and "v3"
        v3_privilege (string): "auth", "noauth", "priv"
            Required only for version "v3"

    Returns:
        True/False

    Example:
        snmp_trap_exists(handle, hostname="10.10.10.10",
                      community="username", port="162",
                      version="v2c",
                      notification_type="informs")

    """

    dn = "sys/svc-ext/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if mo:
        if ((community and mo.community != community) and
            (port and mo.port != port) and
            (version and mo.version != version) and
            (notification_type and
             mo.notification_type != notification_type) and
            (v3_privilege and mo.v3_privilege != v3_privilege)):
            return False
        return True
    return False


def snmp_trap_modify(handle, hostname, community=None, port=None,
                     version=None, notification_type=None, v3_privilege=None):
    """
    Modifies snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): ip address
        community (string): community
        port (number): port
        version (string): "v1", "v2c", "v3"
        notification_type (string): "informs", "traps"
            Required only for version "v2c" and "v3"
        v3_privilege (string): "auth", "noauth", "priv"
            Required only for version "v3"

    Returns:
        CommSnmpTrap: Managed Object

    Raises:
        ValueError: If CommSnmpTrap Mo is not present

    Example:
        snmp_trap_modify(handle, hostname="10.10.10.10",
                          community="username", port="162",
                          version="v3",
                          notification_type="traps",
                          v3_privilege="noauth")

    """

    dn = "sys/svc-ext/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp trap MO is not available")

    if community is not None:
        mo.community = community
    if port is not None:
        mo.port = port
    if version is not None:
        mo.version = version
    if notification_type is not None:
        mo.notification_type = notification_type
    if v3_privilege is not None:
        mo.v3_privilege = v3_privilege

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_trap_remove(handle, hostname):
    """
    Modifies snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): ip address

    Returns:
        None

    Raises:
        ValueError: If CommSnmpTrap Mo is not present

    Example:
        snmp_trap_remove(handle, hostname="10.10.10.10")

    """

    dn = "sys/svc-ext/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp trap MO is not available")

    handle.remove_mo(mo)
    handle.commit()


def snmp_user_add(handle, name, descr, pwd, privpwd, auth="md5",
                  use_aes="yes"):
    """
    Adds snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        descr (string): description
        pwd (string): password
        privpwd (string): privacy password
        auth (string): "md5", "sha"
        use_aes (string): "yes", "no"

    Returns:
        CommSnmpUser: Managed Object

    Example:
        snmp_user_add(handle, name="snmpuser", descr="", pwd="password",
                    privpwd="password", auth="sha")

    """

    from ucsmsdk.mometa.comm.CommSnmpUser import CommSnmpUser

    mo = CommSnmpUser(parent_mo_or_dn="sys/svc-ext/snmp-svc",
                      name=name,
                      descr=descr,
                      pwd=pwd,
                      privpwd=privpwd,
                      auth=auth,
                      use_aes=use_aes)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def snmp_user_exists(handle, name, descr, pwd, privpwd, auth="md5",
                     use_aes="yes"):
    """
    checks if snmp user exists.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        descr (string): description
        pwd (string): password
        privpwd (string): privacy password
        auth (string): "md5", "sha"
        use_aes (string): "yes", "no"

    Returns:
        True/False

    Example:
        snmp_user_exists(handle, name="snmpuser", descr="", pwd="password",
                    privpwd="password", auth="sha")

    """

    dn = "sys/svc-ext/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((descr and mo.descr != descr) and
            (pwd and mo.pwd != pwd) and
            (privpwd and mo.privpwd != privpwd) and
            (auth and mo.auth != auth) and
            (use_aes and mo.use_aes != use_aes)):
            return False
        return True
    return False


def snmp_user_modify(handle, name, descr=None, pwd=None, privpwd=None,
                     auth=None, use_aes=None):
    """
    Modifies snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        descr (string): description
        pwd (string): password
        privpwd (string): privacy password
        auth (string): "md5", "sha"
        use_aes (string): "yes", "no"

    Returns:
        CommSnmpUser: Managed Object

    Raises:
        ValueError: If CommSnmpUser Mo is not present

    Example:
        snmp_user_modify(handle, name="snmpuser", descr="",
                          pwd="password", privpwd="password",
                          auth="md5", use_aes="no")

    """

    dn = "sys/svc-ext/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp user MO is not available")

    if descr is not None:
        mo.descr = descr
    if pwd is not None:
        mo.pwd = pwd
    if privpwd is not None:
        mo.privpwd = privpwd
    if auth is not None:
        mo.auth = auth
    if use_aes is not None:
        mo.use_aes = use_aes

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_user_remove(handle, name):
    """
    removes snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username

    Returns:
        None

    Raises:
        ValueError: If CommSnmpUser Mo is not present

    Example:
        snmp_user_remove(handle, name="snmpuser")

    """

    dn = "sys/svc-ext/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp user MO is not available")

    handle.remove_mo(mo)
    handle.commit()
