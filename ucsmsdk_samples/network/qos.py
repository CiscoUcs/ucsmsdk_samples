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
This module contains methods required for configuring QoS.
"""


def qos_class_enable(handle, priority, cos, drop, weight, mtu, multicast_optimize):
    """
    Enables and configures a QoS System Class

    Args:
        handle (UcsHandle)
        priority (String) : ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]
        cos (String): ["any"], ["0-6", "255-255"]
        drop (String) : ["drop", "no-drop"]
        weight (String) : ["best-effort", "none"], ["0-10"]
        mtu (String) : ["fc", "normal"], ["0-4294967295"]
        multicast_optimize (String) : ["false", "no", "true", "yes"]

    Returns:
        QosclassEthClassified: Managed object

    Raises:
        ValueError: When the Qos class is not present
    Example:
        qos_class_enable(handle, "platinum", "enabled", "6", "drop", "9", "fc", "yes")
    """
    from ucsmsdk.mometa.qosclass.QosclassEthClassified import QosclassEthClassified

    qos_class = QosclassEthClassified(parent_mo_or_dn="fabric/lan/classes",
                                  cos=cos,
                                  name="",
                                  weight=weight,
                                  drop=drop,
                                  multicast_optimize=multicast_optimize,
                                  mtu=mtu,
                                  priority=priority,
                                  admin_state="enabled")

    handle.set_mo(qos_class)
    handle.commit()
    return qos_class


def qos_class_disable(handle, priority):
    """
    Disables a QoS System Class

    Args:
        handle (UcsHandle)
        priority (String) : ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]

    Returns:
        QosclassEthClassified: Managed object

    Raises:
        ValueError: When the Qos class is not present

    Example:
        qos_class_disable(handle, "platinum")
    """
    qos_class = handle.query_dn("fabric/lan/classes/class-" + priority)
    if qos_class:
        qos_class.admin_state = admin_state
    else:
        raise ValueError("QoS class is not available")

    handle.set_mo(qos_class)
    handle.commit()
    return qos_class


def qos_class_exists(handle, priority, admin_state=None, cos=None, drop=None,
                     weight=None, mtu=None, multicast_optimize=None):
    """
    Checks if the Mo with the specified Params already exists

    Args:
        handle (UcsHandle)
        priority (String) : ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]
        admin_state (String) : ["disabled", "enabled"]
        cos (String): ["any"], ["0-6", "255-255"]
        drop (String) : ["drop", "no-drop"]
        weight (String) : ["best-effort", "none"], ["0-10"]
        mtu (String) : ["fc", "normal"], ["0-4294967295"]
        multicast_optimize (String) : ["false", "no", "true", "yes"]

    Returns:
        True/False - bool

    Example:
        bool_var = qos_class_exists(handle, "platinum", "enabled", "6", "drop", "9", "fc", "yes")

    """
    dn = "fabric/lan/classes/class-" + priority
    mo = handle.query_dn(dn)
    if mo:
        if ((admin_state and mo.admin_state != admin_state) and
            (cos and mo.cos != cos) and
            (drop and mo.drop != drop) and
            (weight and mo.weight != weight) and
            (mtu and mo.mtu != mtu) and
            (multicast_optimize and mo.multicast_optimize != multicast_optimize)):
            return False
        return True
    return False

def qos_policy_add(handle, name, priority, burst, rate,
                      host_control, descr="", parent_dn="org-root"):
    """
    Creates QoS Policy

    Args:
        handle (UcsHandle)
        name (String) : QoS Policy Name
        priority (String) : ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]
        burst (uint):
        rate (String) : ["line-rate"], ["8-40000000"]
        host_control (string) : ["full", "full-with-exception", "none"]
        descr (String) :
        parent_dn (String) :

    Returns:
        EpqosDefinition: Managed object

    Raises:
        ValueError: If EpqosDefinition is not present

    Example:
        mo = qos_policy_create(handle, "sample_qos", "platinum", 10240, "line-rate", "full")
    """
    from ucsmsdk.mometa.epqos.EpqosDefinition import EpqosDefinition
    from ucsmsdk.mometa.epqos.EpqosEgress import EpqosEgress

    obj = handle.query_dn(parent_dn)
    if obj:
        mo = EpqosDefinition(parent_mo_or_dn=obj,
                             policy_owner="local",
                             name=name,
                             descr=descr)
        mo_1 = EpqosEgress(parent_mo_or_dn=mo,
                           rate=rate,
                           host_control=host_control,
                           name="",
                           prio=priority,
                           burst=burst)

        handle.add_mo(mo)
        handle.commit()
        return mo
    else:
        raise ValueError(parent_dn + " MO is not available")


def qos_policy_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified qos policy

    Args:
        handle (UcsHandle)
        name (String) : QoS Policy Name
        parent_dn (String) : Dn of the Org in which the policy should reside

    Returns:
        None

    Raises:
        ValueError: If the policy is not found

    Example:
        qos_policy_remove(handle, "sample_qos", parent_dn="org-root")
        qos_policy_remove(handle, "demo_qos_policy", parent_dn="org-root/org-demo")
    """
    dn = parent_dn + '/ep-qos-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Qos Policy is not available")


def qos_policy_exists(handle, name, priority=None, burst=None, rate=None,
                      host_control=None, parent_dn="org-root"):
    """
    Checks if the given qos policy already exists with the same params

    Args:
        handle (UcsHandle)
        name (String) : QoS Policy Name
        priority (String) : ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]
        burst (uint):
        rate (String) : ["line-rate"], ["8-40000000"]
        host_control (string) : ["full", "full-with-exception", "none"]
        descr (String) :
        parent_dn (String) :

    Returns:
        True/False (Boolean)

    Example:
        bool_var = qos_policy_exists(handle, "sample_qos", "platinum", 10240, "line-rate", "full")
    """
    dn = parent_dn + '/ep-qos-' + name
    mo = handle.query_dn(dn)
    if mo:
        if ((priority and mo.priority != priority) and
            (burst and mo.burst != burst) and
            (rate and mo.rate != rate) and
            (host_control and mo.host_control != host_control)):
            return False
        return True
    return False
