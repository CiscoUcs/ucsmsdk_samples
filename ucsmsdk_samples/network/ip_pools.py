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
This module contains methods required for creating IP Pools.
"""

import logging

log = logging.getLogger('ucs')


def ip_pool_create(handle, name, assignment_order,
                   descr="", parent_dn="org-root"):
    """
    Creates IP Pool

    Args:
        handle (UcsHandle)
        name (String) : IP pool name
        assignment_order (String) : ["default", "sequential"]
        descr (String) :
        parent_dn (String) :

    Returns:
        IppoolPool : Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        ip_pool_create(handle, "sample_ip_pool", "default")
    """

    from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool

    obj = handle.query_dn(parent_dn)
    if obj is None:
        raise ValueError("Org %s not found" % parent_dn)
    mo = IppoolPool(parent_mo_or_dn=obj,
                    policy_owner="local",
                    descr=descr,
                    assignment_order=assignment_order,
                    name=name)

    handle.add_mo(mo, True)
    handle.commit()
    return mo

def ip_pool_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified IP Pool
    Args:
        handle (UcsHandle)
        name (String) : IP Pool Name
        parent_dn (String) : Dn of the Org in which the IP Pool reside
    Returns:
        None
    Raises:
        ValueError: If IP Block is not present
    Example:
        ip_block_remove(handle, "cimc", parent_dn="org-root/org-demo/")
    """

    dn = parent_dn + "/ip-pool-" + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Ippool %s is not available" % dn)


def add_ip_block(handle, r_from, to, subnet, default_gw, prim_dns, sec_dns,
                 parent_dn):
    """
    Creates IP Pool block

    Args:
        handle (UcsHandle)
        r_from (String) : Beginning IP Address
        to (String) : Ending IP Address
        subnet (String) : Subnet
        default_gw (String) : default gateway
        prim_dns (String): primary DNS server
        sec_dns (String): secondary DNS server
        parent_dn (String) : Dn of parent

    Returns:
        IppoolBlock: Managed object

    Raises:
        ValueError: If parent dn object is not present

    Example:
        add_ip_block(handle, "1.1.1.1", "1.1.1.10", "255.255.255.0",
                    "1.1.1.254")
    """

    from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

    obj = handle.query_dn(parent_dn)
    if obj is None:
        raise ValueError("IP pool does not exist: %s", parent_dn)
    else:
        log.debug("Creating IP block. from %s to %s, gw=%s, subnet=%s, "
                  "dns1=%s, dns2=%s" % (r_from, to, default_gw, subnet,
                                        prim_dns, sec_dns))
        mo = IppoolBlock(parent_mo_or_dn=obj,
                         r_from=r_from,
                         to=to,
                         subnet=subnet,
                         def_gw=default_gw,
                         prim_dns=prim_dns,
                         sec_dns=sec_dns)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
        

def ip_block_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified IP Block
    Args:
        handle (UcsHandle)
        name (String) : IP Block Name
        parent_dn (String) : Dn of the Org in which the IP Block reside
    Returns:
        None
    Raises:
        ValueError: If IP Block is not present
    Example:
        ip_block_remove(handle, "1.1.1.1-1.1.1.253", parent_dn="org-root/org-demo/ip-pool-cimc")
    """

    dn = parent_dn + "/block-" + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Ipblock %s is not available" % dn)
