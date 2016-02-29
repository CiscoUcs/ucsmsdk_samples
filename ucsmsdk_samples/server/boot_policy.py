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


from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import \
    LsbootDefaultLocalImage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.lsboot.LsbootUsbFlashStorageImage import \
    LsbootUsbFlashStorageImage
from ucsmsdk.mometa.lsboot.LsbootUsbInternalImage import LsbootUsbInternalImage
from ucsmsdk.mometa.lsboot.LsbootUsbExternalImage import LsbootUsbExternalImage


def boot_policy_create(handle, name, descr="",
                       reboot_on_update="yes",
                       enforce_vnic_name="yes",
                       boot_mode="legacy",
                       parent_dn="org-root", boot_device={}):
    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        parent_dn (string): Org DN.
        descr (string): Basic description.
        boot_device (dict): Dictionary of boot devices. {"1":"cdrom-local"}

    Returns:
        LsbootPolicy: Managed Object

    Example:
        boot_policy_create(handle, name="sample_boot",
                            reboot_on_update="yes",
                            boot_mode="legacy",
                            parent_dn="org-root/org-finance",
                            boot_device={"2":"cdrom-local","1":"usb-external",
                            "3":"usb-internal"})
    """

    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

    mo = handle.query_dn(parent_dn)
    if mo is None:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = LsbootPolicy(parent_mo_or_dn=mo,
                      name=name, descr=descr,
                      reboot_on_update=reboot_on_update,
                      enforce_vnic_name=enforce_vnic_name,
                      boot_mode=boot_mode)
    if boot_device is not None:
        _add_device(handle, mo, boot_device)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def boot_policy_modify(handle, name, descr=None,
                       reboot_on_update=None,
                       enforce_vnic_name=None,
                       boot_mode=None,
                       parent_dn="org-root"):
    """
    This method modifies boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        descr (string): Basic description.
        parent_dn (string): Parent of Org.

    Returns:
        LsbootPolicy: Managed Object

    Raises:
        ValueError: If LsbootPolicy is not present

    Example:
        boot_policy_modify(handle, name="sample_boot",
                                reboot_on_update="yes",
                                boot_mode="legacy",
                                parent_dn="org-root/org-test")
    """

    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("boot policy '%s' does not exist" % dn)

    if descr is not None:
        mo.descr = descr
    if reboot_on_update is not None:
        mo.reboot_on_update = reboot_on_update
    if enforce_vnic_name is not None:
        mo.enforce_vnic_name = enforce_vnic_name
    if boot_mode is not None:
        mo.boot_mode = boot_mode

    handle.set_mo()
    handle.commit()
    return mo


def boot_policy_remove(handle, name, parent_dn="org-root"):
    """
    This method removes boot policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the boot policy.
        parent_dn (string): Parent of Org

    Returns:
        None

    Raises:
        ValueError: If LsbootPolicy is not present

    Example:
        boot_policy_remove(handle, name="sample_boot",
                            parent_dn="org-root/org-test")
    """

    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("boot policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def boot_policy_exist(handle, name, reboot_on_update="yes",
                      enforce_vnic_name="yes", boot_mode="legacy", descr="",
                      parent_dn="org-root"):
    """
    checks if boot policy exist

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        parent_dn (string): Org DN.
        descr (string): Basic description.

    Returns:
        True/False: Boolean

    Example:
        boot_policy_exist(handle,
                        name="sample_boot",
                        reboot_on_update="yes",
                        boot_mode="legacy",
                        parent_dn="org-root/org-finance")
    """

    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((boot_mode and mo.boot_mode != boot_mode)
            and
            (reboot_on_update and mo.reboot_on_update != reboot_on_update)
            and
            (enforce_vnic_name and
                     mo.enforce_vnic_name != enforce_vnic_name)and
            (descr and mo.descr != descr)):
            return False
        return True
    return False


def _add_device(handle, parent_mo, boot_device):
    count = 0
    children = handle.query_children(parent_mo)
    for child in children:
        if hasattr(child, 'order'):
            order = getattr(child, 'order')
            if order not in boot_device:
                log.debug("Deleting boot device from boot policy: %s",
                          child.dn)
                handle.remove_mo(child)
                
    for k in boot_device.keys():
        log.debug("Add boot device: order=%s, %s", k, boot_device[k])
        if boot_device[k] in ["cdrom-local", "cdrom"]:
            _add_cdrom_local(parent_mo, k)
        elif boot_device[k] == "cdrom-cimc":
            _add_cdrom_cimc(parent_mo, k)
        elif boot_device[k] == "cdrom-remote":
            _add_cdrom_remote(parent_mo, k)
        elif boot_device[k] in ["lun", "local-disk", "sd-card", "usb-internal",
                                "usb-external"]:
            if count == 0:
                mo = LsbootStorage(parent_mo_or_dn=parent_mo, order=k)
                mo_1 = LsbootLocalStorage(parent_mo_or_dn=mo)
                count += 1
            if boot_device[k] == "lun":
                _add_local_lun(mo_1, k)
            elif boot_device[k] == "local-disk":
                _add_local_disk(mo_1, k)
            elif boot_device[k] == "sd-card":
                _add_sd_card(mo_1, k)
            elif boot_device[k] == "usb-internal":
                _add_usb_internal(mo_1, k)
            elif boot_device[k] == "usb-external":
                _add_usb_external(mo_1, k)
        elif boot_device[k] in ["floppy", "floppy-local"]:
            _add_floppy_local(parent_mo, k)
        elif boot_device[k] == "floppy-external":
            _add_floppy_remote(parent_mo, k)
        elif boot_device[k] == "virtual-drive":
            _add_virtual_drive(parent_mo, k)
        else:
            log.debug("Option <%s> not recognized." % boot_device[k])


def _add_cdrom_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-local",
                       order=order)


def _add_cdrom_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-remote",
                       order=order)


def _add_cdrom_cimc(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-remote-cimc",
                       order=order)


def _add_floppy_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-write-local",
                       order=order)


def _add_floppy_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-remote",
                       order=order)


def _add_virtual_drive(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-drive",
                       order=order)


def _add_local_disk(parent_mo, order):
    LsbootDefaultLocalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_local_lun(parent_mo, order):
    LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)


def _add_sd_card(parent_mo, order):
    LsbootUsbFlashStorageImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_internal(parent_mo, order):
    LsbootUsbInternalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_external(parent_mo, order):
    LsbootUsbExternalImage(parent_mo_or_dn=parent_mo, order=order)
