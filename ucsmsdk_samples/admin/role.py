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


def role_create(handle, name, priv, descr="", policy_owner="local"):
    """
    creates and modify role

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        policy_owner (string): policy owner

    Returns:
        AaaRole Object

    Example:

    """

    from ucsmsdk.mometa.aaa.AaaRole import AaaRole

    mo = AaaRole(parent_mo_or_dn="sys/user-ext",
                 name=name,
                 priv=priv,
                 descr=descr,
                 policy_owner=policy_owner)
    handle.add_mo(mo)
    handle.commit()


def role_modify(handle, name, priv=None, descr=None, policy_owner=None):
    """
    creates and modify role

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        policy_owner (string): policy owner

    Returns:
        AaaRole Object

    Example:

    """

    dn = "sys/user-ext/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Role does not exist")

    if priv is not None:
        mo.priv = priv
    if descr is not None:
        mo.descr = descr
    if policy_owner is not None:
        mo.policy_owner = policy_owner

    handle.set_mo(mo)
    handle.commit()


def role_delete(handle, name):
    """
    deletes role

    Args:
        handle (UcsHandle)
        name (string): role name

    Returns:
        None

    Example:

    """

    dn = "sys/user-ext/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Role does not exist")

    handle.remove_mo(mo)
    handle.commit()


