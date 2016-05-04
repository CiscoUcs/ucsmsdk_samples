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


def hfp_create(handle, org_dn, name,
               blade_bundle_version="",
               rack_bundle_version="",
               ignore_comp_check="yes",
               update_trigger="immediate",
               mode="staged",
               stage_size="0",
               policy_owner="local",
               descr="testdescr"):
    """
    Creates a HostFirmwarePack Policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the org in which policy is required
        name (string) : name of the policy
        blade_bundle_version (string): blade version
        rack_bundle_version (string): rack version
        ignore_comp_check (string): "yes", "no"
        update_trigger (string): "immediate"
        mode (string): "one-shot", "staged"
        stage_size (number): stage_size
        policy_owner (string): "local", "global". Default is local
        descr (string): description of the policy

    Returns:
        FirmwareComputeHostPack: Managed object

    Raises:
        ValueError: If OrgOrg does not exist

    Example:
        hfp_create(handle, name="sample_fp", rack_bundle_version="",
                    blade_bundle_version="", org_dn="org-root")
    """

    from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import \
        FirmwareComputeHostPack

    org = handle.query_dn(org_dn)
    if org is None:
        raise ValueError("Org '%s' does not exist" % org_dn)

    mo = FirmwareComputeHostPack(parent_mo_or_dn=org,
                                 name=name,
                                 blade_bundle_version=blade_bundle_version,
                                 rack_bundle_version=rack_bundle_version,
                                 ignore_comp_check=ignore_comp_check,
                                 update_trigger=update_trigger,
                                 mode=mode,
                                 stage_size=stage_size,
                                 policy_owner=policy_owner,
                                 descr=descr)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def hfp_modify(handle, org_dn, name, blade_bundle_version=None,
               rack_bundle_version=None, ignore_comp_check=None,
               update_trigger=None, mode=None, stage_size=None,
               policy_owner=None, descr=None):
    """
    Modify a HostFirmwarePack Policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the org in which policy is required
        name (string) : name of the policy
        blade_bundle_version (string): blade version
        rack_bundle_version (string): rack version
        ignore_comp_check (string): "yes", "no"
        update_trigger (string): "immediate"
        mode (string): "one-shot", "staged"
        stage_size (number): stage_size
        policy_owner (string): "local", "global". Default is local
        descr (string): description of the policy

    Returns:
        FirmwareComputeHostPack: Managed object

    Raises:
        ValueError: If FirmwareComputeHostPack does not exist

    Example:
        hfp_modify(handle, name="sample_fp", rack_bundle_version="",
                    blade_bundle_version="", org_dn="org-root")
    """

    dn = org_dn + "fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("HFP '%s' does not exist" % dn)

    if blade_bundle_version is not None:
        mo.blade_bundle_version = blade_bundle_version
    if rack_bundle_version is not None:
        mo.rack_bundle_version = rack_bundle_version
    if ignore_comp_check is not None:
        mo.ignore_comp_check = ignore_comp_check
    if update_trigger is not None:
        mo.update_trigger = update_trigger
    if mode is not None:
        mo.mode = mode
    if stage_size is not None:
        mo.stage_size = stage_size
    if policy_owner is not None:
        mo.policy_owner = policy_owner
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def hfp_delete(handle, org_dn, name):
    """
    Deletes the specified host firmware pack policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the vmedia policy
        name (string) : name of the policy to delete

    Returns:
        None

    Raises:
        ValueError: if  FirmwareComputeHostPack does not exist

    Example:
        hfp_delete(handle, name="sample_fp", org_dn="org-root/org-sub")
    """

    dn = org_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("HFP '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def hfp_firmware_pack_item_add(handle, org_dn, hfp_name, hw_vendor, hw_model,
                               type, version):
    """
    Adds a FirmwarePackItem to HostFirmwarePack Policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the org in which policy is required
        hfp_name (string) : name of the host firmware pack policy
        hw_vendor (string): hw_vendor
        hw_model (string): hw_model
        type (string): type
        version (string): version

    Returns:
        FirmwarePackItem: Managed object

    Raises:
        ValueError: If FirmwareComputeHostPack not exist

    Example:
        hfp_firmware_pack_item_add(handle, org_dn="org-root",
                                   hfp_name="testhfp", hw_vendor="test",
                                   hw_model="model", type="adaptor",
                                   version="1.0.0.1")
    """

    from ucsmsdk.mometa.firmware.FirmwarePackItem import FirmwarePackItem

    dn = org_dn + "/fw-host-pack-" + hfp_name
    obj = handle.query_dn(dn)
    if obj is None:
        raise ValueError("HFP '%s' does not exist" % dn)

    mo = FirmwarePackItem(parent_mo_or_dn=obj,
                          hw_vendor=hw_vendor,
                          hw_model=hw_model,
                          type=type,
                          version=version)
    handle.add_mo(mo)
    handle.commit()
    return mo


def hfp_firmware_pack_item_remove(handle, org_dn, hfp_name, hw_vendor,
                                  hw_model, type):
    """
    Removes a FirmwarePackItem from HostFirmwarePack Policy

    Args:
        handle (UcsHandle)
        org_dn (string): the dn of the org in which policy is required
        hfp_name (string) : name of the host firmware pack policy
        hw_vendor (string): hw_vendor
        hw_model (string): hw_model
        type (string): type

    Returns:
        None

    Raises:
        ValueError: If FirmwarePackItem not exist

    Example:
        hfp_firmware_pack_item_add(handle, org_dn="org-root",
                                   hfp_name="testhfp", hw_vendor="test",
                                   hw_model="model", type="adaptor")
    """

    hfp_dn = org_dn + "/fw-host-pack-" + hfp_name
    dn = hfp_dn + "/pack-image-" + hw_vendor + "|" + hw_model + "|" + type
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("FirmwarePackItem '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def hfp_sp_attach(handle, sp_dn, hfp_name):
    """
    Attaches a hfp policy to the specified service profile

    Args:
        handle (UcsHandle)
        sp_dn (string): the dn of the service profile to attach to
        hfp_name (string) : name of the host firmware pack policy

    Returns:
        LsServer: Managed object

    Raises:
        ValueError: if host firmware pack policy does not exist

    Example:
        mo = hfp_sp_attach(handle=handle, sp_dn="org-root/ls-demo_sp",
                                    hfp_name="demo-policy")
    """

    import os

    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("sp does not exist.")

    obj = None
    org_dn = os.path.dirname(sp.dn)
    while obj is None:
        dn = org_dn + "/fw-host-pack-" + hfp_name
        obj = handle.query_dn(dn)
        if obj:
            break
        elif obj is None and org_dn == 'org-root':
            raise ValueError("host firmware pack policy does not exist.")
        org_dn = os.path.dirname(org_dn)

    sp.host_fw_policy_name = hfp_name
    handle.set_mo(sp)
    handle.commit()
    return sp


def hfp_sp_detach(handle, sp_dn):
    """
    Detaches hfp policy from the specified service profile

    Args:
        handle (UcsHandle)
        sp_dn (string): the dn of the service profile to detach from

    Returns:
        LsServer: Managed object

    Raises:
        ValueError: if service profile does not exist

    Example:
        mo = hfp_sp_detach(handle=handle, sp_dn="org-root/ls-demo_sp")
    """

    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("sp does not exist.")

    sp.host_fw_policy_name = ""
    handle.set_mo(sp)
    handle.commit()
    return sp
