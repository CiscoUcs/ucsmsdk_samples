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
This module contains methods required for creating MAC Pools.
"""


def mac_pool_create(handle, name, assignment_order,
                    r_from, to, descr="", parent_dn="org-root"):
    """
    Creates MAC Pool

    Args:
        handle (UcsHandle)
        name (String) : Network Control Policy Name
        assignment_order (String) : ["default", "sequential"]
        r_from (String) : Beginning MAC Address
        to (String) : Ending MAC Address
        descr (String) :
        parent_dn (String) :

    Returns:
        MacpoolPool: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        mac_pool_create(handle, "sample_mac_pool", "default",
                    "00:25:B5:00:00:00", "00:25:B5:00:00:03")
    """
    from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
    from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = MacpoolPool(parent_mo_or_dn=obj,
                         policy_owner="local",
                         descr=descr,
                         assignment_order=assignment_order,
                         name=name)
        MacpoolBlock(parent_mo_or_dn=mo,
                     to=to,
                     r_from=r_from)

        handle.add_mo(mo, modify_present=True)
        handle.commit()
        return mo
    else:
        raise ValueError("org '%s' is not available" % parent_dn)


def mac_pool_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified MAC Pool

    Args:
        handle (UcsHandle)
        name (String) : MAC Pool Name
        parent_dn (String) : Dn of the Org in which the MAC Pool should reside

    Returns:
        None

    Raises:
        ValueError: If MacpoolPool is not present

    Example:
        mac_pool_remove(handle, "sample_mac", parent_dn="org-root")
        mac_pool_remove(handle, "demo_mac_pool", parent_dn="org-root/org-demo")
    """

    dn = parent_dn + '/mac-pool-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Macpool %s is not available" % dn)


def mac_pool_exists(handle, name, assignment_order=None,
                    r_from=None, to=None, descr=None, parent_dn="org-root"):
    """
    Checks if the given MAC Pool already exists with the same params

    Args:
        handle (UcsHandle)
        name (String) : Network Control Policy Name
        assignment_order (String) : ["default", "sequential"]
        r_from (String) : Beginning MAC Address
        to (String) : Ending MAC Address
        descr (String) : description
        parent_dn (String) : org dn

    Returns:
        True/False (Boolean)

    Example:
        bool_var = mac_pool_exists(handle, "sample_mac_pool", "default",
                        "00:25:B5:00:00:00", "00:25:B5:00:00:03")
    """

    dn = parent_dn + '/mac-pool-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((assignment_order and mo.assignment_order != assignment_order) and
                (r_from and mo.r_from != r_from) and
                (to and mo.to != to) and
                (descr and mo.descr != descr)):
            return False
        return True
    return False
