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


def time_zone_set(handle, timezone):
    """
    This method sets the timezone of the UCSM.

    Args:
        handle (UcsHandle)
        timezone (string): time zone e.g. "Asia/Kolkata"

    Returns:
        CommDateTime: Managed object

    Raises:
        ValueError: If CommDateTime Mo is not found

    Example:
        To Set Time Zone:
            mo = time_zone_set(handle, "Asia/Kolkata")

        To Un-Set Time Zone:
            mo = time_zone_set(handle, "")
    """

    mo = handle.query_dn("sys/svc-ext/datetime-svc")
    if not mo:
        raise ValueError("timezone does not exist")

    mo.timezone = timezone
    mo.policy_owner = "local"
    mo.admin_state = "enabled"
    mo.port = "0"

    handle.set_mo(mo)
    handle.commit()
    return mo


def ntp_server_create(handle, name, descr=""):
    """
    Adds NTP server using IP address.

    Args:
        handle (UcsHandle)
        name (string): NTP server IP address or Name
        descr (string): Basic description about NTP server

    Returns:
        CommNtpProvider: Managed object

    Example:
        ntp_server_create(handle, "72.163.128.140", "Default NTP")
    """

    from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider

    mo = CommNtpProvider(parent_mo_or_dn="sys/svc-ext/datetime-svc",
                         name=name,
                         descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ntp_server_exists(handle, name, descr=""):
    """
    checks if ntp server exists.

    Args:
        handle (UcsHandle)
        name (string): NTP server IP address or Name
        descr (string): Basic description about NTP server

    Returns:
        True/False

    Example:
        ntp_server_exists(handle, "72.163.128.140", "Default NTP")
    """

    dn = "sys/svc-ext/datetime-svc/ntp-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def ntp_server_remove(handle, name):
    """
    Removes the NTP server.

    Args:
        handle (UcsHandle)
        name : NTP server IP address or Name

    Returns:
        None

    Raises:
        ValueError: If CommNtpProvider is not found

    Example:
        ntp_server_remove(handle, "72.163.128.140")
    """

    dn = "sys/svc-ext/datetime-svc/ntp-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("NTP Server not found. Nothing to remove.")

    handle.remove_mo(mo)
    handle.commit()
