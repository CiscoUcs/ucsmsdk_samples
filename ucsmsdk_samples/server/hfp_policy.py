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


def hfp_create(handle, name, blade_bundle_version, rack_bundle_version,
               mode="staged", descr="", parent_dn="org-root"):
    """
    This method creates Host Firmware pack.

    Args:
        handle (UcsHandle)
        name (string): Name of the firmware pack.
        rack_bundle_version (string): Rack bundle version
        blade_bundle_version (string): Blade bundle version
        mode (string): "one-shot" or "staged"
        descr (string): Basic description.
        parent_dn (string): Parent of Org

    Returns:
        FirmwareComputeHostPack: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        hfp_create(handle, name="sample_fp", rack_bundle_version="",
                    blade_bundle_version="")
    """

    from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import\
        FirmwareComputeHostPack

    org = handle.query_dn(parent_dn)
    if not org:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = FirmwareComputeHostPack(parent_mo_or_dn=org.dn,
                                 name=name,
                                 blade_bundle_version=blade_bundle_version,
                                 rack_bundle_version=rack_bundle_version,
                                 mode=mode,
                                 descr=descr
                                 )
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def hfp_modify(handle, name, blade_bundle_version=None,
               rack_bundle_version=None, mode=None, descr=None,
               parent_dn="org-root"):
    """
    This method modify Host Firmware pack.

    Args:
        handle (UcsHandle)
        name (string): Name of the firmware pack.
        rack_bundle_version (string): Rack bundle version
        blade_bundle_version (string): Blade bundle version
        mode (string): "one-shot" or "staged"
        descr (string): Basic description.
        parent_dn (string): Parent of Org

    Returns:
        FirmwareComputeHostPack: Managed Object

    Raises:
        ValueError: If FirmwareComputeHostPack is not present

    Example:
        hfp_modify(handle, name="sample_fp", rack_bundle_version="",
                    blade_bundle_version="")
    """

    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("hfp does not exist.")

    if blade_bundle_version is not None:
        mo.blade_bundle_version = blade_bundle_version
    if rack_bundle_version is not None:
        mo.rack_bundle_version = rack_bundle_version
    if mode is not None:
        mo.mode = mode
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def hfp_remove(handle, name, parent_dn="org-root"):

    """
    This method removes Host Firmware pack.

    Args:
        handle (UcsHandle)
        name (string): Name of the firmware pack.
        parent_dn (string): Parent of Org.

    Returns:
        None

    Raises:
        ValueError: If FirmwareComputeHostPack is not present

    Example:
        hfp_remove(handle, name="sample_fp", parent_dn="org-root/org-sub")
    """

    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("hfp does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def hfp_exists(handle, name, blade_bundle_version, rack_bundle_version,
               mode="staged", descr="", parent_dn="org-root"):
    """
    Checks if the given VLAN already exists with the same params

    Args:
        handle (UcsHandle)
        name (string): Name of the firmware pack.
        rack_bundle_version (string): Rack bundle version
        blade_bundle_version (string): Blade bundle version
        mode (string): "one-shot" or "staged"
        descr (string): Basic description.
        parent_dn (string): Parent of Org

    Returns:
        True/False (Boolean)

    Example:
        hfp_exist(handle, name="sample_fp", rack_bundle_version="",
                    blade_bundle_version="")
    """

    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((blade_bundle_version and
                mo.blade_bundle_version != blade_bundle_version) and
            (rack_bundle_version and
                mo.rack_bundle_version != rack_bundle_version) and
            (mode and mo.mode != mode) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
