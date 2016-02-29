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
This module performs the operation related to user.
"""


def user_create(handle, name, first_name, last_name, descr, clear_pwd_history,
                phone, email, pwd, expires, pwd_life_time, expiration,
                enc_pwd="", enc_pwd_set="no", account_status="active",
                role="read-only", role_descr=""):
    """
    Creates user and assign role to it.

    Args:
        handle (UcsHandle)
        name (string): name
        first_name (string): first_name
        last_name (string): last_name
        descr (string): descr
        clear_pwd_history (string): clear_pwd_history
        phone (string): phone
        email (string): email
        pwd (string): pwd
        expires (string): expires
        pwd_life_time (string): pwd_life_time
        expiration (string): expiration
        enc_pwd (string): enc_pwd
        enc_pwd_set (string): enc_pwd_set
        account_status (string): account_status
        role (string): role
        role_descr (string): role_descr

    Returns:
        AaaUser: Managed Object

    Example:
        user_create(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  enc_pwd_set="no", account_status="active")
    """

    from ucsmsdk.mometa.aaa.AaaUser import AaaUser
    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    mo = AaaUser(parent_mo_or_dn="sys/user-ext",
                 name=name,
                 first_name=first_name,
                 last_name=last_name,
                 descr=descr,
                 clear_pwd_history=clear_pwd_history,
                 phone=phone,
                 email=email,
                 pwd=pwd,
                 expires=expires,
                 pwd_life_time=pwd_life_time,
                 expiration=expiration,
                 enc_pwd=enc_pwd,
                 enc_pwd_set=enc_pwd_set,
                 account_status=account_status)
    AaaUserRole(parent_mo_or_dn=mo, name=role, descr=role_descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_exists(handle, name, first_name, last_name, descr, clear_pwd_history,
                phone, email, pwd, expires, pwd_life_time, expiration,
                enc_pwd="", enc_pwd_set="no", account_status="active"):
    """
    checks if user exists

    Args:
        handle (UcsHandle)
        name (string): name
        first_name (string): first_name
        last_name (string): last_name
        descr (string): descr
        clear_pwd_history (string): clear_pwd_history
        phone (string): phone
        email (string): email
        pwd (string): pwd
        expires (string): expires
        pwd_life_time (string): pwd_life_time
        expiration (string): expiration
        enc_pwd (string): enc_pwd
        enc_pwd_set (string): enc_pwd_set
        account_status (string): account_status

    Returns:
        True/False

    Example:
        user_exists(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  enc_pwd_set="no", account_status="active")
    """

    dn = "sys/user-ext/user-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((first_name and mo.first_name != first_name) and
            (last_name and mo.last_name != last_name) and
            (descr and mo.descr != descr) and
            (clear_pwd_history and
             mo.clear_pwd_history != clear_pwd_history) and
            (phone and mo.phone != phone) and
            (email and mo.email != email) and
            (pwd and mo.pwd != pwd) and
            (expires and mo.expires != expires) and
            (pwd_life_time and mo.pwd_life_time != pwd_life_time) and
            (expiration and mo.expiration != expiration) and
            (enc_pwd and mo.enc_pwd != enc_pwd) and
            (enc_pwd_set and mo.enc_pwd_set != enc_pwd_set) and
            (account_status and mo.account_status != account_status)):
            return False
        return True
    return False


def user_modify(handle, name, first_name=None, last_name=None, descr=None,
                clear_pwd_history=None, phone=None, email=None, pwd=None,
                expires=None, pwd_life_time=None, expiration=None,
                enc_pwd=None, enc_pwd_set=None, account_status=None):
    """
    modifies user

    Args:
        handle (UcsHandle)
        name (string): name
        first_name (string): first_name
        last_name (string): last_name
        descr (string): descr
        clear_pwd_history (string): clear_pwd_history
        phone (string): phone
        email (string): email
        pwd (string): pwd
        expires (string): expires
        pwd_life_time (string): pwd_life_time
        expiration (string): expiration
        enc_pwd (string): enc_pwd
        enc_pwd_set (string): enc_pwd_set
        account_status (string): account_status

    Returns:
        AaaUser: Managed Object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_modify(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  enc_pwd_set="no", account_status="active")
    """

    dn = "sys/user-ext/user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("User does not exist.")

    if first_name is not None:
        mo.first_name = first_name
    if last_name is not None:
        mo.last_name = last_name
    if descr is not None:
        mo.descr = descr
    if clear_pwd_history is not None:
        mo.clear_pwd_history = clear_pwd_history
    if phone is not None:
        mo.phone = phone
    if email is not None:
        mo.email = email
    if pwd is not None:
        mo.pwd = pwd
    if expires is not None:
        mo.expires = expires
    if pwd_life_time is not None:
        mo.pwd_life_time = pwd_life_time
    if expiration is not None:
        mo.expiration = expiration
    if enc_pwd is not None:
        mo.enc_pwd = enc_pwd
    if enc_pwd_set is not None:
        mo.enc_pwd_set = enc_pwd_set
    if account_status is not None:
        mo.account_status = account_status

    handle.set_mo(mo)
    handle.commit()
    return mo


def user_delete(handle, name):
    """
    deletes user

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_modify(handle, name="test")
    """

    dn = "sys/user-ext/user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("User does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def user_add_role(handle, user_name, name, descr=""):
    """
    Adds role to an user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename
        descr (string): descr

    Returns:
        AaaUserRole: Managed object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_add_role(handle, user_name="test", name="admin")
    """

    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn = "sys/user-ext/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("User does not exist.")

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_role_exists(handle, user_name, name, descr=""):
    """
    check if role is already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename
        descr (string): descr

    Returns:
        True/False

    Example:
        user_role_exists(handle, user_name="test", name="admin")
    """

    user_dn = "sys/user-ext/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def user_remove_role(handle, user_name, name):
    """
    Remove role from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        None

    Raises:
        ValueError: If AaaUserRole is not present

    Example:
        user_remove_role(handle, user_name="test", name="admin")
    """

    user_dn = "sys/user-ext/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Role is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def user_add_locale(handle, user_name, name, descr=""):
    """
    Adds locale to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        descr (string): descr

    Returns:
        AaaUserLocale: Managed Object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_add_locale(handle, user_name="test", name="testlocale")
    """

    from ucsmsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    dn = "sys/user-ext/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("User does not exist.")

    mo = AaaUserLocale(parent_mo_or_dn=obj, name=name, descr=descr)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_locale_exists(handle, user_name, name, descr=""):
    """
    check if locale already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        descr (string): descr

    Returns:
        True/False

    Example:
        user_locale_exists(handle, user_name="test", name="testlocale")
    """

    user_dn = "sys/user-ext/user-" + user_name
    dn = user_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if mo:
        if descr and mo.descr != descr:
            return False
        return True
    return False


def user_remove_locale(handle, user_name, name):
    """
    Remove locale from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        None

    Raises:
        ValueError: If AaaUserLocale is not present

    Example:

    """

    user_dn = "sys/user-ext/user-" + user_name
    dn = user_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Locale is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def password_strength_check(handle, descr="", policy_owner="local"):
    """
    check pasword strength for locally authenticated user

    Args:
        handle (UcsHandle)
        descr (string): description
        policy_owner (string): ["local", "pending-policy", "policy"]

    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_check(handle)
    """

    mo = handle.query_dn("sys/user-ext")
    mo.pwd_strength_check = "yes"
    mo.descr = descr
    mo.policy_owner = policy_owner
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_strength_uncheck(handle):
    """
    check or un-check pasword strength for locally authenticated user

    Args:
        handle (UcsHandle)

    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_uncheck(handle)
    """

    mo = handle.query_dn("sys/user-ext")
    mo.pwd_strength_check = "no"
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_profile_modify(handle, change_interval=None,
                            no_change_interval=None,
                            change_during_interval=None, change_count=None,
                            history_count=None, expiration_warn_time=None,
                            descr=None, policy_owner=None):
    """
    modfiy passpord profile of locally authenticated user

    Args:
        handle (UcsHandle)
        change_interval (number): change interval
        no_change_interval (number): no change interval
        change_during_interval (string): ["disable", "enable"]
        change_count (number): change count
        history_count (number): history count
        expiration_warn_time(number): expiration warn time
        descr (string): description
        policy_owner (string): ["local", "pending-policy", "policy"]

    Returns:
        AaaPwdProfile: Managed Object

    Raises:
        ValueError: If AaaPwdProfile is not present

    Example:
        password_profile_modify(handle, change_count="2")
    """

    dn = "sys/user-ext/pwd-profile"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("password profile does not exist.")

    if change_interval is not None:
        mo.change_interval = change_interval
    if no_change_interval is not None:
        mo.no_change_interval = no_change_interval
    if change_during_interval is not None:
        mo.change_during_interval = change_during_interval
    if change_count is not None:
        mo.change_count = change_count
    if history_count is not None:
        mo.history_count = history_count
    if expiration_warn_time is not None:
        mo.expiration_warn_time = expiration_warn_time
    if descr is not None:
        mo.descr = descr
    if policy_owner is not None:
        mo.policy_owner = policy_owner

    handle.set_mo(mo)
    handle.commit()
    return mo
