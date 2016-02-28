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

log = logging.getLogger("ucs")


def vmedia_policy_create(handle, org_dn, name, retry_on_mount_fail="yes",
                         descr="", policy_owner="local"):
    """
    Creates a vMedia Policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the org in which policy is required
        name (string) : name of the policy
        retry_on_mount_fail (string): "yes", "no"
        descr (string): description of the policy
        policy_owner (string): "local", "global". Default is local

    Returns:
        CimcvmediaMountConfigPolicy: Managed object

    Raises:
        ValueError: If OrgOrg does not exist

    Example:
        mo = vmedia_policy_create(handle=handle, org_dn="org-root",
                                    name="demo_policy")
    """

    from ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy import \
        CimcvmediaMountConfigPolicy

    org = handle.query_dn(org_dn)
    if org is None:
        raise ValueError("Org '%s' does not exist" % org_dn)

    mo = CimcvmediaMountConfigPolicy(parent_mo_or_dn=org,
                                     name=name,
                                     retry_on_mount_fail=retry_on_mount_fail,
                                     policy_owner=policy_owner,
                                     descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def vmedia_mount_add(handle, vmedia_policy_dn, mapping_name, device_type,
                     mount_protocol, remote_ip_address, image_name_variable,
                     image_file_name, image_path, remote_port="0",
                     user_id="", password="", description="",
                     auth_option="default"):
    """
    Creates a new vMedia mount entry

    Args:
        handle (UcsHandle)
        vmedia_policy_dn (string): the dn of the vmedia policy
        mapping_name (string) : name of the map. This is just a string label.
        device_type (string): "cdd", "hdd"
        mount_protocol (string): "cifs", "http", "https", "nfs"
        remote_ip_address (string): IP address of the remote server
        image_name_variable (string):
        image_file_name (string): filename of the image to be downloaded
        image_path (string): path of the image on the remote server
        remote_port (string): port number to connect to.
        user_id (string): username
        password (string): password
        description (string): description for the mount entry
        auth_option (string): "default", "none", "ntlm", "ntlmi", "ntlmssp",
                                "ntlmsspi", "ntlmv2", "ntlmv2i"

    Returns:
        CimcvmediaConfigMountEntry: Managed Object

    Raises:
        ValueError: If CimcvmediaMountConfigPolicy does not exist

    Example:
        mo = vmedia_mount_add(handle, vmedia_policy_dn,
                            mapping_name="ubuntu_1404",
                            device_type="cdd",
                            mount_protocol="nfs",
                            remote_ip_address="10.105.219.128",
                            image_name_variable="none",
                            image_file_name="ubuntu-14.04.3-desktop-amd64.iso",
                            image_path="/isoimages")
    """

    from ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry import \
        CimcvmediaConfigMountEntry

    mo = handle.query_dn(vmedia_policy_dn)
    if mo is None:
        raise ValueError("vmedia policy does not exist.")
    mo = CimcvmediaConfigMountEntry(parent_mo_or_dn=mo,
                                    mapping_name=mapping_name,
                                    device_type=device_type,
                                    mount_protocol=mount_protocol,
                                    remote_ip_address=remote_ip_address,
                                    image_name_variable=image_name_variable,
                                    image_file_name=image_file_name,
                                    image_path=image_path,
                                    remote_port=remote_port,
                                    user_id=user_id,
                                    password=password,
                                    description=description,
                                    auth_option=auth_option)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def vmedia_mount_remove(handle, vmedia_policy_dn, mapping_name):
    """
    Deletes the specified vMedia mount entry

    Args:
        handle (UcsHandle)
        vmedia_policy_dn (string): the dn of the vmedia policy
        mapping_name (string) : name of the map. This is just a string label.

    Returns:
        None

    Raises:
        ValueError: if CimcvmediaConfigMountEntry does not exist

    Example:
        mo = vmedia_mount_remove(handle=handle, vmedia_policy_dn=policy_dn,
                                    mapping_name="ubuntu_1404")
    """
    dn = vmedia_policy_dn + "/cfg-mnt-entry-" + mapping_name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("vmedia mount does not exist.")

    handle.remove_mo()
    handle.commit()


def vmedia_policy_delete(handle, org_dn, name):
    """
    Deletes the specified vMedia policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the vmedia policy
        name (string) : name of the policy to delete

    Returns:
        None

    Raises:
        ValueError: If CimcvmediaMountConfigPolicy does not exist

    Example:
        mo = vmedia_policy_delete(handle=handle, org_dn="org-root",
                                    name="demo-policy")
    """
    dn = org_dn + "/mnt-cfg-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("vmedia_policy does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def vmedia_sp_attach(handle, sp_dn, vmedia_policy_name):
    """
    Attaches a vMedia policy to the specified service profile

    Args:
        handle (UcsHandle)
        sp_dn (string): the dn of the service profile to attach to
        vmedia_policy_name (string) : name of the vmedia policy

    Returns:
        LsServer: Managed object

    Raises:
        ValueError: If CimcvmediaMountConfigPolicy or LsServer does not exist

    Example:
        mo = vmedia_sp_attach(handle=handle, sp_dn="org-root/ls-demo_sp",
                                    name="demo-policy")
    """
    import os

    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("sp does not exist.")

    org_dn = os.path.dirname(sp_dn)
    vmedia_policy_dn = org_dn + "/mnt-cfg-policy-" + vmedia_policy_name
    vmedia_policy = handle.query_dn(vmedia_policy_dn)
    if vmedia_policy is None:
        raise ValueError("vmedia_policy does not exist.")

    sp.vmedia_policy_name = vmedia_policy_name
    handle.set_mo(sp)
    handle.commit()
    return sp


def vmedia_sp_detach(handle, sp_dn):
    """
    Detaches vMedia policy from the specified service profile

    Args:
        handle (UcsHandle)
        sp_dn (string): the dn of the service profile to detach from

    Returns:
        LsServer: Managed object

    Raises:
        ValueError: if LsServer does not exist

    Example:
        mo = vmedia_sp_detach(handle=handle, sp_dn="org-root/ls-demo_sp")
    """
    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("sp does not exist.")

    sp.vmedia_policy_name = ""
    handle.set_mo(sp)
    handle.commit()
    return sp


def vmedia_mount_state(handle, sp_dn):
    """
    Queries the state of a mount entry

    Args:
        handle (UcsHandle)
        sp_dn (string): the dn of the service profile

    Returns:
        List of CimcvmediaConfigMountEntry Managed Objects

    Raises:
        ValueError: If LsServer does not exist Or
                    LsServer.assoc_state != "associated" Or
                    associated ComputeBlade does not exist Or
                    MgmtController does not exist Or
                    CimcvmediaMountConfigPolicy does not exist Or
                    CimcvmediaConfigMountEntry

    Example:
        mount_entries_array = vmedia_mount_state(handle=handle,
                                        sp_dn="org-root/ls-demo_sp")
    """

    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("Service Profile does not exist.")

    if not sp.pn_dn:
        raise ValueError("Service profile is not associated.")

    asociated_blade = handle.query_dn(sp.pn_dn)
    if asociated_blade is None:
        raise ValueError("Blade does not exist")

    mgmt_controller_dn = asociated_blade.dn + "/mgmt"
    mgmt_controller = handle.query_dn(mgmt_controller_dn)
    if mgmt_controller is None:
        raise ValueError("Management Controller does not exist.")

    actual_mount_list = handle.query_children(
        in_mo=mgmt_controller,
        class_id="CimcvmediaActualMountList")
    if not actual_mount_list:
        raise ValueError("Vmedia Mount does not exist.")

    mount_entries = handle.query_children(
        in_mo=actual_mount_list[0],
        class_id="CimcvmediaActualMountEntry")
    if not mount_entries:
        raise ValueError("Vmedia Mount Entries do not exist.")

    mnt_state = {
        "unknown": "Mapping is not present",
        "not-mounted": "Mapping is not present",
        "unmounting": "Unmounting in progress",
        "mounting": "Mounting in progress",
        "mounted": "Mounted successfully",
        "mount-failed": "Mounting failed",
    }
    for mount_entry in mount_entries:
        log.debug("name:%s, type:%s, status:%s, description:%s" % (
            mount_entry.mapping_name,
            mount_entry.device_type,
            mount_entry.oper_mount_status,
            mnt_state[mount_entry.oper_mount_status],
        ))
    return mount_entries
