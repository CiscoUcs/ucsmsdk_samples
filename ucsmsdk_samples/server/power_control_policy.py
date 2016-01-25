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


def power_control_policy_create(handle, name, prio="no-cap",
                                    descr="",parent_dn="org-root"):
    """
    This method creates power control policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the power control policy.
        prio (string): ."no-cap" or "utility"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        power_control_policy_create(handle,
                                name="sample_power", prio="no-cap")
    """

    obj = handle.query_dn(parent_dn)
    if obj:
        from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy

        mo = PowerPolicy(parent_mo_or_dn=parent_dn,
                         name=name, prio=prio,
                         descr=descr)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" %org_name)


def power_control_policy_modify(handle, org_name, name, prio=None,
                                    descr=None,org_parent="org-root"):
    """
    This method creates power control policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the power control policy.
        prio (string): ."no-cap" or "utility"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        power_control_policy_create(handle, org_name="sample-org",
                                name="sample_power", prio="no-cap")
    """

    org_dn = org_parent + "/org-" + org_name
    policy_dn= org_dn + "/power-policy-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        if prio is not None:
            mo.prio = prio
        if descr is not None:
            mo.descr = descr

        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Power Control Policy <%s> not found." % name)


def power_control_policy_remove(handle,org_name,name, org_parent="org-root"):
    """
    This method removes power control policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the power control policy.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        power_control_policy_remove(handle, org_name="sample-org",
                                name="sample_power")
    """
    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "/power-policy-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Power Control Policy <%s> not found.Nothing to remove."
                     %name)
        else:
            handle.remove_mo(mo)
            handle.commit()
