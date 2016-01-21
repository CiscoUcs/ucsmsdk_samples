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


def sol_policy_create(handle, name, admin_state,
                      speed="9600", descr="",
                      parent_dn="org-root"):
    """
    This method creates SoL policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the SoL policy.
        admin_state (string): "enable" or "disable"
        speed (string): Speed on SoL e.g. "9600"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Example:
        sol_policy_create(handle,
                         name="sample_SoL", admin_state="enable",
                         speed="9600")

    """
    obj = handle.query_dn(parent_dn)
    if obj:
        from ucsmsdk.mometa.sol.SolPolicy import SolPolicy

        mo = SolPolicy(parent_mo_or_dn=parent_dn, speed=speed,
                       admin_state=admin_state,
                       name=name, descr=descr)
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        log.info("Sub-Org <%s> not found!" % org_name)


def sol_policy_modify(handle, org_name, name, admin_state=None,
                      speed=None, descr=None,
                      org_parent="org-root"):
    """
    This method creates SoL policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the SoL policy.
        admin_state (string): "enable" or "disable"
        speed (string): Speed on SoL e.g. "9600"
        descr (string): Basic description.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        sol_policy_modify(handle, org_name="sample-org",
                         name="sample_SoL", admin_state="enable",
                         speed="9600")

    """
    org_dn = org_parent + "/org-" + org_name
    policy_dn= org_dn + "sol/-" + name
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        if admin_state is not None:
            mo.admin_state = admin_state
        if speed is not None:
            mo.speed = speed
        if descr is not None:
            mo.descr = descr

        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Serial over lan policy <%s> not found.Nothing to remove"
                 % name)


def sol_policy_remove(handle, org_name, name, org_parent="org-root"):
    """
    This method removes SoL policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the SoL policy.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        sol_policy_remove(handle, org_name="sample-org",
                                name="sample_SoL")
    """
    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        policy_dn= org_dn + "sol/-" + name
        mo = handle.query_dn(policy_dn)
        if not mo:
            log.info("Serial over lan policy <%s> not found.Nothing to remove"
                     %name)
        else:
            handle.remove_mo(mo)
            handle.commit()
