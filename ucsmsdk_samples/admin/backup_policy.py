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


def backup_policy_remote_create(handle, hostname, user, pwd, remote_file,
                                admin_state,
                                type="full-state",
                                proto="ftp",
                                preserve_pooled_values="no"):
    """
    This method creates a remote backup policy.

    Args:
        handle (UcsHandle)
        hostname (string): IP or name of the remote host.
        user (string): user of the remote host.
        pwd (string): authentication password of the user.
        remote_file (string): Absolute path at remote destination.
        admin_state (string): "enabled" or "disabled"
        type (string): Backup type "config-all", "config-logical",
                        "config-system", "full-state"
        proto (string): Communication protocol "ftp","scp","tftp","sftp"
        preserve_pooled_values (string): "yes" or "no"

    Returns:
        MgmtBackup: Managed object

    Example:
        mo = backup_policy_remote_create(handle, hostname="10.10.10.10",
                            user="root", pwd="12345",
                            remote_file="/root/backup",
                            admin_state="enabled",
                            type="full-state", proto="scp")
    """
    from ucsmsdk.mometa.mgmt.MgmtBackup import MgmtBackup

    mo = MgmtBackup(parent_mo_or_dn="sys", proto=proto,
                    preserve_pooled_values=preserve_pooled_values,
                    hostname=hostname,
                    pwd=pwd,
                    admin_state=admin_state,
                    user=user,
                    type=type,
                    remote_file=remote_file)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def backup_policy_remote_remove(handle, hostname):
    """
    This method removes a backup policy.

    Args:
        handle (UcsHandle)
        hostname (string): IP or name of the remote host.

    Returns:
        None

    Raises:
        ValueError - If MgmtBackup Mo is not present

    Example:
        backup_policy_remote_remove(handle, hostname="10.10.10.10")
    """

    policy_dn = "sys/backup-" + hostname
    mo = handle.query_dn(policy_dn)
    if mo is not None:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("No Backup policy <%s>.Nothing to remove." % hostname)
