# Copyright 2016 Cisco Systems, Inc.
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


from ucsmsdk.mometa.aaa.AaaEpAuthProfile import AaaEpAuthProfile
from ucsmsdk.mometa.aaa.AaaEpUser import AaaEpUser


def ipmi_policy_create(handle, name, descr="", parent_dn="org-root",
                       username="admin", password=None):
    """
    This method creates AaaEpAuthProfile policy, with optional
    username and password.

    Args:
        handle (UcsHandle)
        name (string): Name of the AaaEpAuthProfile policy.
        descr (string): Basic description.
        parent_dn (string): Parent of Org.
        username (string): username for authenticating the IPMI
        password (string): password of user

    Returns:
       AaaEpAuthProfile: Managed Object

    Example:
        ipmi_policy_create(handle, name="sample_ipmi_pol",
        parent_dn="org-root/org-sub")

    """

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = AaaEpAuthProfile(parent_mo_or_dn=obj, policy_owner="local",
                          ipmi_over_lan="enable", name=name, descr=descr)
    if password is not None:
        AaaEpUser(parent_mo_or_dn=mo, pwd=password, name=username,
                  descr="", priv="admin")
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
