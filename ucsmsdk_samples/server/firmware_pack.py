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


def firmware_pack_create(handle, org_name, name, rack_bundle_version,
                         blade_bundle_version, descr="", mode="staged",
                         org_parent="org-root"):
    """
    This method creates Host Firmware pack.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the firmware pack.
        rack_bundle_version (string): Rack bundle version
        blade_bundle_version (string): Blade bundle version
        mode (string): "one-sot" or "staged"
        descr (string): Basic description.
        org_parent (string): Parent of Org

    Returns:
        None

    Example:
        firmware_pack_create(handle, org_name="sample_org",
                                name="sample_fp",
                                rack_bundle_version="",
                                blade_bundle_version="")
    """

    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" % org_name)
    else:
        from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import\
            FirmwareComputeHostPack

        mo = FirmwareComputeHostPack(parent_mo_or_dn=org_dn,
                                     name=name,
                                     descr=descr,
                                     rack_bundle_version=rack_bundle_version,
                                     mode=mode,
                                     blade_bundle_version=blade_bundle_version)
        handle.add_mo(mo)
        handle.commit()


def firmware_pack_modify(handle, org_name, name, rack_bundle_version=None,
                         blade_bundle_version=None, descr=None, mode=None,
                         org_parent="org-root"):
    """
    This method creates Host Firmware pack.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the firmware pack.
        rack_bundle_version (string): Rack bundle version
        blade_bundle_version (string): Blade bundle version
        mode (string): "one-sot" or "staged"
        descr (string): Basic description.
        org_parent (string): Parent of Org

    Returns:
        None

    Example:
        firmware_pack_modify(handle, org_name="sample_org",
                                name="sample_fp",
                                rack_bundle_version="",
                                blade_bundle_version="")
    """

    org_dn = org_parent + "/org-" + org_name
    fw_dn= org_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(fw_dn)
    if mo is not None:
        if rack_bundle_version is not None:
            mo.rack_bundle_version = rack_bundle_version
        if blade_bundle_version is not None:
            mo.blade_bundle_version =  blade_bundle_version
        if mode is not None:
            mo.mode=mode
        if descr is not None:
            mo.descr = descr

        handle.set_mo(mo)
        handle.commit()
    else:
        log.info("Firmware host pack <%s> not found." % name)


def firmware_pack_remove(handle, org_name, name, org_parent="org-root"):

    """
    This method removes Host Firmware pack.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the firmware pack.
        org_parent (string): Parent of Org.

    Returns:
        None

    Example:
        firmware_pack_remove(handle, org_name="sample_org",
                                name="sample_fp")
    """
    org_dn = org_parent + "/org-" + org_name
    p_mo = handle.query_dn(org_dn)
    if not p_mo:
        log.info("Sub-Org <%s> not found!" %org_name)
    else:
        fw_dn= org_dn + "/fw-host-pack-" + name
        mo = handle.query_dn(fw_dn)
        if not mo:
            log.info("Firmware host pack <%s> not found.Nothing to remove" % name)
        else:
            handle.remove_mo(mo)
            handle.commit()
