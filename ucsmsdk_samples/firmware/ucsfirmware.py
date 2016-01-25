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


import os
import sys
import time


from ucsmsdk.utils.ccoimage import get_ucs_cco_image_list
from ucsmsdk.utils.ccoimage import get_ucs_cco_image

from ucsmsdk.mometa.top.TopSystem import TopSystem
from ucsmsdk.mometa.firmware.FirmwareCatalogue import FirmwareCatalogue
from ucsmsdk.mometa.firmware.FirmwareDownloader import FirmwareDownloader
from ucsmsdk.mometa.firmware.FirmwareDownloader import FirmwareDownloaderConsts


def firmware_available(username, password, mdf_id_list=None, proxy=None):
    images = get_ucs_cco_image_list(username=username, password=password,
                                  mdf_id_list=mdf_id_list, proxy=proxy)

    image_names = [image.image_name for image in images]
    return sorted(image_names)


def firmware_download(image_name, username, password, download_dir,
                      mdf_id_list=None, proxy=None):

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


def firmware_add_local(handle, image_dir, image_name):

    from ucsmsdk.ucseventhandler import UcsEventHandle

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

    handle.add_mo(firmware_downloader)
    handle.set_dump_xml()
    handle.commit()

    return firmware_downloader


def firmware_add_remote(handle, file_name, remote_path, protocol, server,
                            user="", pwd=""):

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
    handle.set_dump_xml()
    handle.commit()

def firmware_remove(handle, image_name):

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
    handle.set_dump_xml()
    handle.commit()

def firmware_activate_ucsm(handle, version="2.2(2c)"):

    mgmt_controller = handle.query_classid(class_id="MgmtController",
                                filter_str='(subject, "system", type="eq")')[0]

    firmware_running = handle.query_children(in_mo=mgmt_controller,
                                             class_id="FirmwareRunning")[0]

    if firmware_running.version == version:
        print("UCS Manager 'running' software version already at version: '%s'"
              " on UCS Domain:" % version)
        return

    infra_bundle = version + "A"
    firmware_infra_pack = handle.query_classid(class_id="FirmwareInfraPack")[0]
    firmware_infra_pack.infra_bundle_version = infra_bundle

    set_flag = False
    set_str = raw_input("Are you sure want to proceed? This will reboot the "
                    "server.Enter 'yes' to proceed.")
    if set_str.strip().lower() == "yes":
        set_flag = True

    if not set_flag:
        print("Abort activate firmware version.")
        return None

    # handle.set_mo(firmware_infra_pack)
    # handle.commit()
    print("Please wait while UCS Manager restarts on UCS Domain")
    print("Operation may take 3 or more minutes")
    time.sleep(180)

    connected = False
    retry = 1
    while not connected:
        try:
            print("Retry attempt %s" % retry),
            handle.login(force=True)
            print (": Pass")
            connected = True
        except:
            print(": Fail")
            print("Sleeping for 60 seconds")
            time.sleep(60)

    mgmt_controller = handle.query_classid(class_id="MgmtController",
                                filter_str='(subject, "system", type="eq")')[0]

    firmware_running = handle.query_children(in_mo=mgmt_controller,
                                             class_id="FirmwareRunning")[0]

    if firmware_running.version == version:
        print("UCS Manager 'running' software version updated to version: '%s'"
              " successfully on UCS Domain" % version)
        return
    else:
        print("UCS Manager 'running' software version 'NOT' updated to "
              "version:'%s'" % version)
        print("Exiting.")
        sys.exit()


def firmware_activate_blade(handle, version):

    blade_bundle = version + "B"
    rack_bundle = version + "C"

    blades = handle.query_classid("ComputeBlade")
    for blade in blades:
        mgmt_controllers = handle.query_children(in_mo=blade,
                                                 class_id="MgmtController")
        for mo in mgmt_controllers:
            if mo.subject == "blade":
                mgmt_controller = mo
                break

        firmware_running = handle.query_children(in_mo=mgmt_controller,
                                                 class_id="FirmwareRunning")
        for mo in firmware_running:
            if mo.deployment == "system" and mo.version == version:
                print("Blade <%s> is already at version <%s>" % (blade.dn,
                                                                 version))
                return

        assigned_to_dn = blade.assigned_to_dn
        if not assigned_to_dn:
            host_firmware_pack_dn = "org-root/fw-host-pack-default"
        else:
            # sp_name = re.search(r'^ls-(?P<sp_name>\w+)$',
            #         os.path.basename(assigned_to_dn)).groupdict()['sp_name']
            sp = handle.query_dn(assigned_to_dn)
            host_firmware_pack_dn = sp.oper_host_fw_policy_name

        host_firmware_pack = handle.query_dn(host_firmware_pack_dn)
        host_firmware_pack.blade_bundle_version = blade_bundle

        set_flag = False
        set_str = raw_input("Are you sure want to proceed? This will reboot "
                            "the server.Enter 'yes' to proceed.")
        if set_str.strip().lower() == "yes":
            set_flag = True

        if not set_flag:
            print("Abort update blade firmware.")
            return None

        # handle.set_mo(host_firmware_pack)
        # handle.commit()

        host_firmware_pack_dn = "host_firmware_pack_dn"

        instance_filter = '(type, "instance", type="eq")'
        assoc_filter = '(assoc_state, "associated", type="eq")'
        oper_host_fw_filter = '(oper_host_fw_policy_name, %s, type="eq")' % \
                              host_firmware_pack_dn
        filter_str = instance_filter + " and " + assoc_filter + " and " + \
                     oper_host_fw_filter

        sps = handle.query_classid(class_id="LsServer", filter_str=filter_str)
        for sp in sps:
            dn = sp.dn + '/ack'
            ls_maint_ack = handle.query_dn(dn)
            if ls_maint_ack:
                ls_maint_ack.admin_state = 'trigger-immediate'
                handle.set_mo(ls_maint_ack)
                handle.commit()


def firmware_auto_install(handle, version, image_dir, infra_only=False):

    from ucsmsdk.ucseventhandler import UcsEventHandle

    try:
        # create version string
        ver_split = version.split('(')
        version_bundle = ver_split[0] + "." + ver_split[1].strip(')')

        bundles = []
        cco_image_list = []

        # create firmware file name for the respective version
        aseries_bundle = "ucs-k9-bundles-infra." + version_bundle + ".A.bin"
        bundles.append(aseries_bundle)

        if not infra_only:
            bseries_bundle = "ucs-k9-bundles-b-series." + version_bundle + \
                             ".B.bin"
            bundles.append(bseries_bundle)

            cseries_bundle = "ucs-k9-bundles-c-series." + version_bundle + \
                             ".C.bin"
            bundles.append(cseries_bundle)

        print("Starting Firmware download process to local directory: %s" %
              image_dir)

        # adding files to cco image list if not available in local directory
        for bundle in bundles:
            file_path = os.path.join(image_dir, bundle)
            if os.path.exists(file_path):
                print("Image already exist in image directory ")
            else:
                cco_image_list.append(bundle)

        # if image not available raising exception to download
        if cco_image_list:
            raise ValueError("Download images %s using firmware_download" %
                             cco_image_list)

        # check if image is already uploaded to ucs domain
        for image in bundles:
            print("Checking if image file: '%s' is already uploaded to UCS "
                  "Domain" % image)

            deleted = False
            filter_str = '(name, %s, type="eq")' % image
            firmware_package = handle.query_classid(
                class_id="FirmwareDistributable", filter_str=filter_str)[0]
            if firmware_package:
                firmware_dist_image = handle.query_children(
                    in_mo=firmware_package, class_id="FirmwareDistImage")[0]
                if firmware_dist_image:
                    if firmware_dist_image.image_deleted != "":
                        deleted = True

            # image does not exist then upload
            if deleted or not firmware_package:
                print("Uploading file to UCSM.")
                firmware = firmware_add_local(handle, image_dir, image)
                eh = UcsEventHandle(handle)
                eh.add(managed_object=firmware, prop="transfer_state",
                       success_value=['downloaded'], poll_sec=30,
                       timeout_sec=600)
                print("Upload of image file '%s' is completed." % image)

            else:
                print("Image file '%s' is already upload available on UCSM" %
                      image)

        # Activate UCSM
        firmware_activate_ucsm(handle, version=version)

        if not infra_only:
            # Activate Blade
            firmware_activate_blade(handle, version=version)
    except:
        print("Error Occurred in Script.")
        handle.logout()
        raise


