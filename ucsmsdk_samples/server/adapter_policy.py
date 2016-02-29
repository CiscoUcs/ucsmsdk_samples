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


def adapter_policy_create(handle, name, descr="", parent_dn="org-root"):
    """
    This method creates AdaptorHostEthIfProfile policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the AdaptorHostEthIfProfile policy.
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
       AdaptorHostEthIfProfile: Managed Object

    Example:
        adapter_policy_create(handle, name="sample_adapter_pol",
        parent_dn="org-root/org-sub")

    """

    from ucsmsdk.mometa.adaptor.AdaptorHostEthIfProfile import \
        AdaptorHostEthIfProfile

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
