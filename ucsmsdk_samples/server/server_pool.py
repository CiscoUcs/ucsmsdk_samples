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

from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledRackUnit import ComputePooledRackUnit
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot


def server_pool_create(handle, name, descr="", parent_dn="org-root"):
    """
    This method creates ComputePool.

    Args:
        handle (UcsHandle)
        name (string): Name of the ComputePool.
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
       ComputePool: Managed Object

    Example:
        server_pool_create(handle, name="sample_compute_pool",
        parent_dn="org-root/org-sub")

    """

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = ComputePool(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def server_pool_add_rack_unit(handle, rack_id, parent_dn="org-root"):
    """
    This method adds a rack server to a ComputePool.

    Args:
        handle (UcsHandle)
        rack_id (string): ID of rack server to add
        parent_dn (string): Parent of Org.

    Returns:
       ComputePooledRackUnit: Managed Object

    Example:
        server_pool_add_rack_unit(handle, rack_id=1,
        parent_dn="org-root/org-sub/compute-pool-sample_compute_pool")

    """

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)
    if not isinstance(obj, ComputePool):
        raise TypeError("Object {0} is not a ComputePool".format(obj.dn))

    mo = ComputePooledRackUnit(parent_mo_or_dn=parent_dn, id=str(rack_id))
    handle.add_mo(mo)
    handle.commit()
    return mo


def server_pool_add_slot(handle, chassis_id, slot_id, parent_dn="org-root"):
    """
    This method adds a blade server to a ComputePool.

    Args:
        handle (UcsHandle)
        chassis_id (string): ID of chassis in which blade inserted.
        slot_id (string): ID of slot in which blade is inserted.
        parent_dn (string): Parent of Org.

    Returns:
       ComputePooledSlot: Managed Object

    Example:
        server_pool_add_slot(handle, chassis_id="1", slot_id="1",
        parent_dn="org-root/org-sub/compute-pool-sample_compute_pool")

    """

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)
    if not isinstance(obj, ComputePool):
        raise TypeError("Object {0} is not a ComputePool".format(obj.dn))

    mo = ComputePooledSlot(parent_mo_or_dn=parent_dn, slot_id=str(slot_id),
                           chassis_id=str(chassis_id))
    handle.add_mo(mo)
    handle.commit()
    return mo


def server_pool_exists(handle, parent_dn="org-root"):
    """
    This method adds a validates if a server pool exists.

    Args:
        handle (UcsHandle)
        parent_dn (string): Parent of Org.

    Returns:
       ComputePooledSlot: Managed Object

    Example:
        server_pool_add_slot(handle,
        parent_dn="org-root/org-sub/compute-pool-sample_compute_pool")

    """

    obj = handle.query_dn(parent_dn)
    if not obj:
        return False
    if not isinstance(obj, ComputePool):
        raise TypeError("Object {0} is not a ComputePool".format(obj.dn))
    else:
        return True
