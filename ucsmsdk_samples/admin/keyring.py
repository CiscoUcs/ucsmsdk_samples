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


def key_ring_add(handle, name, descr="", policy_owner="local", tp="",
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
        key_ring = key_ring_add(handle, name="mykeyring")
    """

    from ucsmsdk.mometa.pki.PkiKeyRing import PkiKeyRing

    mo = PkiKeyRing(parent_mo_or_dn="sys/pki-ext",
                    name=name,
                    descr=descr, policy_owner=policy_owner, tp=tp, cert=cert,
                    regen=regen, modulus=modulus)
    handle.add_mo(mo)
    handle.commit()
    return mo


def key_ring_remove(handle, name):
    """
    Creates a Key Ring

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If PkiKeyRing Mo is not present

    Example:
        key_ring_remove(handle, name="mykeyring")
    """

    dn = "sys/pki-ext/keyring-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("keyring not found")


def certificate_request_add(handle, key_ring, dns="", locality="", state="",
                            country="", org_name="", org_unit_name="",
                            email="", pwd="", subj_name="", ip="0.0.0.0",
                            ip_a="0.0.0.0", ip_b="0.0.0.0", ipv6="::",
                            ipv6_a="::", ipv6_b="::"):
    """
    Adds a certificate request to keyring

    Args:
        handle (UcsHandle)
        key_ring (PkiKeyRing): KeyRing Object
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

    Example:
        key_ring = key_ring_add(handle, name="mykeyring")

        certificate_request_add(handle, key_ring=key_ring)
    """

    from ucsmsdk.mometa.pki.PkiCertReq import PkiCertReq
    mo = PkiCertReq(parent_mo_or_dn=key_ring,
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


def certificate_request_remove(handle, key_ring):
    """
    Removes a certificate request from keyring

    Args:
        handle (UcsHandle)
        key_ring (PkiKeyRing): KeyRing Object

    Returns:
        None

    Raises:
        ValueError: If PkiCertReq Mo is not present

    Example:
        key_ring = key_ring_add(handle, name="mykeyring")

        certificate_request_remove(handle, key_ring=key_ring)

    """
    dn = key_ring.dn + "/certreq"
    mo = handle.query_dn(dn)
    if mo is not None:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("certificate not found")
