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
This module contains methods required for creating UUID Pools.
"""


def uuid_pool_create(handle, name, descr="", prefix="derived", assignment_order="default", parent_dn="org-root"):
    """
    This method creates Maintenance policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the maintenance policy.
        prefix (string) : "derived" or UUID prefix value
        assignment_order (string): "default" or "sequential"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        UuidpoolPool: Managed Object

    Raises:
        TypeError: If Name is not present

    Example:
        maintenance_policy_create(handle, name="sample_uuid_pool",
                                    prefix="derived",
                                    assignment_order="sequential",
                                    parent_dn="org-root")

    """

    from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool

    mo = UuidpoolPool(parent_mo_or_dn=parent_dn,
                      prefix=prefix,
                      descr=descr,
                      assignment_order=assignment_order,
                      name=name)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def uuid_block_create(handle, parent_mo, r_from, to):
    """
    This method creates a UUID block.

    Args:
        handle (UcsHandle)
        parent_mo (ManagedObject): UUID pool block is added to
        r_from (string) : Starting range of UUID Block
        to (string): End of block range

    Returns:
        UuidpoolPool: Managed Object

    Raises:
        TypeError: If any input is not present

    Example:
        maintenance_policy_create(handle, parent_mo=mo,
                                    r_from="0000-010101000000",
                                    to="0000-010101000100")
    """

    from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock

    UuidpoolBlock(parent_mo_or_dn=parent_mo,
                  to=to,
                  r_from=r_from)

    handle.add_mo(parent_mo, True)
    handle.commit()
    return parent_mo
