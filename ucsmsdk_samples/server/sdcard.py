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

import time
import logging

from ucsmsdk.ucseventhandler import UcsEventHandle
from ucsmsdk.mometa.storage.StorageFlexFlashControllerFsmStage import \
    StorageFlexFlashControllerFsmStageConsts

log = logging.getLogger("ucs")

end_script = False


def _operation_callback(mce):
    """
    Callback for Flex Controller
    """

    global end_script
    # TODO
    if mce.mo.fsm_status == \
            StorageFlexFlashControllerFsmStageConsts.STAGE_STATUS_SUCCESS:
        log.debug("Operation Successful. FSM State: " + mce.mo.stage_state)
    elif mce.mo.fsm_status == \
            StorageFlexFlashControllerFsmStageConsts.STAGE_STATUS_FAIL:
        log.debug("Operation Failed. FSM State: " + mce.mo.stage_state)
    end_script = True


def _operation_monitor(handle, event_handle, mo):
    """
    Adds an event handler to monitor the Flex Controller.
    """

    fsm_mo = handle.query_classid(
        class_id="storageFlexFlashControllerFsmStage",
        filter_str="(dn,'" + mo.dn + "')")

    event_handle.add(
        managed_object=fsm_mo[0],
        prop="stage_status",
        success_value=[
            StorageFlexFlashControllerFsmStageConsts.STAGE_STATUS_SUCCESS],
        failure_value=[
            StorageFlexFlashControllerFsmStageConsts.STAGE_STATUS_FAIL],
        timeout_sec=600,
        call_back=_operation_callback)


def configure_storage_flex_flash_controller(handle, parent_dn, flex_id,
                                            operation_request,
                                            admin_slot_number="NA",
                                            wait_operation_completion=True):
    """
    This method configures the storage card for flex controller.

    Args:
        handle (UcsHandle)
        parent_dn (string): Parent Dn of the controller
        operation_request (string): format/reset/pair
        admin_slot_number (string): 1/2/NA
        flex_id : ID of Storage Flex
        wait_operation_completion : True/False

    Returns:
        None

    Raises:
        ValueError: If StorageFlexFlashController is not present

    Example:
        a. To Reset the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="reset",
                                                admin_slot_number="NA")
        b. To Format the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="format",
                                                admin_slot_number="NA")

        c. To Auto-Sync the SD Card.
        configure_storage_flex_flash_controller(handle,flex_id="1",
                                                operation_request="pair",
                                                admin_slot_number="1")

    """

    from ucsmsdk.mometa.storage.StorageFlexFlashController import \
        StorageFlexFlashController

    dn = parent_dn + "/board"
    q_mo = handle.query_dn(dn)
    if q_mo is not None:
        mo = StorageFlexFlashController(parent_mo_or_dn=dn, id=flex_id,
                                        operation_request=operation_request,
                                        admin_slot_number=admin_slot_number)
        handle.add_mo(mo, True)
        handle.commit()
        if wait_operation_completion:
            # add a watch on sp
            event_handle = UcsEventHandle(handle)
            _operation_monitor(handle=handle, event_handle=event_handle, mo=mo)
            while not end_script:
                time.sleep(1)
    else:
        raise ValueError("Storage Flex controller does not exists.")
