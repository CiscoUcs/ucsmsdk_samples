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


def configure_storage_flex_flash_controller(handle, parent_dn,flex_id,
                                            operation_request,
                                            configured_mode,
                                            operating_mode,
                                            admin_slot_number="NA"):
    """
    This method configures the storage card for flex controller.

    Args:
        handle (UcsHandle)
        parent_dn (string): Parent Dn of the controller
        operating_mode (string): mirror/unknown/util
        configured_mode (string): mirror/unknown/util
        operation_request (string): format/reset/pair
        admin_slot_number (string): 1/2/NA

    Returns:
        None

    Example:
        a. To Reset the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="reset",
                                                operating_mode="mirror",
                                                configured_mode="mirror"
                                                admin_slot_number="NA")
        b. To Format the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="format",
                                                operating_mode="mirror",
                                                configured_mode="mirror"
                                                admin_slot_number="NA")

        c. To Auto-Sync the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="pair",
                                                operating_mode="mirror",
                                                configured_mode="mirror"
                                                admin_slot_number="1")


    """
    from ucsmsdk.mometa.storage.StorageFlexFlashController import \
        StorageFlexFlashController

    dn = parent_dn + "/board"
    q_mo = handle.query_dn(dn)
    if q_mo is not None:
        mo = StorageFlexFlashController(parent_mo_or_dn=dn,id=flex_id,
                                        configured_mode=configured_mode,
                                        operation_request=operation_request,
                                        admin_slot_number=admin_slot_number,
                                        operating_mode=operating_mode)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        raise ValueError("Storage Flex controller does not exists.")