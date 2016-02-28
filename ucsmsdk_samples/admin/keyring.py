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
This module performs the operation related to key management.
"""


def key_ring_create(handle, name, descr="", policy_owner="local", tp="",
                    cert="", regen="no", modulus="mod512"):
    """
    Creates a Key Ring

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): description
        policy_owner (string): policy owner
        tp (string): tp
        cert (string): certificate
        regen (string): regen, "false", "no", "true", "yes"
        modulus (string): modulus, valid values are "mod1024", "mod1536",
            "mod2048", "mod2560", "mod3072", "mod3584", "mod4096", "mod512",
            "modinvalid"

    Returns:
        PkiKeyRing: Managed object

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")
    """

    from ucsmsdk.mometa.pki.PkiKeyRing import PkiKeyRing

    mo = PkiKeyRing(parent_mo_or_dn="sys/pki-ext",
                    name=name,
                    descr=descr, policy_owner=policy_owner, tp=tp, cert=cert,
                    regen=regen, modulus=modulus)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def key_ring_exists(handle, name, descr="", policy_owner="local", tp="",
                    cert="", regen="no", modulus="mod512"):
    """
    checks if a Key Ring exists

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): description
        policy_owner (string): policy owner
        tp (string): tp
        cert (string): certificate
        regen (string): regen, "false", "no", "true", "yes"
        modulus (string): modulus, valid values are "mod1024", "mod1536",
            "mod2048", "mod2560", "mod3072", "mod3584", "mod4096", "mod512",
            "modinvalid"

    Returns:
        True/False

    Example:
        key_ring = key_ring_exists(handle, name="mykeyring")
    """

    dn = "sys/pki-ext/keyring-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((descr and mo.descr != descr) and
            (policy_owner and mo.policy_owner != policy_owner) and
            (tp and mo.tp != tp) and
            (cert and mo.cert != cert) and
            (regen and mo.regen != regen) and
            (modulus and mo.modulus != modulus)):
            return False
        return True
    return False


def key_ring_modify(handle, name, descr=None, policy_owner=None, tp=None,
                    cert=None, regen=None, modulus=None):
    """
    Modifies a Key Ring

    Args:
        handle (UcsHandle)
        name (string): name
        descr (string): description
        policy_owner (string): policy owner
        tp (string): tp
        cert (string): certificate
        regen (string): regen, "false", "no", "true", "yes"
        modulus (string): modulus, valid values are "mod1024", "mod1536",
            "mod2048", "mod2560", "mod3072", "mod3584", "mod4096", "mod512",
            "modinvalid"

    Returns:
        PkiKeyRing Object

    Raises:
        ValueError: If PkiKeyRing is not present

    Example:
        key_ring = key_ring_modify(handle, name="mykeyring")
    """

    dn = "sys/pki-ext/keyring-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("keyring '%s' does not exist" % dn)

    if descr is not None:
        mo.descr = descr
    if policy_owner is not None:
        mo.policy_owner = policy_owner
    if tp is not None:
        mo.tp = tp
    if cert is not None:
        mo.cert = cert
    if regen is not None:
        mo.regen = regen
    if modulus is not None:
        mo.modulus = modulus

    handle.set_mo(mo)
    handle.commit()
    return mo


def key_ring_delete(handle, name):
    """
    Deletes a Key Ring

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If PkiKeyRing Mo is not present

    Example:
        key_ring_delete(handle, name="mykeyring")
    """

    dn = "sys/pki-ext/keyring-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("keyring '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def certificate_request_add(handle, name, dns="", locality="", state="",
                            country="", org_name="", org_unit_name="",
                            email="", pwd="", subj_name="", ip="0.0.0.0",
                            ip_a="0.0.0.0", ip_b="0.0.0.0", ipv6="::",
                            ipv6_a="::", ipv6_b="::"):
    """
    Adds a certificate request to keyring

    Args:
        handle (UcsHandle)
        name (string): KeyRing name
        dns (string): dns
        locality (string): locality owner
        state (string): state
        country (string): country
        org_name (string): org_name
        org_unit_name (string): org_unit_name
        email (string): email
        pwd (string): pwd
        subj_name (string): subj_name
        ip (string): ipv4
        ip_a (string):
        ip_b (string):
        ipv6 (string):
        ipv6_a (string):
        ipv6_b (string):

    Returns:
        PkiCertReq: Managed object

    Raises:
        ValueError: If PkiKeyRing is not present

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_add(handle, key_ring=key_ring)
    """

    from ucsmsdk.mometa.pki.PkiCertReq import PkiCertReq

    dn = "sys/pki-ext/keyring-" + name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("keyring '%s' does not exist" % dn)

    mo = PkiCertReq(parent_mo_or_dn=obj,
                    dns=dns,
                    locality=locality,
                    state=state,
                    country=country,
                    org_name=org_name,
                    org_unit_name=org_unit_name,
                    email=email,
                    pwd=pwd,
                    subj_name=subj_name,
                    ip=ip,
                    ip_a=ip_a,
                    ip_b=ip_b,
                    ipv6=ipv6,
                    ipv6_a=ipv6_a,
                    ipv6_b=ipv6_b
                    )
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def certificate_request_exists(handle, name, dns="", locality="", state="",
                               country="", org_name="", org_unit_name="",
                               email="", pwd="", subj_name="", ip="0.0.0.0",
                               ip_a="0.0.0.0", ip_b="0.0.0.0", ipv6="::",
                               ipv6_a="::", ipv6_b="::"):
    """
    Checks if a certificate request exists

    Args:
        handle (UcsHandle)
        name (string): KeyRing name
        dns (string): dns
        locality (string): locality owner
        state (string): state
        country (string): country
        org_name (string): org_name
        org_unit_name (string): org_unit_name
        email (string): email
        pwd (string): pwd
        subj_name (string): subj_name
        ip (string): ipv4
        ip_a (string):
        ip_b (string):
        ipv6 (string):
        ipv6_a (string):
        ipv6_b (string):

    Returns:
        True/False

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_exists(handle, key_ring="keyring")
    """

    dn = "sys/pki-ext/keyring-" + name + "certreq"
    mo = handle.query_dn(dn)
    if mo:
        if ((dns and mo.dns != dns) and
            (locality and mo.locality != locality) and
            (state and mo.state != state) and
            (country and mo.country != country) and
            (org_name and mo.org_name != org_name) and
            (org_unit_name and mo.org_unit_name != org_unit_name) and
            (email and mo.email != email) and
            (pwd and mo.pwd != pwd) and
            (subj_name and mo.subj_name != subj_name) and
            (ip and mo.ip != ip) and
            (ip_a and mo.ip_a != ip_a) and
            (ip_b and mo.ip_b != ip_b) and
            (ipv6 and mo.ipv6 != ipv6) and
            (ipv6_a and mo.ipv6_a != ipv6_a) and
            (ipv6_b and mo.ipv6_b != ipv6_b)):
            return False
        return True
    return False


def certificate_request_modify(handle, name, dns=None, locality=None,
                               state=None, country=None, org_name=None,
                               org_unit_name=None, email=None, pwd=None,
                               subj_name=None, ip=None, ip_a=None, ip_b=None,
                               ipv6=None, ipv6_a=None, ipv6_b=None):
    """
    modifies a certificate request

    Args:
        handle (UcsHandle)
        name (string): KeyRing name
        dns (string): dns
        locality (string): locality owner
        state (string): state
        country (string): country
        org_name (string): org_name
        org_unit_name (string): org_unit_name
        email (string): email
        pwd (string): pwd
        subj_name (string): subj_name
        ip (string): ipv4
        ip_a (string):
        ip_b (string):
        ipv6 (string):
        ipv6_a (string):
        ipv6_b (string):

    Returns:
        PkiCertReq Object

    Raises:
        ValueError: If PkiCertReq is not present

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_add(handle, key_ring="keyring")
    """

    dn = "sys/pki-ext/keyring-" + name + "certreq"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("keyring certificate '%s' does not exist" % dn)

    if dns is not None:
        mo.dns = dns
    if locality is not None:
        mo.locality = locality
    if state is not None:
        mo.state = state
    if country is not None:
        mo.country = country
    if org_name is not None:
        mo.org_name = org_name
    if org_unit_name is not None:
        mo.org_unit_name = org_unit_name
    if email is not None:
        mo.email = email
    if pwd is not None:
        mo.pwd = pwd
    if subj_name is not None:
        mo.subj_name = subj_name
    if ip is not None:
        mo.ip = ip
    if ip_a is not None:
        mo.ip_a = ip_a
    if ip_b is not None:
        mo.ip_b = ip_b
    if ipv6 is not None:
        mo.ipv6 = ipv6
    if ipv6_a is not None:
        mo.ipv6_a = ipv6_a
    if ipv6_b is not None:
        mo.ipv6_b = ipv6_b

    handle.set_mo(mo)
    handle.commit()
    return mo


def certificate_request_remove(handle, name):
    """
    Removes a certificate request from keyring

    Args:
        handle (UcsHandle)
        name (string): KeyRing name

    Returns:
        None

    Raises:
        ValueError: If PkiCertReq is not present

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_remove(handle, key_ring=key_ring)

    """

    dn = "sys/pki-ext/keyring-" + name + "certreq"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("keyring certificate '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()
