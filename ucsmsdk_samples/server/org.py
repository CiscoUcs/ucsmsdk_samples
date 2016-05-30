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


def org_create(handle, name, descr="", parent_dn="org-root"):

    """
    This method creates sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        descr (string): Basic description about the org.
        parent_dn (string): org dn

    Returns:
        OrgOrg: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        org_create(handle, name="sample_org")
    """

    from ucsmsdk.mometa.org.OrgOrg import OrgOrg

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist")

    mo = OrgOrg(parent_mo_or_dn=parent_dn, name=name, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def org_modify(handle, name, descr=None, parent_dn="org-root"):
    """
    This method modifies sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        descr (string): Basic description about the org.
        parent_dn (string): org dn

    Returns:
        OrgOrg: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        org_modify(handle, name="sample_org", descr="My Org")
    """

    dn = parent_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("org '%s' does not exist" % dn)

    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def org_remove_by_dn(handle, org_dn):
    """
    This method removes sub organization by DN.

    Args:
        handle (UcsHandle)
        org_dn (string): DN of the organization

    Returns:
        None

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        org_remove(handle, org_dn="org-root/org-sample")
    """

    mo = handle.query_dn(org_dn)
    if not mo:
        raise ValueError("org '%s' does not exist" % org_dn)
    handle.remove_mo(mo)
    handle.commit()


def org_remove(handle, name, parent_dn="org-root"):
    """
    This method removes sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        parent_dn (string):

    Returns:
        None

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        org_remove(handle, name="sample_org")
    """

    dn = parent_dn + "/org-" + name
    org_remove_by_dn(handle, dn)


def org_exists(handle, name, descr="", parent_dn="org-root"):
    """
    Check if given org already exists.

    Args:
        handle (UcsHandle)
        name (string): Name of  organization
        descr (string): Basic description about the org
        parent_dn (string):

    Returns:
        True/False (Boolean)

    Example:
        org_exists(handle, name="sample_org")
    """

    dn = parent_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False
