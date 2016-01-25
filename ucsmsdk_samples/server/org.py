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

import logging
log = logging.getLogger('ucs')


def org_create(handle, name, descr="",parent_dn="org-root"):

    """
    This method creates sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        descr (string): Basic description about the org.
        parent_dn (string):

    Returns:
        OrgOrg: managed object

    Example:
        org_create(handle, name="sample_org")
    """

    from ucsmsdk.mometa.org.OrgOrg import OrgOrg

    mo = OrgOrg(parent_mo_or_dn=parent_dn, name=name, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def org_modify(handle,name, descr=None, parent_dn="org-root"):
    """
    This method modifies sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        descr (string): Basic description about the org.
        parent_dn (string):

    Returns:
        None

    Example:
        org_modify(handle, name="sample_org", descr="My Org")
    """
    dn = parent_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if mo is not None:
        if descr is not None:
            mo.descr = descr
        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found" %name)


def org_remove(handle,name,parent_dn="org-root"):
    """
    This method removes sub organization.

    Args:
        handle (UcsHandle)
        name (string): Name of the organization
        parent_dn (string):

    Returns:
        None

    Example:
        org_remove(handle, name="sample_org")
    """

    dn = parent_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        log.info("Sub-Org <%s> not found.Nothing to remove." %name)
    else:
        handle.remove_mo(mo)
        handle.commit()
