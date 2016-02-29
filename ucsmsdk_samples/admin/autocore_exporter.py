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


def tftp_core_exporter_enable(handle,
                              hostname,
                              path,
                              port,
                              descr=""):
    """
    This method configures UCSM tftp core exporter.

    Args:
        handle (UcsHandle)
        hostname (string): IP or Hostname of server.
        path (string): Absolute path where core files are to be stored.
        port (string): Port number of tftp exporter
        descr (string): Basic description about configuration.


    Returns:
        SysdebugAutoCoreFileExportTarget: ManagedObject

    Example:
        mo = tftp_core_exporter_enable(handle,hostname="10.65.180.18",
                port="69", path="/root/tftp")
    """

    from ucsmsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import\
        SysdebugAutoCoreFileExportTarget

    mo = SysdebugAutoCoreFileExportTarget(parent_mo_or_dn="sys/sysdebug",
                                          descr=descr,
                                          hostname=hostname,
                                          admin_state="enabled",
                                          path=path, port=port)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def tftp_core_exporter_disable(handle):
    """
    This method disables UCSM tftp core exporter.

    Args:
        handle (UcsHandle)

    Returns:
        SysdebugAutoCoreFileExportTarget: ManagedObject

    Example:
        tftp_core_exporter_disable(handle)
    """

    from ucsmsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import\
        SysdebugAutoCoreFileExportTarget

    mo = SysdebugAutoCoreFileExportTarget(parent_mo_or_dn="sys/sysdebug",
                                          admin_state="disabled")

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
