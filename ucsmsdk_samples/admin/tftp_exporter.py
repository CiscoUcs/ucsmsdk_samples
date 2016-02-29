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


def tftp_core_exporter_enable(handle, hostname=None, path=None, port=None,
                              descr=None):
    """
    This method enables UCSM tftp core exporter.

    Args:
        handle (UcsHandle)
        hostname (string): IP or Hostname of server.
        path (string): Absolute path where core files are to be stored.
        port (string): Port number of tftp exporter
        descr (string): Basic description about configuration.


    Returns:
        SysdebugAutoCoreFileExportTarget: Managed Object

    Raises:
        ValueError: If SysdebugAutoCoreFileExportTarget is not present

    Example:
        To Enable Core Exporter:
            tftp_core_exporter_enable(handle,hostname="10.65.180.18",
                    port="69", path="/root/tftp")
    """

    from ucsmsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import \
        SysdebugAutoCoreFileExportTargetConsts

    dn = "sys/sysdebug/file-export"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("tftp core exporter '%s' does not exist" % dn)

    mo.admin_state = SysdebugAutoCoreFileExportTargetConsts.ADMIN_STATE_ENABLED

    if hostname is not None:
        mo.hostname = hostname
    if path is not None:
        mo.path = path
    if port is not None:
        mo.port = port
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def tftp_core_exporter_disable(handle):
    """
    This method disables UCSM tftp core exporter.

    Args:
        handle (UcsHandle)

    Returns:
        SysdebugAutoCoreFileExportTarget: Managed Object

    Raises:
        ValueError: If SysdebugAutoCoreFileExportTarget is not present

    Example:
        To Disable Core Exporter:
            tftp_core_exporter_disable(handle)
    """

    from ucsmsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import \
        SysdebugAutoCoreFileExportTargetConsts

    dn = "sys/sysdebug/file-export"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("tftp core exporter '%s' does not exist" % dn)

    mo.admin_state = \
        SysdebugAutoCoreFileExportTargetConsts.ADMIN_STATE_DISABLED

    handle.set_mo(mo)
    handle.commit()
    return mo
