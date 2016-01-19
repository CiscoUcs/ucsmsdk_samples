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


def syslog_local_console(handle, admin_state, severity="emergencies"):
    """
    This method configures System Logs on local console.

    Args:
        handle (UcsHandle)
        admin_state (string): "enabled" or "disabled"
        severity (string): Level of logging.

    Returns:
        CommSyslogConsole: Managed object

    Example:
        To Enable Logs on Console:
        mo = syslog_local_console(handle, admin_state="enabled",
                                    severity="alert")

        To Disable Logs on Console:
        mo = syslog_local_console(handle, admin_state="disabled")
    """

    from ucsmsdk.mometa.comm.CommSyslogConsole import CommSyslogConsole

    mo = CommSyslogConsole(parent_mo_or_dn="sys/svc-ext/syslog",
                           admin_state=admin_state, severity=severity)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def syslog_local_monitor(handle, admin_state, severity="emergencies"):
    """
    This method configures System Logs on local monitor.

    Args:
        handle (UcsHandle)
        admin_state (string): "enabled" or "disabled"
        severity (string): Level of logging.

    Returns:
        CommSyslogMonitor: Managed object

    Example:
        To Enable Logs:
        mo = syslog_local_monitor(handle, admin_state="enabled",
                                    severity="alert")

        To Disable Logs:
        mo = syslog_local_monitor(handle, admin_state="disabled")
    """

    from ucsmsdk.mometa.comm.CommSyslogMonitor import CommSyslogMonitor

    mo = CommSyslogMonitor(parent_mo_or_dn="sys/svc-ext/syslog",
                           admin_state=admin_state,
                           severity=severity)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def syslog_local_file(handle, admin_state, name, severity="emergencies",
                       size="40000"):
    """
    This method configures System Logs on local file storage.

    Args:
        handle (UcsHandle)
        admin_state (string): "enabled" or "disabled"
        name (string): Name of Log file.
        severity (string): Level of logging.
        size (string): Maximum allowed size of log file(In KBs).

    Returns:
        CommSyslogFile: Managed object

    Example:
        To Enable Logs:
        mo = syslog_local_file(handle, admin_state="enabled", severity="alert"
                            size="435675", name="sys_log")

        To Disable Logs:
        mo = syslog_local_file(handle, admin_state="disabled")
    """

    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFile

    mo = CommSyslogFile(parent_mo_or_dn="sys/svc-ext/syslog", size=size,
                        admin_state=admin_state,
                        name=name,
                        severity=severity)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def syslog_remote_enable(handle, name, hostname,
                         severity="emergencies", forwarding_facility="local0"):

    """
    This method enables System Logs on remote server.

    Args:
        handle (UcsHandle)
        hostname (string) : Remote host IP or Name
        severity (string): Level of logging.
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"
        forwarding_facility (string): Forwarding mechanism local0 to local7.

    Returns:
        CommSyslogClient: Managed object

    Example:
        syslog_remote_enable(handle, hostname="192.168.1.2",
                        severity="alert",
                        name="primary")
    """

    from ucsmsdk.mometa.comm.CommSyslogClient import CommSyslogClient

    mo = CommSyslogClient(parent_mo_or_dn="sys/svc-ext/syslog",
                          forwarding_facility=forwarding_facility,
                          hostname=hostname, admin_state="enabled",
                          severity=severity, name=name)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def syslog_remote_disable(handle, name):

    """
    This method disables System Logs on remote server.

    Args:
        handle (UcsHandle)
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"

    Returns:
        None

    Raises:
        ValueError: If CommSyslogClient Mo is not present

    Example:
        syslog_remote_disable(handle, name="primary")
    """

    mo = handle.query_dn("sys/svc-ext/syslog/client-" + name)
    if mo:
        mo.admin_state = "disabled"
        handle.add_mo(mo, modify_present=True)
        handle.commit()
    else:
        raise ValueError("Syslog Mo is not available.")


def syslog_source(handle, faults="enabled", audits="enabled",
                  events="enabled"):
    """
    This method configures Type of System Logs.

    Args:
        handle (UcsHandle)
        faults (string) : for fault logging.
        audits (string): for audit task logging.
        events (string): for event logging.

    Returns:
        CommSyslogSource: Managed object

    Example:
            syslog_source(handle, faults="enabled", audits="disabled",
                    events="disabled")

    """

    from ucsmsdk.mometa.comm.CommSyslogSource import CommSyslogSource

    mo = CommSyslogSource(parent_mo_or_dn="sys/svc-ext/syslog",
                          faults=faults,
                          audits=audits,
                          events=events)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
