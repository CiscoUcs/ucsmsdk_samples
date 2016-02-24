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

"""
This module performs the operation related to callhome.
"""


def call_home_config(handle, contact=None, phone=None, email=None,
                     addr=None, customer=None, contract=None, site=None,
                     r_from=None, reply_to=None, urgency=None,
                     host=None, port=None):
    """
    Configures call home alert

    Args:
        handle (UcsHandle)
        contact (string): Contact Name
        phone (string): phone number e.g. +91-1234567890
        email (string): contact email address
        addr (string): contact address
        customer (number): customer id
        contract (number): contract id
        site (number): site id
        r_from (string): from email address
        reply_to (string): to email address
        urgency (string): alert priority
         valid values are "alert", "critical", "debug", "emergency",
         "error", "info", "notice", "warning"
        host (string): ip address or hostname
        port (number): port number

    Returns:
        None

    Raises:
        ValueError: If CallhomeSource or CallhomeSmtp is not present

    Example:
        from ucsmsdk.mometa.callhome.CallhomeSource import \
            CallhomeSourceConsts

        call_home_config(handle,
                         contact="user name",
                         phone="+91-1234567890",
                         email="user@cisco.com",
                         addr="user address",
                         customer="1111",
                         contract="2222",
                         site="3333",
                         r_from="from@cisco.com",
                         reply_to="to@cisco.com",
                         urgency=CallhomeSourceConsts.URGENCY_ALERT,
                         host="10.10.10.12",
                         port="25"
                         )
    """

    # configure call home
    dn = "call-home/source"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Call home source '%s' not available." % dn)

    if contact is not None:
        mo.contact = contact
    if phone is not None:
        mo.phone = phone
    if email is not None:
        mo.email = email
    if addr is not None:
        mo.addr = addr
    if customer is not None:
        mo.customer = customer
    if contract is not None:
        mo.contract = contract
    if site is not None:
        mo.site = site
    if r_from is not None:
        mo.r_from = r_from
    if reply_to is not None:
        mo.reply_to = reply_to
    if urgency is not None:
        mo.urgency = urgency
    handle.set_mo(mo)
    handle.commit()

    smtp_dn = "call-home/smtp"
    mo_smtp = handle.query_dn(smtp_dn)
    if not mo_smtp:
        raise ValueError("Call home smtp '%s' not available." % smtp_dn)

    if host is not None:
        mo.host = host
    if port is not None:
        mo.port = port
    handle.set_mo(mo_smtp)
    handle.commit()


def call_home_enable(handle, alert_throttling_admin_state=None, name="",
                     descr=""):
    """
    Enables call home alert.

    Args:
        handle (UcsHandle)
        alert_throttling_admin_state (string): "on" or "off"
        name (string): name
        descr (string): description

    Returns:
        CallhomeEp : ManagedObject

    Raises:
        ValueError: If CallhomeEp is not present

    Example:
        call_home_state_enable(handle)
    """

    call_home = handle.query_dn("call-home")
    if not call_home:
        raise ValueError("Call home not available.")

    call_home.admin_state = "on"
    if alert_throttling_admin_state is not None:
        call_home.alert_throttling_admin_state = alert_throttling_admin_state
    call_home.name = name
    call_home.descr = descr
    handle.set_mo(call_home)
    handle.commit()

    return call_home


def call_home_disable(handle):
    """
    Disables call home alert.

    Args:
        handle (UcsHandle)

    Returns:
        CallhomeEp : ManagedObject

    Raises:
        ValueError: If CallhomeEp is not present

    Example:
        call_home_state_disable(handle)
    """

    call_home = handle.query_dn("call-home")
    if not call_home:
        raise ValueError("Call home not available.")

    call_home.admin_state = "off"
    handle.set_mo(call_home)
    handle.commit()

    return call_home


def anonymous_reporting_enable(handle):
    """
    Enables call home anonymous reporting.

    Args:
        handle (UcsHandle)

    Returns:
        CallhomeAnonymousReporting : ManagedObject

    Raises:
        ValueError: If CallhomeAnonymousReporting is not present

    Example:
        anonymous_reporting_enable(handle)
    """

    mo = handle.query_dn("call-home/anonymousreporting")
    if not mo:
        raise ValueError("call home anonymous reporting is not available.")

    mo.admin_state = "on"
    handle.set_mo(mo)
    handle.commit()

    return mo


def anonymous_reporting_disable(handle):
    """
    Disables call home anonymous reporting.

    Args:
        handle (UcsHandle)

    Returns:
        CallhomeAnonymousReporting : ManagedObject

    Raises:
        ValueError: If CallhomeAnonymousReporting is not present

    Example:
        anonymous_reporting_disable(handle)
    """

    mo = handle.query_dn("call-home/anonymousreporting")
    if not mo:
        raise ValueError("Anonymous reporting is not available.")

    mo.admin_state = "off"
    handle.set_mo(mo)
    handle.commit()
    return mo
