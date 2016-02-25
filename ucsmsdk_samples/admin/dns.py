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


def dns_server_add(handle, name, descr=""):
    """
    Adds a dns server

    Args:
        handle (UcsHandle)
        descr (string): description
        name (string): IP Address of dns server

    Returns:
        CommDnsProvider: Managed object

    Example:
        mo = dns_server_add(handle, name="8.8.8.8", descr="dns_google")
    """

    from ucsmsdk.mometa.comm.CommDnsProvider import CommDnsProvider

    mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name=name,
                         descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def dns_server_remove(handle, name):
    """
    Removes a dns server

    Args:
        handle (UcsHandle)
        name (string): IP Address of the dns server

    Returns:
        None

    Raises:
        ValueError: If CommDnsProvider is not present

    Example:
        dns_server_remove(handle, "10.10.10.10")
    """

    dn = "sys/svc-ext/dns-svc/dns-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("dns server '%s' not found" % dn)

    handle.remove_mo(mo)
    handle.commit()


def dns_server_exists(handle, name, descr=None):
    """
    Checks if the dns entry already exists

    Args:
        handle (UcsHandle)
        name (string): IP address of the dns server

    Returns:
        True/False(bool)

    Example:
        bool_var = dns_server_exists(handle, "10.10.10.10")
    """

    dn = "sys/svc-ext/dns-svc/dns-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and (mo.descr != descr):
            return False
        return True
    return False
