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
import os
import time
import datetime
import sys

from ucsmsdk.utils.ccoimage import get_ucs_cco_image_list
from ucsmsdk.utils.ccoimage import get_ucs_cco_image

from ucsmsdk.mometa.top.TopSystem import TopSystem
from ucsmsdk.mometa.firmware.FirmwareCatalogue import FirmwareCatalogue
from ucsmsdk.mometa.firmware.FirmwareDownloader import FirmwareDownloader
from ucsmsdk.mometa.firmware.FirmwareDownloader import FirmwareDownloaderConsts
from ucsmsdk.mometa.firmware.FirmwareAck import FirmwareAckConsts

log = logging.getLogger('ucs')


def firmware_available(username, password, mdf_id_list=None, proxy=None):
    """
    Returns the names of firmware images available on cco

    Args:
        username (string): cec username
        password (string): cec password
        mdf_id_list (list of string): mdf ids
        proxy (string): proxy address

    Returns:
        list

    Example:
        firmware_available(username="cecuser", password="cecpasswd")
    """

    images = get_ucs_cco_image_list(username=username, password=password,
                                    mdf_id_list=mdf_id_list, proxy=proxy)

    image_names = [image.image_name for image in images]
    return sorted(image_names)


def get_firmware_bundles(handle, bundle_type=None):
    """
    Return the list of firmware bundles that have been downloaded on the
    Fabric Interconnect

    Args:
        handle (UcsHandle)
        bundle_type (string): ["b-series-bundle", "c-series-bundle",
                              "catalog", "full-bundle", "image",
                              "infrastructure-bundle", "m-series-bundle",
                              "s-series-bundle", "unknown"]

    Returns:
        list of FirmwareDistributable Managed Objects

    Example:
        get_firmware_bundles(handle, bundle_type="b-series-bundle")
    """

    filter_str = None
    if bundle_type is not None:
        filter_str = '(type, %s, type="eq")' % bundle_type
    bundles = handle.query_classid(
        class_id="FirmwareDistributable", filter_str=filter_str)
    return bundles


def get_blade_firmware_version(handle, bundle_version,
                               image_types=['blade-controller']):
    """
    Return the image firmware versions given the bundle version

    Args:
        handle (UcsHandle)
        bundle_version (string): version
        image_types (list of string)

    Returns:
        dict

    Example:
        get_blade_firmware_version(handle, bundle_version="2.2(6f)")
    """

    bundles = get_firmware_bundles(handle,
                                   bundle_type='b-series-bundle')
    firmware_map = {}
    for image_type in image_types:
        firmware_map[image_type] = {'image_name': None, 'version': None}

    for bundle in bundles:
        log.debug("Bundle type: %s, version: %s. Bundle version: %s",
                  bundle.type, bundle.version, bundle_version)
        if bundle.type == 'b-series-bundle' and \
                bundle.version.startswith(bundle_version):
            dist_images = handle.query_children(in_mo=bundle,
                                                class_id="FirmwareDistImage")
            for dist_image in dist_images:
                # print dist_image
                for image_type in image_types:
                    if dist_image.type == image_type:
                        firmware_map[image_type]['image_name'] = \
                            dist_image.name
                        log.debug('Bundle version %s, infra firmware image '
                                  'name: %s', bundle_version, dist_image.name)
            break

    filter_str = None
    for image_type in image_types:
        if firmware_map[image_type]['image_name'] is None:
            raise Exception("Infra image type '%s' version '%s' is not "
                            "present", image_type, bundle_version)
        else:
            str_ = '(name, %s, type="eq")' % (
                firmware_map[image_type]['image_name'])
            if filter_str is None:
                filter_str = str_
            else:
                filter_str = filter_str + " or " + str_

    firmware_images = handle.query_classid(class_id="FirmwareImage",
                                           filter_str=filter_str)
    for firmware_image in firmware_images:
        for image_type in image_types:
            if firmware_image.name == firmware_map[image_type]['image_name']:
                log.debug("Found bundle/image version mapping. Image type: %s,"
                          " img version: %s, bundle: %s",
                          image_type, firmware_image.version, bundle_version)
                firmware_map[image_type]['version'] = firmware_image.version
    return firmware_map


def get_infra_firmware_version(handle, bundle_version,
                               image_types=['system', 'switch-kernel',
                                            'switch-software']):
    """
    Return the image firmware versions given the bundle version

    Args:
        handle (UcsHandle)
        bundle_version (string): version
        image_types (list of string)

    Returns:
        dict

    Example:
        get_infra_firmware_version(handle, bundle_version="2.2(6f)")
    """

    bundles = get_firmware_bundles(handle, bundle_type='infrastructure-bundle')
    firmware_map = {}
    for image_type in image_types:
        firmware_map[image_type] = {'image_name': None, 'version': None}

    for bundle in bundles:
        log.debug("Bundle type: %s, version: %s. Bundle version: %s",
                  bundle.type, bundle.version, bundle_version)
        if bundle.type == 'infrastructure-bundle' and \
                bundle.version.startswith(bundle_version):
            dist_images = handle.query_children(in_mo=bundle,
                                                class_id="FirmwareDistImage")
            for dist_image in dist_images:
                for image_type in image_types:
                    if dist_image.type == image_type:
                        firmware_map[image_type]['image_name'] = \
                            dist_image.name
                        log.debug('Bundle version %s, infra firmware image '
                                  'name: %s', bundle_version, dist_image.name)
            break

    filter_str = None
    for image_type in image_types:
        if firmware_map[image_type]['image_name'] is None:
            raise Exception("Infra image type '%s' version '%s' is not "
                            "present", image_type, bundle_version)
        else:
            str_ = '(name, %s, type="eq")' % (
                firmware_map[image_type]['image_name'])
            if filter_str is None:
                filter_str = str_
            else:
                filter_str = filter_str + " or " + str_

    firmware_images = handle.query_classid(class_id="FirmwareImage",
                                           filter_str=filter_str)
    for firmware_image in firmware_images:
        for image_type in image_types:
            if firmware_image.name == firmware_map[image_type]['image_name']:
                log.debug("Found bundle/image version mapping. Image type: %s,"
                          " img version: %s, bundle: %s",
                          image_type, firmware_image.version, bundle_version)
                firmware_map[image_type]['version'] = firmware_image.version
    return firmware_map


def has_firmware_bundle(handle, version):
    """
    Returns true if the specified UCS bundle (A, B, C...) is present on the FIs

    Args:
        handle (UcsHandle)
        version (string): version

    Returns:
        True/False(bool)

    Example:
        has_firmware_bundle(handle, bundle_version="1.0.1.0")
    """

    bundles = get_firmware_bundles(handle)
    for bundle in bundles:
        # log.debug("Bundle version %s is available on UCS, want %s",
        #           bundle.version, version)
        if bundle.version == version:
            return True
    return False


def firmware_download(image_name, username, password, download_dir,
                      mdf_id_list=None, proxy=None):
    """
    Downloads the firmware image from cco

    Args:
        image_name (string): firmware image name
        username (string): cec username
        password (string): cec password
        download_dir (string): path of download directory
        mdf_id_list (list of string): mdf ids
        proxy (string): proxy address

    Returns:
        None

    Raises:
        ValueError if firmware image not available on cco

    Example:
        firmware_download(image_name="ucs-k9-bundle-c-series.2.2.5b.C.bin",
                          username="user", password="passwd",
                          download_dir="/home/imagedir")
    """

    images = get_ucs_cco_image_list(username=username, password=password,
                                    mdf_id_list=mdf_id_list, proxy=proxy)

    image_dict = {}
    for image in images:
        image_dict[image.image_name] = image

    if image_name not in image_dict:
        raise ValueError("Image not available")

    # download image
    image = image_dict[image_name]
    get_ucs_cco_image(image, file_dir=download_dir, proxy=proxy)


def firmware_add_local(handle, image_dir, image_name, timeout=10 * 60):
    """
    Downloads the firmware image on ucsm from local server

    Args:
        image_dir (string): path of download directory
        image_name (string): firmware image name
        timeout (number): timeout in seconds

    Returns:
        FirmwareDownloader: Managed Object

    Raises:
        ValueError if download fail or timeout

    Example:
        firmware_add_local(image_dir="/home/imagedir",
                           image_name="ucs-k9-bundle-c-series.2.2.5b.C.bin")
    """

    file_path = os.path.join(image_dir, image_name)

    if not os.path.exists(file_path):
        raise IOError("File does not exist")

    top_system = TopSystem()
    firmware_catalogue = FirmwareCatalogue(parent_mo_or_dn=top_system)
    firmware_downloader = FirmwareDownloader(
        parent_mo_or_dn=firmware_catalogue,
        file_name=image_name)
    firmware_downloader.server = FirmwareDownloaderConsts.PROTOCOL_LOCAL
    firmware_downloader.protocol = FirmwareDownloaderConsts.PROTOCOL_LOCAL
    firmware_downloader.admin_state = \
        FirmwareDownloaderConsts.ADMIN_STATE_RESTART

    uri_suffix = "operations/file-%s/image.txt" % image_name
    handle.file_upload(url_suffix=uri_suffix,
                       file_dir=image_dir,
                       file_name=image_name)

    handle.add_mo(firmware_downloader, modify_present=True)
    # handle.set_dump_xml()
    handle.commit()

    start = datetime.datetime.now()
    while not firmware_downloader.transfer_state == \
            FirmwareDownloaderConsts.TRANSFER_STATE_DOWNLOADED:
        firmware_downloader = handle.query_dn(firmware_downloader.dn)
        if firmware_downloader.transfer_state == \
                FirmwareDownloaderConsts.TRANSFER_STATE_FAILED:
            raise Exception("Download of '%s' failed. Error: %s" %
                            (image_name,
                             firmware_downloader.fsm_rmt_inv_err_descr))
        if (datetime.datetime.now() - start).total_seconds() > timeout:
            raise Exception("Download of '%s' timed out" % image_name)

    return firmware_downloader


def firmware_add_remote(handle, file_name, remote_path, protocol, server,
                        user="", pwd=""):
    """
    Downloads the firmware image on ucsm from remote server

    Args:
        handle (UcsHandle)
        file_name (string): firmware image name
        remote_path (string): path of image directory
        protocol (string): protocol
        server (string): remote server ip address
        user (string): remote server username
        pwd (string): remote server password

    Returns:
        FirmwareDownloader: Managed Object

    Raises:
        ValueError if image not available or incorrect credential

    Example:
        firmware_add_remote(handle,
                            file_name="ucs-k9-bundle-c-series.2.2.5b.C.bin",
                            remote_path="/home/imagedir",
                            protocol="nfs",
                            server="10.65.1.2,
                            user="user", pwd="pwd")
    """

    file_path = os.path.join(remote_path, file_name)

    if not os.path.exists(file_path):
        raise IOError("Image does not exist")

    if protocol is not FirmwareDownloaderConsts.PROTOCOL_TFTP:
        if not user:
            raise ValueError("Provide user")
        if not pwd:
            raise ValueError("Provide pwd")

    top_system = TopSystem()
    firmware_catalogue = FirmwareCatalogue(parent_mo_or_dn=top_system)
    firmware_downloader = FirmwareDownloader(
        parent_mo_or_dn=firmware_catalogue,
        file_name=file_name)
    firmware_downloader.remote_path = remote_path
    firmware_downloader.protocol = protocol
    firmware_downloader.server = server
    firmware_downloader.user = user
    firmware_downloader.pwd = pwd
    firmware_downloader.admin_state = \
        FirmwareDownloaderConsts.ADMIN_STATE_RESTART

    handle.add_mo(firmware_downloader)
    # handle.set_dump_xml()
    handle.commit()
    return firmware_downloader


def firmware_remove(handle, image_name):
    """
    Removes firmware image from  ucsm

    Args:
        handle (UcsHandle)
        image_name (string): firmware image name

    Returns:
        None

    Raises:
        ValueError if image not available on ucsm

    Example:
        firmware_add_remote(handle,
                            file_name="ucs-k9-bundle-c-series.2.2.5b.C.bin")
    """

    top_system = TopSystem()
    firmware_catalogue = FirmwareCatalogue(parent_mo_or_dn=top_system)
    firmware_downloader = FirmwareDownloader(
        parent_mo_or_dn=firmware_catalogue,
        file_name=image_name)

    dn = firmware_downloader.dn
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Image not available on UCSM.")

    handle.remove_mo(mo)
    # handle.set_dump_xml()
    handle.commit()


def validate_connection(handle, timeout=15 * 60):
    """
    Montiors UCSM Connection, if connection exists return True else False

    Args:
        handle (UcsHandle)
        timeout (number): timeout in seconds

    Returns:
        True/False(bool)

    Raises:
        Exception if unable to connect to UCSM

    Example:
        firmware_add_remote(handle,
                            file_name="ucs-k9-bundle-c-series.2.2.5b.C.bin")
    """

    connected = False
    start = datetime.datetime.now()
    while not connected:
        try:
            # If the session is already established,
            # this will validate the session
            connected = handle.login()
        except Exception as e:
            # UCSM may been in the middle of activation,
            # hence connection would fail
            log.debug("Login to UCSM failed: %s", str(e))

        if not connected:
            try:
                log.debug("Login to UCS Manager, elapsed time %ds",
                          (datetime.datetime.now() - start).total_seconds())
                # handle.set_dump_xml()
                handle.login(force=True)
                log.debug("Login successful")
                connected = True
            except:
                log.debug("Login failed. Sleeping for 60 seconds")
                time.sleep(60)
            if (datetime.datetime.now() - start).total_seconds() > timeout:
                raise Exception("TimeOut: Unable to login to UCS Manager")
    return connected


def _get_running_firmware_version(handle, subject="system"):
    """
    Gets Running Firmware version

    Args:
        handle (UcsHandle)
        subject (string): subject

    Returns:
        list of FirmwareRunning Managed Objects

    Raises:
        Exception if unable to connect to UCSM

    Example:
        _get_running_firmware_version(handle)
    """

    running_firmware_list = []
    filter_str_ = '(subject, ' + subject + ', type="eq")'
    mgmt_controllers = handle.query_classid(class_id="MgmtController",
                                            filter_str=filter_str_)

    if len(mgmt_controllers) == 0:
        raise Exception("No Mgmt Controller Object with subject %s", subject)

    for mgmt_controller in mgmt_controllers:
        list_ = handle.query_children(in_mo=mgmt_controller,
                                      class_id="FirmwareRunning")
        if len(list_) == 0:
            raise Exception("No FirmwareRunning Object with subject %s",
                            subject)
        for running_firmware in list_:
            running_firmware_list.append(running_firmware)

    return running_firmware_list


def wait_for_firmware_activation(handle, bundle_version,
                                 subject,
                                 image_types,
                                 wait_for_upgrade_completion,
                                 acknowledge_reboot,
                                 timeout,
                                 observer=None):
    """
    Returns True if firmware is already running at the specified version
    If not running at the desired version, optionally wait until activation
    has completed and UCS came back online.

    Args:
        handle (UcsHandle)
        bundle_version(string): version
        subject (string): subject
        image_types (list): image types
        wait_for_upgrade_completion (bool): True/False
        acknowledge_reboot (bool): True/False
        timeout (number): timeout in seconds
        observer (string): observer

    Returns:
        True/False(bool)

    Raises:
        Exception if running version not available ot ucsm is not running at
        desired version

    Example:
        wait_for_firmware_activation(handle,
                                    version="1.0.1.0", subject="system",
                                    image_types=['system'],
                                    wait_for_upgrade_completion=True,
                                    acknowledge_reboot=False,
                                    timeout=600)
    """

    is_running_desired_version = False
    start = datetime.datetime.now()
    while not is_running_desired_version:
        validate_connection(handle, timeout)

        try:
            is_running_desired_version = True
            running_firmware_list = _get_running_firmware_version(handle,
                                                                  subject)

            firmware_map = get_infra_firmware_version(handle, bundle_version)

            for image_type in image_types:
                found_image_type_match = False
                for running_firmware in running_firmware_list:
                    if running_firmware.type == image_type:
                        found_image_type_match = True
                        expected_version = firmware_map[image_type]['version']
                        log.debug("UCS %s is running version %s, expected: %s,"
                                  " bundle: %s",
                                  running_firmware.dn,
                                  running_firmware.version,
                                  expected_version, bundle_version)
                        if running_firmware.version != expected_version:
                            is_running_desired_version = False
                if not found_image_type_match:
                    raise Exception("No FirmwareRunning object of type %s",
                                    image_type)

            if not is_running_desired_version:
                if not wait_for_upgrade_completion:
                    log.debug("UCS %s is not running at desired version",
                              subject)
                    break
                else:
                    log.debug("UCS %s is not running at desired version. "
                              "Waiting for activation completion", subject)
                    # if observer: observer.fw_observer_cb("UCS %s is not
                    # running at desired version. Waiting for activation
                    # completion", subject)
                    time.sleep(60)

                    # Check if there is a pending switch reboot
                    firmware_ack = handle.query_dn('sys/fw-system/ack')
                    log.debug("Firmware ack: oper_state: %s, scheduler:%s",
                              firmware_ack.oper_state, firmware_ack.scheduler)
                    if firmware_ack.oper_state == 'waiting-for-user' and \
                            acknowledge_reboot:
                        log.debug("Acknowledging switch reboot")
                        if observer:
                            observer.fw_observer_cb('Acknowledging UCS '
                                                    'primary Fabric '
                                                    'Interconnect reboot')
                        firmware_ack.adminState = \
                            FirmwareAckConsts.ADMIN_STATE_TRIGGER_IMMEDIATE
                        handle.set_mo(firmware_ack)
                        handle.commit()
        except Exception:
            # Login session may become invalid during upgrade because UCSM will
            # restart, or FIs will reboot.
            log.exception("Script lost connectivity to UCSM during upgrade. "
                          "This is expected")
            time.sleep(30)

        if (datetime.datetime.now() - start).total_seconds() > timeout:
            log.warning("UCS %s activation timeout. Elapsed time: %ds",
                        subject,
                        (datetime.datetime.now() - start).total_seconds())
            break

    return is_running_desired_version


def wait_for_ucsm_activation(handle, version,
                             wait_for_upgrade_completion=True,
                             timeout=20 * 60):
    """
    Returns True if UCSM is already running at the specified version.
    If not running at the desired version, optionally wait until activation
    has completed and UCS came back online.
    """

    log.debug("Wait for UCSM firmware activation")
    return wait_for_firmware_activation(
        handle, version, subject="system",
        image_types=['system'],
        wait_for_upgrade_completion=wait_for_upgrade_completion,
        acknowledge_reboot=False,
        timeout=timeout)


def wait_for_fi_activation(handle, version,
                           wait_for_upgrade_completion=True,
                           timeout=60 * 60,
                           observer=None):
    """
    Returns True if the FIs are already running at the specified version
    """

    log.debug("Wait for FI firmware activation")
    return wait_for_firmware_activation(
        handle, version, subject="switch",
        image_types=['switch-software', 'switch-kernel'],
        wait_for_upgrade_completion=wait_for_upgrade_completion,
        acknowledge_reboot=True,
        timeout=timeout,
        observer=observer)


def firmware_activate_infra(handle, version="2.2(2c)",
                            require_user_confirmation=True, observer=None):
    """
    Activate Infra bundle on UCSM

    Args:
        handle (UcsHandle)
        version: version
        require_user_confirmation (bool): True/False
        observer (Thread): observer

    Returns:
        None

    Raises:
        Exception if FI bundle is not available

    Example:
        firmware_activate_infra(handle)
    """

    infra_bundle_version = version + "A"
    bundle_available = has_firmware_bundle(handle,
                                           version=infra_bundle_version)
    if not bundle_available:
        raise Exception("Bundle %s is not available on Fabric Interconnect",
                        infra_bundle_version)

    if observer:
        observer.fw_observer_cb('Querying UCS Manager version')

    ucsm_has_desired_version = wait_for_ucsm_activation(
        handle, version, wait_for_upgrade_completion=False)

    if observer:
        observer.fw_observer_cb('Querying UCS switch firmware version')

    fis_have_desired_version = wait_for_fi_activation(
        handle, version, wait_for_upgrade_completion=False)

    need_activation = not ucsm_has_desired_version or not \
        fis_have_desired_version
    if not need_activation:
        log.debug("No infra firmware activation required")
        return
    if require_user_confirmation:
        set_flag = False
        set_str = input("Are you sure want to proceed? This will reboot "
                            "theFabric Interconnects. Enter 'yes' to proceed.")
        if set_str.strip().lower() == "yes":
            set_flag = True

        if not set_flag:
            log.debug("Abort activate firmware version.")
            return

    firmware_infra_pack = handle.query_classid(class_id="FirmwareInfraPack")[0]
    # connected = True
    if firmware_infra_pack.infra_bundle_version != infra_bundle_version:
        firmware_infra_pack.infra_bundle_version = infra_bundle_version

        handle.set_mo(firmware_infra_pack)
        handle.commit()
        if not ucsm_has_desired_version:
            handle.logout()

    if observer:
        observer.fw_observer_cb('Activating UCS Manager version %s', version)

    ucsm_has_desired_version = wait_for_ucsm_activation(
        handle, version, wait_for_upgrade_completion=True)

    if ucsm_has_desired_version:
        log.debug("UCS Manager successfully updated to version '%s'" % version)
    else:
        log.debug("UCS Manager not updated to version '%s'" % version)
        raise Exception("UCS Manager not updated to version %s", version)

    if observer:
        observer.fw_observer_cb('Activating UCS switch firmware version %s',
                                version)

    wait_for_fi_activation(
        handle, version, wait_for_upgrade_completion=True, observer=observer)


def _get_blade_firmware_running(handle, blade):
    """
    Gets Running Firmware version

    Args:
        handle (UcsHandle)
        blade (ComputeBlade): ManagedObject

    Returns:
        FirmwareRunning: Managed Objects

    Raises:
        None

    Example:
        _get_blade_firmware_running(handle, blade)
    """

    mgmt_controllers = handle.query_children(in_mo=blade,
                                             class_id="MgmtController")

    for mgmt_controller in mgmt_controllers:
        if mgmt_controller.subject == "blade":
            firmware_runnings_ = handle.query_children(
                in_mo=mgmt_controller, class_id="FirmwareRunning")

    firmware_runnings = []
    for firmware_running_ in firmware_runnings_:
        if firmware_running_.deployment == "system":
            firmware_runnings.append(firmware_running_)

    if not firmware_runnings or len(firmware_runnings) != 1:
        log.debug("Improper firmware running")
        return None

    firmware_running = firmware_runnings[0]
    # version = firmware_running.version
    # log.debug("Blade ('%s') running at version '%s'" % (blade.dn, version))
    return firmware_running


def wait_for_blade_activation(handle,
                              bundle_version,
                              firmware_running_map,
                              require_user_confirmation=True,
                              timeout=15 * 60):
    """
    Returns True if firmware is already running at the specified version
    If not running at the desired version, optionally wait until activation.

    Args:
        handle (UcsHandle)
        bundle_version(string): version
        firmware_running_map (dict): {'blade_dn' :
                                        'FirmwareRunning ManagedObject'}
        timeout (number): timeout in seconds


    Returns:
        True/False(bool)

    Raises:
        Exception if running version not available ot ucsm is not running at
        desired version

    Example:
        wait_for_firmware_activation(handle,
                                    version="1.0.1.0", subject="system",
                                    image_types=['system'],
                                    wait_for_upgrade_completion=True,
                                    acknowledge_reboot=False,
                                    timeout=600)
    """

    firmware_running_state = {}
    is_running_desired_version = False
    start = datetime.datetime.now()
    while not is_running_desired_version:
        log.debug("sleeping for 60 seconds.")
        time.sleep(60)
        try:
            is_running_desired_version = True
            for blade in sorted(firmware_running_map):
                firmware_running = firmware_running_map[blade][0]

                if firmware_running.version == bundle_version:
                    firmware_running_state[firmware_running.dn] = True

                if firmware_running.dn in firmware_running_state and \
                        firmware_running_state[firmware_running.dn]:
                    log.debug("Blade '%s' is running at version '%s': "
                              "Expected '%s'"
                              % (blade, firmware_running.version,
                                 bundle_version))
                    continue

                firmware_running = handle.query_dn(firmware_running.dn)
                log.debug("Blade '%s' is running at version '%s': Expected "
                          "'%s'"
                          % (blade, firmware_running.version,
                             bundle_version))
                if firmware_running.version != bundle_version:
                    is_running_desired_version = False

                    if require_user_confirmation:
                        set_flag = False
                        set_str = input("The update process will need to "
                                            "reboot the server(s). "
                                            "Would you like to acknowledge "
                                            "the same?"
                                            "Enter 'yes' to proceed.")
                        if set_str.strip().lower() == "yes":
                            set_flag = True

                        if not set_flag:
                            log.warning("Acknowledgement is required to "
                                        "update blade server.")
                            continue

                    sp_dn = firmware_running_map[blade][1]
                    dn = sp_dn + '/ack'
                    ls_maint_ack = handle.query_dn(dn)
                    if ls_maint_ack:
                        if ls_maint_ack.oper_state == "waiting-for-user":
                            if ls_maint_ack.admin_state == 'trigger-immediate':
                                ls_maint_ack.admin_state = 'untriggered'
                                handle.set_mo(ls_maint_ack)
                                handle.commit()
                                log.debug("Re-Acknowledging blade '%s' with "
                                          "service profile '%s'." % (blade,
                                                                     sp_dn))
                                time.sleep(5)

                            ls_maint_ack.admin_state = 'trigger-immediate'
                            handle.set_mo(ls_maint_ack)
                            handle.commit()
                            log.debug("Acknowledging blade '%s' with service "
                                      "profile '%s'." % (blade, sp_dn))

                    continue

                firmware_running_map[blade][0] = firmware_running
        except Exception as e:
            log.exception(e.message)
            log.debug("sleeping for 30 seconds")
            time.sleep(30)
        if (datetime.datetime.now() - start).total_seconds() > timeout:
            log.warning("Blade activation timeout. Elapsed time: %ds",
                        (datetime.datetime.now() - start).total_seconds())
            is_running_desired_version = False
            break

    return is_running_desired_version


def firmware_activate_blade(handle, version, require_user_confirmation=True):
    """
    Activate blade bundle on UCSM

    Args:
        handle (UcsHandle)
        version: version
        require_user_confirmation (bool): by default True. If False needs no
                                          user intervention.

    Returns:
        None

    Example:
        firmware_activate_blade(handle, version="2.2.5b")
    """

    blade_bundle = version + "B"
    # rack_bundle = version + "C"

    host_firmware_packs = []
    firmware_running_map = {}

    blades_ = handle.query_classid("ComputeBlade")
    blades = sorted(blades_, key=lambda blade_: blade_.dn)
    for blade in blades:
        blade_dn = blade.dn
        firmware_running = _get_blade_firmware_running(handle, blade)
        if not firmware_running:
            log.debug("Improper firmware on blade '%s'" % blade_dn)
            continue
        firmware_running_map[blade_dn] = [firmware_running,
                                          blade.assigned_to_dn]
        if firmware_running.version == version:
            log.debug("Blade ('%s') running software version already at "
                      "version: '%s'" % (blade_dn, version))
            continue
        else:
            log.debug("Blade ('%s') is running at version '%s': Expected '%s'"
                      % (blade_dn, firmware_running.version, version))
            assigned_to_dn = blade.assigned_to_dn
            if not assigned_to_dn:
                host_firmware_pack_dn = "org-root/fw-host-pack-default"
            else:
                # sp_name = re.search(r'^ls-(?P<sp_name>\w+)$',
                # os.path.basename(assigned_to_dn)).groupdict()['sp_name']
                sp = handle.query_dn(assigned_to_dn)
                host_firmware_pack_dn = sp.oper_host_fw_policy_name

            if host_firmware_pack_dn in host_firmware_packs:
                continue

            host_firmware_pack = handle.query_dn(host_firmware_pack_dn)
            host_firmware_pack.blade_bundle_version = blade_bundle

            if require_user_confirmation:
                set_flag = False
                set_str = input("Are you sure want to proceed? This will "
                                    "reboot the server."
                                    "Enter 'yes' to proceed.")
                if set_str.strip().lower() == "yes":
                    set_flag = True

                if not set_flag:
                    log.debug("Abort update blade firmware.")
                    return None

            handle.set_mo(host_firmware_pack)
            handle.commit()

            if require_user_confirmation:
                set_flag = False
                set_str = input("The update process will need to reboot "
                                    "the server(s). Would you like to "
                                    "acknowledge the same?"
                                    "Enter 'yes' to proceed.")
                if set_str.strip().lower() == "yes":
                    set_flag = True

                if not set_flag:
                    log.debug("Acknowledgement is required to update blade "
                              "server.")
                    sys.exit()

            sps = handle.query_classid(class_id="LsServer")
            for sp in sps:
                if sp.type == 'instance' and sp.assoc_state == 'associated':
                    if sp.oper_host_fw_policy_name and \
                            sp.oper_host_fw_policy_name == \
                            host_firmware_pack_dn:
                        dn = sp.dn + '/ack'
                        ls_maint_ack = handle.query_dn(dn)
                        if ls_maint_ack:
                            ls_maint_ack.admin_state = 'trigger-immediate'
                            handle.set_mo(ls_maint_ack)
                            handle.commit()
                            log.debug("Acknowledging blade '%s', service "
                                      "profile '%s' using hostfirmwarepack "
                                      "'%s'." % (sp.pn_dn, sp.dn,
                                                 sp.oper_host_fw_policy_name))

            host_firmware_packs.append(host_firmware_pack_dn)
    status = False
    if firmware_running_map:
        log.debug("Waiting for blade activation")
        status = wait_for_blade_activation(handle,
                                           version,
                                           firmware_running_map,
                                           require_user_confirmation,
                                           timeout=15 * 60)
    return status


def get_firmware_file_names(version, extension="bin"):
    """
    create version string
    """

    ver_split = version.split('(')
    version_bundle = ver_split[0] + "." + ver_split[1].strip(')')

    # create firmware file name for the respective version
    aseries_bundle = "ucs-k9-bundle-infra." + version_bundle + ".A." + \
                     extension
    bseries_bundle = "ucs-k9-bundle-b-series." + version_bundle + ".B." + \
                     extension
    cseries_bundle = "ucs-k9-bundle-c-series." + version_bundle + ".C." + \
                     extension

    return {"A": (aseries_bundle, version + "A"),
            "B": (bseries_bundle, version + "B"),
            "C": (cseries_bundle, version + "C"),
            }


def is_image_available_on_ucsm(handle, image):
    """
    Check if image available on UCSM

    Args:
        handle (UcsHandle)
        image (string): image name

    Returns:
        True/False(boolean)

    Example:
        is_image_available_on_ucsm(handle,
                                   image="ucs-k9-bundle-infra.2.2.3f.A.bin")
    """

    log.debug("Checking if image file: '%s' is already uploaded to UCS"
              " Domain" % image)

    deleted = False
    filter_str = '(name, %s, type="eq")' % image
    firmware_package = handle.query_classid(
        class_id="FirmwareDistributable", filter_str=filter_str)
    if firmware_package:
        firmware_dist_image = handle.query_children(
            in_mo=firmware_package[0], class_id="FirmwareDistImage")
        if firmware_dist_image:
            firmware_dist_image = firmware_dist_image[0]
            if firmware_dist_image.image_deleted != "":
                deleted = True

    if deleted or not firmware_package:
        log.debug("Image file '%s' is not available on UCSM" % image)
        return False
    else:
        log.debug("Image file '%s' is available on UCSM" % image)
        return True


def firmware_auto_install(handle, version, image_dir, infra_only=False,
                          infra=True, blade=True, rack=False,
                          require_user_confirmation=True):
    """
    This will do end-to-end processing to update firmware on ucsm.

    Args:
        handle (UcsHandle)
        version (string): firmware version
        image_dir (string): image directory
        infra_only (bool): by default False. If set to True, will update
                          firmware of FI only
        require_user_confirmation (bool): by default True. If False needs no
                                          user intervention.

    Returns:
        None

    Example:
        firmware_auto_install(handle, version="2.2.5b",
                              image_dir="/home/imagedir")
    """

    from ucsmsdk.ucseventhandler import UcsEventHandle

    try:
        bundle_map = get_firmware_file_names(version)

        bundles = []
        cco_image_list = []
        images_to_upload = []

        if infra_only:
            bundles.append(bundle_map['A'][0])
        else:
            if infra:
                bundles.append(bundle_map['A'][0])
            if blade:
                bundles.append(bundle_map['B'][0])
            if rack:
                bundles.append(bundle_map['C'][0])

        for image in bundles:
            if not is_image_available_on_ucsm(handle, image):
                images_to_upload.append(image)

        for image in images_to_upload:
            log.debug("Checking if image file: '%s' is exist in local "
                      "directory" % image)
            file_path = os.path.join(image_dir, image)
            if os.path.exists(file_path):
                log.debug("Image already exist in image directory ")
            else:
                cco_image_list.append(image)

        # if image not available raising exception to download
        if cco_image_list:
            raise ValueError("Download images %s using firmware_download" %
                             cco_image_list)

        # upload images on ucsm
        for image in images_to_upload:
            log.debug("Uploading image '%s' to UCSM." % image)
            firmware = firmware_add_local(handle, image_dir, image)
            eh = UcsEventHandle(handle)
            eh.add(managed_object=firmware, prop="transfer_state",
                   success_value=['downloaded'], poll_sec=30,
                   timeout_sec=600)
            log.debug("Upload of image file '%s' is completed." % image)

        if infra_only:
            # Activate UCSM
            firmware_activate_infra(
                handle, version=version,
                require_user_confirmation=require_user_confirmation)
        else:
            if infra:
                # Activate UCSM
                log.debug("Activating Firmware Infra......")
                firmware_activate_infra(
                    handle, version=version,
                    require_user_confirmation=require_user_confirmation)
            if blade:
                # Activate Blade
                log.debug("Activating Firmware Blade......")
                firmware_activate_blade(
                    handle, version=version,
                    require_user_confirmation=require_user_confirmation)
            if rack:
                # Activate Blade
                log.debug("firmware upgrade code for rack is yet to be done.")
                # firmware_activate_blade(
                #     handle, version=version,
                #     require_user_confirmation=require_user_confirmation)

    except:
        log.debug("Error Occurred in Script.")
        handle.logout()
        raise
