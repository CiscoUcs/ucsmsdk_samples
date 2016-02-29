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


def bios_create(handle, parent_org_dn, name, descr="",
                reboot_on_update="no",
                vp_cdn_control="platform-default",
                vp_front_panel_lockout="platform-default",
                vp_post_error_pause="platform-default",
                vp_quiet_boot="platform-default",
                vp_resume_on_ac_power_loss="platform-default",
                vp_serial_port_a_enable="platform-default",
                vp_baud_rate="platform-default",
                vp_console_redirection="platform-default",
                vp_flow_control="platform-default",
                vp_legacy_os_redirection="platform-default",
                vp_putty_key_pad="platform-default",
                vp_terminal_type="platform-default"):
    """
    This method creates the Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        descr (string): Basic description.
        reboot_on_update : "yes" or "no"
        vp_cdn_control: "disabled", "enabled", "platform-default"
        vp_front_panel_lockout: "disabled", "enabled", "platform-default"
        vp_post_error_pause: "disabled", "enabled", "platform-default"
        vp_quiet_boot: "disabled", "enabled", "platform-default"
        vp_resume_on_ac_power_loss: "last-state", "platform-default","reset",
            "stay-off"
        vp_serial_port_a_enable: "disabled", "enabled", "platform-default"
        vp_baud_rate: "115200", "19200", "platform-default"
        vp_console_redirection: "com-0", "disabled", "enabled",
            "platform-default"
        vp_flow_control: "none", "platform-default", "rts-cts"
        vp_legacy_os_redirection: "80x24", "80x25", "disabled", "enabled"
        vp_putty_key_pad: "escn", "linux", "platform-default"
        vp_terminal_type: "pc-ansi", "platform-default", "vt-utf8", "vt100",
            "vt100-plus"

    Returns:
         BiosVProfile: Managed Object

    Raises:
        ValueError: If OrgOrg is not present

    Example:
        bios_create(handle,name="sample_bios",parent_dn="org-root/org-sample",
                    reboot_on_update="yes",
                    vp_quite_boot="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
    from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import \
        BiosVfConsistentDeviceNameControl
    from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import \
        BiosVfFrontPanelLockout
    from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
    from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
    from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import \
        BiosVfResumeOnACPowerLoss
    from ucsmsdk.mometa.bios.BiosVfSerialPortAEnable import \
        BiosVfSerialPortAEnable
    from ucsmsdk.mometa.bios.BiosVfConsoleRedirection import \
        BiosVfConsoleRedirection

    obj = handle.query_dn(parent_org_dn)
    if obj is None:
        raise ValueError("Parent org does not exist.")

    mo = BiosVProfile(
        parent_mo_or_dn=obj, name=name, descr=descr,
        reboot_on_update=reboot_on_update)

    mo_1 = BiosVfConsistentDeviceNameControl(
        parent_mo_or_dn=mo,
        vp_cdn_control=vp_cdn_control)

    mo_2 = BiosVfFrontPanelLockout(
        parent_mo_or_dn=mo,
        vp_front_panel_lockout=vp_front_panel_lockout)

    mo_3 = BiosVfPOSTErrorPause(
        parent_mo_or_dn=mo, vp_post_error_pause=vp_post_error_pause)

    mo_4 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot=vp_quiet_boot)

    mo_5 = BiosVfResumeOnACPowerLoss(
        parent_mo_or_dn=mo,
        vp_resume_on_ac_power_loss=vp_resume_on_ac_power_loss)

    mo_6 = BiosVfSerialPortAEnable(
        parent_mo_or_dn=mo, vp_serial_port_a_enable=vp_serial_port_a_enable)

    mo_7 = BiosVfConsoleRedirection(
        parent_mo_or_dn=mo,
        vp_baud_rate=vp_baud_rate,
        vp_console_redirection=vp_console_redirection,
        vp_flow_control=vp_flow_control,
        vp_legacy_os_redirection=vp_legacy_os_redirection,
        vp_putty_key_pad=vp_putty_key_pad,
        vp_terminal_type=vp_terminal_type)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def bios_remove(handle, name, parent_org_dn):
    """
    This method removes the Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.

    Returns:
        None

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_remove(handle,name="sample_bios",parent_dn="org-root/org-sample")
    """

    profile_dn = parent_org_dn + "/bios-prof-" + name
    mo = handle.query_dn(profile_dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("Bios policy '%s' not found.Nothing to remove" %
                         profile_dn)


def bios_add_token(handle, name, parent_org_dn, token_name, token_value):
    # TODO
    pass


def bios_serial_port(handle, name, parent_org_dn,
                     vp_serial_port_a_enable="platform-default"):
    """
    This method configures serial port option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_serial_port_a_enable="disabled", "enabled", "platform-default"

    Returns:
        BiosVfSerialPortAEnable: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_serial_port(handle,name="sample_bios",
                        parent_dn="org-root/org/sample",
                        vp_serial_port_a_enable="enabled")

    """

    from ucsmsdk.mometa.bios.BiosVfSerialPortAEnable import \
        BiosVfSerialPortAEnable

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfSerialPortAEnable(
            parent_mo_or_dn=obj,
            vp_serial_port_a_enable=vp_serial_port_a_enable)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_console_redirection(handle, name, parent_org_dn,
                             vp_baud_rate="platform-default",
                             vp_console_redirection="platform-default",
                             vp_flow_control="platform-default",
                             vp_legacy_os_redirection="platform-default",
                             vp_putty_key_pad="platform-default",
                             vp_terminal_type="platform-default"):
    """
    This method configures console option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_baud_rate: "115200", "19200", "platform-default"
        vp_console_redirection: "com-0", "disabled", "enabled",
            "platform-default"
        vp_flow_control: "none", "platform-default", "rts-cts"
        vp_legacy_os_redirection: "80x24", "80x25", "disabled", "enabled"
        vp_putty_key_pad: "escn", "linux", "platform-default"
        vp_terminal_type: "pc-ansi", "platform-default", "vt-utf8", "vt100",
            "vt100-plus"

    Returns:
        BiosVfConsoleRedirection: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_console_redirection(handle,name="sample_bios",
                                parent_dn="org-root/org-sample",
                                vp_baud_rate="115200")
    """

    from ucsmsdk.mometa.bios.BiosVfConsoleRedirection import \
        BiosVfConsoleRedirection

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfConsoleRedirection(
            parent_mo_or_dn=obj,
            vp_baud_rate=vp_baud_rate,
            vp_console_redirection=vp_console_redirection,
            vp_flow_control=vp_flow_control,
            vp_legacy_os_redirection=vp_legacy_os_redirection,
            vp_putty_key_pad=vp_putty_key_pad,
            vp_terminal_type=vp_terminal_type)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_quiet_boot(handle, name, parent_org_dn,
                         vp_quiet_boot="platform-default"):
    """
    This method configures quite boot option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_quiet_boot: "platform-default","disabled", "enabled"

    Returns:
        BiosVfQuietBoot: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_quiet_boot(handle,name="sample_bios",
                            parent_dn="org-root/org-sample",
                            vp_quite_boot="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQuietBoot(parent_mo_or_dn=obj, vp_quiet_boot=vp_quiet_boot)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_error_pause(handle, name, parent_org_dn,
                          vp_post_error_pause="platform-default"):
    """
    This method configures error pause option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_post_error_pause: "platform-default","disabled", "enabled"

    Returns:
        BiosVfPOSTErrorPause: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_error_pause(handle,name="sample_bios",
                            parent_dn="org-root/org-sample",
                            vp_post_error_pause="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPOSTErrorPause(
            parent_mo_or_dn=obj, vp_post_error_pause=vp_post_error_pause)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_power_loss(handle, name, parent_org_dn,
                         vp_resume_on_ac_power_loss="platform-default"):
    """
    This method configures power loss option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_resume_on_ac_power_loss: "platform-default","disabled", "enabled"

    Returns:
        BiosVfResumeOnACPowerLoss: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_power_loss(handle,name="sample_bios",
                            parent_dn="org-root/org-sample",
                            vp_resume_on_ac_power_loss="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import \
        BiosVfResumeOnACPowerLoss

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfResumeOnACPowerLoss(
            parent_mo_or_dn=obj,
            vp_resume_on_ac_power_loss=vp_resume_on_ac_power_loss)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_front_panel_lockout(handle, name, parent_org_dn,
                                  vp_front_panel_lockout="platform-default"):
    """
    This method configures front lockout option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_front_panel_lockout: "platform-default","disabled", "enabled"

    Returns:
        BiosVfFrontPanelLockout: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_front_panel_lockout(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_front_panel_lockout="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import \
        BiosVfFrontPanelLockout

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFrontPanelLockout(
            parent_mo_or_dn=obj,
            vp_front_panel_lockout=vp_front_panel_lockout)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_device_name_control(handle, name, parent_org_dn,
                                  vp_cdn_control="platform-default"):
    """
    This method configures front lockout option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_cdn_control: "platform-default","disabled", "enabled"

    Returns:
        BiosVfConsistentDeviceNameControl: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_device_name_control(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_cdn_control="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import \
        BiosVfConsistentDeviceNameControl

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfConsistentDeviceNameControl(
            parent_mo_or_dn=obj, vp_cdn_control=vp_cdn_control)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_turbo_boost(handle, name, parent_org_dn,
                          vp_intel_turbo_boost_tech="platform-default"):
    """
    This method configures turbo boost option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        bios_conf_turbo_boost: "platform-default","disabled", "enabled"

    Returns:
        BiosVfIntelTurboBoostTech: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_device_name_control(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_intel_turbo_boost_tech="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelTurboBoostTech import \
        BiosVfIntelTurboBoostTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelTurboBoostTech(
            parent_mo_or_dn=obj,
            vp_intel_turbo_boost_tech=vp_intel_turbo_boost_tech)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_speed_step(
        handle, name, parent_org_dn,
        vp_enhanced_intel_speed_step_tech="platform-default"):
    """
    This method configures intel speed option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_enhanced_intel_speed_step_tech : "platform-default","disabled",
                                            "enabled"

    Returns:
        BiosVfEnhancedIntelSpeedStepTech: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_intel_speed_step(handle,name="sample_bios",
                                parent_dn="org-root/org-sample",
                                vp_enhanced_intel_speed_step_tech="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfEnhancedIntelSpeedStepTech import \
        BiosVfEnhancedIntelSpeedStepTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfEnhancedIntelSpeedStepTech(
            parent_mo_or_dn=obj,
            vp_enhanced_intel_speed_step_tech=
                vp_enhanced_intel_speed_step_tech)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_hyper_threading(
        handle, name, parent_org_dn,
        vp_intel_hyper_threading_tech="platform-default"):
    """
    This method configures hyper threading option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_intel_hyper_threading_tech : "platform-default","disabled",
                                        "enabled"

    Returns:
        BiosVfIntelHyperThreadingTech: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_hyper_threading(handle,name="sample_bios",
                                parent_dn="org-root/org-sample",
                                vp_intel_hyper_threading_tech="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelHyperThreadingTech import \
        BiosVfIntelHyperThreadingTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelHyperThreadingTech(
            parent_mo_or_dn=obj,
            vp_intel_hyper_threading_tech=vp_intel_hyper_threading_tech)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_core_multi_processing(
        handle, name, parent_org_dn,
        vp_core_multi_processing="platform-default"):
    """
    This method configures hyper threading option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_core_multi_processing : "platform-default","disabled", "enabled"

    Returns:
        BiosVfCoreMultiProcessing: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_core_multi_processing(handle,name="sample_bios",
                                        parent_dn="org-root/org-sample",
                                        vp_core_multi_processing="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfCoreMultiProcessing import \
        BiosVfCoreMultiProcessing

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfCoreMultiProcessing(
            parent_mo_or_dn=obj,
            vp_core_multi_processing=vp_core_multi_processing)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_disable_bit(handle, name, parent_org_dn,
                          vp_execute_disable_bit="platform-default"):
    """
    This method configures disable bit option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_execute_disable_bit : "platform-default","disabled", "enabled"

    Returns:
        BiosVfExecuteDisableBit: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_disable_bit(handle,name="sample_bios",
                            parent_dn="org-root/org-sample",
                            vp_execute_disable_bit="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfExecuteDisableBit import \
        BiosVfExecuteDisableBit

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfExecuteDisableBit(
            parent_mo_or_dn=obj, vp_execute_disable_bit=vp_execute_disable_bit)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_virtual_tech(
        handle, name, parent_org_dn,
        vp_intel_virtualization_technology="platform-default"):
    """
    This method configures virtual tech option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_intel_virtualization_technology : "platform-default","disabled",
                                            "enabled"

    Returns:
        BiosVfIntelVirtualizationTechnology: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_disable_bit(handle,name="sample_bios",
                            parent_dn="org-root/org-sample",
                            vp_execute_disable_bit="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelVirtualizationTechnology import \
        BiosVfIntelVirtualizationTechnology

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelVirtualizationTechnology(
            parent_mo_or_dn=obj,
            vp_intel_virtualization_technology=
                vp_intel_virtualization_technology)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_prefetch(
        handle, name, parent_org_dn,
        vp_dcuip_prefetcher="platform-default",
        vp_adjacent_cache_line_prefetcher="platform-default",
        vp_hardware_prefetcher="platform-default",
        vp_dcu_streamer_prefetch="platform-default"):
    """
    This method configures processor pre-fetch option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_dcuip_prefetcher : "platform-default","disabled", "enabled"
        vp_adjacent_cache_line_prefetcher: "disabled", "enabled",
                                            "platform-default"
        vp_hardware_prefetcher: "disabled", "enabled", "platform-default"
        vp_dcu_streamer_prefetch: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfProcessorPrefetchConfig: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_prefetch(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_dcuip_prefetcher="enabled",
                                    vp_hardware_prefetcher="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorPrefetchConfig import \
        BiosVfProcessorPrefetchConfig

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorPrefetchConfig(
            parent_mo_or_dn=obj,
            vp_dcuip_prefetcher=vp_dcuip_prefetcher,
            vp_adjacent_cache_line_prefetcher=
                vp_adjacent_cache_line_prefetcher,
            vp_hardware_prefetcher=vp_hardware_prefetcher,
            vp_dcu_streamer_prefetch=vp_dcu_streamer_prefetch)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_direct_cache_access(handle, name, parent_org_dn,
                                  vp_direct_cache_access="platform-default"):
    """
    This method configures direct cache access option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_direct_cache_access : "platform-default","disabled", "enabled"

    Returns:
        BiosVfDirectCacheAccess: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_direct_cache_access(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_direct_cache_access="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfDirectCacheAccess import \
        BiosVfDirectCacheAccess

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDirectCacheAccess(
            parent_mo_or_dn=obj,
            vp_direct_cache_access=vp_direct_cache_access)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c_state(handle, name, parent_org_dn,
                                vp_processor_c_state="platform-default"):
    """
    This method configures processor C state option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_c_state : "platform-default","disabled", "enabled"

    Returns:
        BiosVfProcessorCState: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_c_state(handle,name="sample_bios",
                                    parent_dn="org-root/org-sample",
                                    vp_processor_c_state="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorCState import BiosVfProcessorCState

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorCState(parent_mo_or_dn=obj,
                                   vp_processor_c_state=vp_processor_c_state)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c1_e(handle, name, parent_org_dn,
                             vp_processor_c1_e="platform-default"):
    """
    This method configures processor C1 option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_c1_e : "platform-default","disabled", "enabled"

    Returns:
        BiosVfProcessorC1E: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_c1_e(handle,name="sample_bios",
                                parent_dn="org-root/org-sample",
                                vp_processor_c1_e="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorC1E import BiosVfProcessorC1E

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC1E(parent_mo_or_dn=obj,
                                vp_processor_c1_e=vp_processor_c1_e)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c3_report(handle, name, parent_org_dn,
                                  vp_processor_c3_report="platform-default"):
    """
    This method configures processor C3 report option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_c3_report : "acpi-c2", "acpi-c3","platform-default",
                                "disabled", "enabled"

    Returns:
        BiosVfProcessorC3Report: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_c3_report(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_processor_c3_report="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorC3Report import \
        BiosVfProcessorC3Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC3Report(
            parent_mo_or_dn=obj,
            vp_processor_c3_report=vp_processor_c3_report)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c6_report(handle, name, parent_org_dn,
                                  vp_processor_c6_report="platform-default"):
    """
    This method configures processor C6 report option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_c6_report : "platform-default","disabled", "enabled"

    Returns:
        BiosVfProcessorC6Report: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_c6_report(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_processor_c6_report="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorC6Report import \
        BiosVfProcessorC6Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC6Report(
            parent_mo_or_dn=obj, vp_processor_c6_report=vp_processor_c6_report)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c7_report(handle, name, parent_org_dn,
                                  vp_processor_c7_report="platform-default"):
    """
    This method configures processor C7 report option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_c7_report : "platform-default","disabled", "enabled"

    Returns:
        BiosVfProcessorC7Report: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_c7_report(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_processor_c7_report="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorC7Report import \
        BiosVfProcessorC7Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC7Report(
            parent_mo_or_dn=obj, vp_processor_c7_report=vp_processor_c7_report)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_cpu_performance(handle, name, parent_org_dn,
                              vp_cpu_performance="platform-default"):
    """
    This method configures CPU preformance option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_cpu_performance : "platform-default","custom", "enterprise",
                            "high-throughput"

    Returns:
        BiosVfCPUPerformance: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_cpu_performance(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_cpu_performance="higt-throughput")
    """

    from ucsmsdk.mometa.bios.BiosVfCPUPerformance import BiosVfCPUPerformance

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfCPUPerformance(parent_mo_or_dn=obj,
                                  vp_cpu_performance=vp_cpu_performance)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_max_variable_mtrr(handle, name, parent_org_dn,
                                vp_processor_mtrr="platform-default"):
    """
    This method configures max vrible MTRR option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_processor_mtrr : "8", "auto-max", "platform-default"

    Returns:
        BiosVfMaxVariableMTRRSetting: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_max_variable_mtrr(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_processor_mtrr="8")
    """

    from ucsmsdk.mometa.bios.BiosVfMaxVariableMTRRSetting import \
        BiosVfMaxVariableMTRRSetting

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=obj,
                                          vp_processor_mtrr=vp_processor_mtrr)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_local_x2_apic(handle, name, parent_org_dn,
                            vp_local_x2_apic="platform-default"):
    """
    This method configures local X2 apic option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_local_x2_apic : "x2apic", "xapic", "auto", "platform-default"

    Returns:
        BiosVfLocalX2Apic: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_local_x2_apic(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_local_x2_apic="auto")
    """

    from ucsmsdk.mometa.bios.BiosVfLocalX2Apic import BiosVfLocalX2Apic

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfLocalX2Apic(parent_mo_or_dn=obj,
                               vp_local_x2_apic=vp_local_x2_apic)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_energy(handle, name, parent_org_dn,
                               vp_power_technology="platform-default",
                               vp_energy_performance="platform-default"):
    """
    This method configures processor energy options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_power_technology : "custom", "disabled", "platform-default" etc
        vp_energy_performance : "balanced-performance","platform-default" etc

    Returns:
        BiosVfProcessorEnergyConfiguration: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_processor_energy(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_power_technology="performance")
    """

    from ucsmsdk.mometa.bios.BiosVfProcessorEnergyConfiguration import \
        BiosVfProcessorEnergyConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorEnergyConfiguration(
            parent_mo_or_dn=obj,
            vp_power_technology=vp_power_technology,
            vp_energy_performance=vp_energy_performance)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_frequency_floor_override(
        handle, name, parent_org_dn,
        vp_frequency_floor_override="platform-default"):
    """
    This method configures frequency override options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_frequency_floor_override : "enabled", "disabled", "platform-default"

    Returns:
        BiosVfFrequencyFloorOverride: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_frequency_floor_override(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_frequency_floor_override="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfFrequencyFloorOverride import \
        BiosVfFrequencyFloorOverride

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFrequencyFloorOverride(
            parent_mo_or_dn=obj,
            vp_frequency_floor_override=vp_frequency_floor_override)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_pstate_coordination(handle, name, parent_org_dn,
                                  vp_pstate_coordination="platform-default"):
    """
    This method configures P-State options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_pstate_coordination : "hw-all", "sw-all", "sw-any"
                                "platform-default"

    Returns:
        BiosVfPSTATECoordination: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_pstate_coordination(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_pstate_coordination="hw-all")
    """

    from ucsmsdk.mometa.bios.BiosVfPSTATECoordination import \
        BiosVfPSTATECoordination

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPSTATECoordination(
            parent_mo_or_dn=obj,
            vp_pstate_coordination=vp_pstate_coordination)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_dram_clock(handle, name, parent_org_dn,
                         vp_dram_clock_throttling="platform-default"):
    """
    This method configures D-RAM Clock option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_dram_clock_throttling : "auto", "balanced", "energy-efficient",etc

    Returns:
        BiosVfDRAMClockThrottling: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_dram_clock(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_dram_clock_throttling="performance")
    """

    from ucsmsdk.mometa.bios.BiosVfDRAMClockThrottling import \
        BiosVfDRAMClockThrottling

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDRAMClockThrottling(
            parent_mo_or_dn=obj,
            vp_dram_clock_throttling=vp_dram_clock_throttling)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_inter_leave(handle, name, parent_org_dn,
                          vp_channel_interleaving="platform-default",
                          vp_rank_interleaving="platform-default",
                          vp_memory_interleaving="platform-default"):
    """
    This method configures inter leave option of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_channel_interleaving : "1-way", "2-way", "3-way" etc
        vp_rank_interleaving : "1-way", "2-way", "4-way", etc
        vp_memory_interleaving : "2-way-node-interleave",
                                "4-way-node-interleave" etc
    Returns:
        BiosVfInterleaveConfiguration: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_inter_leave(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_rank_interleaving="1-way")
    """

    from ucsmsdk.mometa.bios.BiosVfInterleaveConfiguration import \
        BiosVfInterleaveConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfInterleaveConfiguration(
            parent_mo_or_dn=obj,
            vp_channel_interleaving=vp_channel_interleaving,
            vp_rank_interleaving=vp_rank_interleaving,
            vp_memory_interleaving=vp_memory_interleaving)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_scrub_policy(handle, name, parent_org_dn,
                           vp_patrol_scrub="platform-default",
                           vp_demand_scrub="platform-default"):
    """
    This method configures scrub policy options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_demand_scrub : "disabled", "enabled", "platform-default"
        vp_patrol_scrub : "disabled", "enabled", "platform-default"

    Returns:
        BiosVfScrubPolicies: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_scrub_policy(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_demand_scrub="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfScrubPolicies import BiosVfScrubPolicies

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfScrubPolicies(parent_mo_or_dn=obj,
                                 vp_patrol_scrub=vp_patrol_scrub,
                                 vp_demand_scrub=vp_demand_scrub)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_altitude(handle, name, parent_org_dn,
                       vp_altitude="platform-default"):
    """
    This method configures Altitude options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_altitude : "1500-m", "300-m", "platform-default", etc

    Returns:
        BiosVfAltitude: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_altitude(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_altitude="3000-m")
    """
    from ucsmsdk.mometa.bios.BiosVfAltitude import BiosVfAltitude

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAltitude(parent_mo_or_dn=obj, vp_altitude=vp_altitude)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_directed_io(
        handle, name, parent_org_dn,
        vp_intel_vtd_pass_through_dma_support="platform-default",
        vp_intel_vtdats_support="platform-default",
        vp_intel_vtd_interrupt_remapping="platform-default",
        vp_intel_vtd_coherency_support="platform-default",
        vp_intel_vt_for_directed_io="platform-default"):
    """
    This method configures Intel Directed I/O options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_intel_vtd_pass_through_dma_support : "disabled", "enabled",
                                                "platform-default"
        vp_intel_vtdats_support: "disabled", "enabled", "platform-default"
        vp_intel_vtd_interrupt_remapping: "disabled", "enabled",
                                          "platform-default"
        vp_intel_vtd_coherency_support: "disabled", "enabled",
                                        "platform-default"
        vp_intel_vt_for_directed_io: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfIntelVTForDirectedIO

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_intel_directed_io(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_intel_vtd_coherency_support="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelVTForDirectedIO import \
        BiosVfIntelVTForDirectedIO

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelVTForDirectedIO(
            parent_mo_or_dn=obj,
            vp_intel_vtd_pass_through_dma_support=
                vp_intel_vtd_pass_through_dma_support,
            vp_intel_vtdats_support=vp_intel_vtdats_support,
            vp_intel_vtd_interrupt_remapping=vp_intel_vtd_interrupt_remapping,
            vp_intel_vtd_coherency_support=vp_intel_vtd_coherency_support,
            vp_intel_vt_for_directed_io=vp_intel_vt_for_directed_io)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_ras_memory(
        handle, name, parent_org_dn,
        vp_select_memory_ras_configuration="platform-default"):
    """
    This method configures RAS memory options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_select_memory_ras_configuration: "lockstep", "mirroring"
                                            "platform-default", etc
    Returns:
        BiosVfSelectMemoryRASConfiguration: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_ras_memory(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_select_memory_ras_configuration="maximum-performance")
    """

    from ucsmsdk.mometa.bios.BiosVfSelectMemoryRASConfiguration import \
        BiosVfSelectMemoryRASConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfSelectMemoryRASConfiguration(
            parent_mo_or_dn=obj,
            vp_select_memory_ras_configuration=
                vp_select_memory_ras_configuration)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_numa_optimized(handle, name, parent_org_dn,
                             vp_numa_optimized="platfrom-default"):
    """
    This method configures NUMA options of Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_numa_optimized: "disabled", "enabled","platform-default"

    Returns:
        BiosVfNUMAOptimized: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_numa_optimized(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_numa_optimized="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfNUMAOptimized import BiosVfNUMAOptimized

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfNUMAOptimized(parent_mo_or_dn=obj,
                                 vp_numa_optimized=vp_numa_optimized)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_ddr_mode(handle, name, parent_org_dn,
                       vp_lv_ddr_mode="platform-default"):
    """
    This method configures DDR mode option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_lv_ddr_mode: "auto", "performance-mode",etc

    Returns:
        BiosVfLvDIMMSupport: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_ddr_mode(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_lv_ddr_mode="auto")
    """

    from ucsmsdk.mometa.bios.BiosVfLvDIMMSupport import BiosVfLvDIMMSupport

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfLvDIMMSupport(parent_mo_or_dn=obj,
                                 vp_lv_ddr_mode=vp_lv_ddr_mode)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_dram_refresh_rate(handle, name, parent_org_dn,
                                vp_dram_refresh_rate="platform-default"):
    """
    This method configures DRAM Refresh Rate option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_dram_refresh_rate : "1x", "2x", "3x",etc

    Returns:
        BiosVfDramRefreshRate: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_dram_refresh_rate(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_dram_refresh_rate="2x")
    """

    from ucsmsdk.mometa.bios.BiosVfDramRefreshRate import BiosVfDramRefreshRate

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDramRefreshRate(parent_mo_or_dn=obj,
                                   vp_dram_refresh_rate=vp_dram_refresh_rate)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_serial_port_a(handle, name, parent_org_dn,
                            vp_serial_port_a_enable="platform-default"):
    """
    This method configures Serial Port option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_serial_port_a_enable : "disabled", "enabled", "platform-default"

    Returns:
        BiosVfSerialPortAEnable: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_serial_port_a(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_serial_port_a_enable="2x")
    """

    from ucsmsdk.mometa.bios.BiosVfSerialPortAEnable import \
        BiosVfSerialPortAEnable

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfSerialPortAEnable(
            parent_mo_or_dn=obj,
            vp_serial_port_a_enable=vp_serial_port_a_enable)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_boot(handle, name, parent_org_dn,
                       vp_legacy_usb_support="platform-default",
                       vp_make_device_non_bootable="platform-default"):
    """
    This method configures USB boot option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_legacy_usb_support : "auto", "disabled", "enabled",
                                "platform-default"
        vp_make_device_non_bootable:  "disabled", "enabled", "platform-default"

    Returns:
        BiosVfUSBBootConfig: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_boot(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_legacy_usb_support="auto")
    """

    from ucsmsdk.mometa.bios.BiosVfUSBBootConfig import BiosVfUSBBootConfig

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBBootConfig(
            parent_mo_or_dn=obj,
            vp_legacy_usb_support=vp_legacy_usb_support,
            vp_make_device_non_bootable=vp_make_device_non_bootable)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_idle_power(handle, name, parent_org_dn,
                             vp_usb_idle_power_optimizing="platform-default"):
    """
    This method configures USB Idle power option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_usb_idle_power_optimizing : "high-performance",
                                        "lower-idle-power" etc
    Returns:
        BiosVfUSBSystemIdlePowerOptimizingSetting

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_idle_power(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_usb_idle_power_optimizing="high-performance")
    """

    from ucsmsdk.mometa.bios.BiosVfUSBSystemIdlePowerOptimizingSetting import \
        BiosVfUSBSystemIdlePowerOptimizingSetting

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBSystemIdlePowerOptimizingSetting(
            parent_mo_or_dn=obj,
            vp_usb_idle_power_optimizing=vp_usb_idle_power_optimizing)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_front_panel_lock(handle, name, parent_org_dn,
                                   vp_usb_front_panel_lock="platform-default"):
    """
    This method configures USB front panel lock option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_usb_front_panel_lock: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfUSBFrontPanelAccessLock: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_front_panel_lock(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_usb_front_panel_lock="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfUSBFrontPanelAccessLock import \
        BiosVfUSBFrontPanelAccessLock

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBFrontPanelAccessLock(
            parent_mo_or_dn=obj,
            vp_usb_front_panel_lock=vp_usb_front_panel_lock)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_port(handle, name, parent_org_dn,
                       vp_usb_port_front="platform-default",
                       vp_usb_port_v_media="platform-default",
                       vp_usb_port_kvm="platform-default",
                       vp_port6064_emulation="platform-default",
                       vp_usb_port_rear="platform-default",
                       vp_usb_port_internal="platform-default",
                       vp_usb_port_sd_card="platform-default"):
    """
    This method configures USB port option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_usb_port_front: "disabled", "enabled", "platform-default"
        vp_usb_port_v_media: "disabled", "enabled", "platform-default"
        vp_usb_port_kvm: "disabled", "enabled", "platform-default"
        vp_port6064_emulation: "disabled", "enabled", "platform-default"
        vp_usb_port_rear: "disabled", "enabled", "platform-default"
        vp_usb_port_internal: "disabled", "enabled", "platform-default"
        vp_usb_port_sd_card: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfUSBPortConfiguration: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_port(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_usb_port_front="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfUSBPortConfiguration import \
        BiosVfUSBPortConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBPortConfiguration(
            parent_mo_or_dn=obj,
            vp_usb_port_front=vp_usb_port_front,
            vp_usb_port_v_media=vp_usb_port_v_media,
            vp_usb_port_kvm=vp_usb_port_kvm,
            vp_port6064_emulation=vp_port6064_emulation,
            vp_usb_port_rear=vp_usb_port_rear,
            vp_usb_port_internal=vp_usb_port_internal,
            vp_usb_port_sd_card=vp_usb_port_sd_card)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_all(handle, name, parent_org_dn,
                      vp_all_usb_devices="platform-default"):
    """
    This method configures all USB option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_all_usb_devices : "disabled", "enabled", "platform-default"

    Returns:
        BiosVfAllUSBDevices: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_all(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_all_usb_devices="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfAllUSBDevices import BiosVfAllUSBDevices

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAllUSBDevices(parent_mo_or_dn=obj,
                                 vp_all_usb_devices=vp_all_usb_devices)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_vf(handle, name, parent_org_dn,
                     vp_xhci_mode="platform-default",
                     vp_legacy_usb_support="platform-default"):
    """
    This method configures USB VF option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_xhci_mode : "disabled", "enabled", "platform-default"
        vp_legacy_usb_support: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfUSBConfiguration: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_usb_vf(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_legacy_usb_support="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfUSBConfiguration import \
        BiosVfUSBConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBConfiguration(
            parent_mo_or_dn=obj,
            vp_xhci_mode=vp_xhci_mode,
            vp_legacy_usb_support=vp_legacy_usb_support)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_max_mem_below_4gb(
        handle, name, parent_org_dn,
        vp_maximum_memory_below4_gb="platform-default"):
    """
    This method configures Max memory below 4gb option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_maximum_memory_below4_gb: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfMaximumMemoryBelow4GB: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_max_mem_below_4gb(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_maximum_memory_below4_gb="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfMaximumMemoryBelow4GB import \
        BiosVfMaximumMemoryBelow4GB

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMaximumMemoryBelow4GB(
            parent_mo_or_dn=obj,
            vp_maximum_memory_below4_gb=vp_maximum_memory_below4_gb)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_mapped_mem_io(handle, name, parent_org_dn,
                            vp_memory_mapped_io_above4_gb="platform-defalut"):
    """
    This method configures mapped memory option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_memory_mapped_io_above4_gb: "disabled", "enabled",
                                        "platform-default"

    Returns:
        BiosVfMemoryMappedIOAbove4GB: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_mapped_mem_io(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_memory_mapped_io_above4_gb="disabled")
    """

    from ucsmsdk.mometa.bios.BiosVfMemoryMappedIOAbove4GB import \
        BiosVfMemoryMappedIOAbove4GB

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMemoryMappedIOAbove4GB(
            parent_mo_or_dn=obj,
            vp_memory_mapped_io_above4_gb=vp_memory_mapped_io_above4_gb)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_vga_priority(handle, name, parent_org_dn,
                           vp_vga_priority="platform-default"):
    """
    This method configures VGA priority option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_vga_priority: "offboard", "onboard", "platform-default", etc

    Returns:
        BiosVfVGAPriority: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_vga_priority(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_vga_priority="offboard")
    """

    from ucsmsdk.mometa.bios.BiosVfVGAPriority import BiosVfVGAPriority

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfVGAPriority(parent_mo_or_dn=obj,
                               vp_vga_priority=vp_vga_priority)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_qpi_link_frequency(
        handle, name, parent_org_dn,
        vp_qpi_link_frequency_select="platform-default"):
    """
    This method configures QPI link option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_qpi_link_frequency_select: "6400", "7200", "platform-default", etc

    Returns:
        BiosVfQPILinkFrequencySelect: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_qpi_link_frequency(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_qpi_link_frequency_select="7200")
    """

    from ucsmsdk.mometa.bios.BiosVfQPILinkFrequencySelect import \
        BiosVfQPILinkFrequencySelect

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQPILinkFrequencySelect(
            parent_mo_or_dn=obj,
            vp_qpi_link_frequency_select=vp_qpi_link_frequency_select)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_qpi_snoop_mode(handle, name, parent_org_dn,
                             vp_qpi_snoop_mode="platform-default"):
    """
    This method configures QPI Snoop option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_qpi_snoop_mode: "auto", "cluster-on-die", "early-snoop", etc

    Returns:
        BiosVfQPISnoopMode: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_qpi_snoop_mode(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_qpi_snoop_mode="home-snoop")
    """

    from ucsmsdk.mometa.bios.BiosVfQPISnoopMode import BiosVfQPISnoopMode

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQPISnoopMode(parent_mo_or_dn=obj,
                                vp_qpi_snoop_mode=vp_qpi_snoop_mode)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_rom_slot_option(
        handle, name, parent_org_dn,
        vp_slot3_state="platform-default",
        vp_slot4_state="platform-default",
        vp_slot1_state="platform-default",
        vp_pc_ie_slot_sas_option_rom="platform-default",
        vp_pc_ie_slot_hba_option_rom="platform-default",
        vp_slot6_state="platform-default",
        vp_slot9_state="platform-default",
        vp_pc_ie_slot_n2_option_rom="platform-default",
        vp_slot7_state="platform-default",
        vp_pc_ie_slot_n1_option_rom="platform-default",
        vp_slot8_state="platform-default",
        vp_slot2_state="platform-default",
        vp_slot5_state="platform-default",
        vp_slot10_state="platform-default",
        vp_pc_ie_slot_mlom_option_rom="platform-default"):
    """
    This method configures BiosVfPCISlotOptionROMEnable in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.

    Returns:
        BiosVfPCISlotOptionROMEnable: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_qpi_snoop_mode(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_qpi_snoop_mode="home-snoop")
    """

    from ucsmsdk.mometa.bios.BiosVfPCISlotOptionROMEnable import \
        BiosVfPCISlotOptionROMEnable

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPCISlotOptionROMEnable(
            parent_mo_or_dn=obj,
            vp_slot3_state=vp_slot3_state,
            vp_slot4_state=vp_slot4_state,
            vp_slot1_state=vp_slot1_state,
            vp_pc_ie_slot_sas_option_rom=vp_pc_ie_slot_sas_option_rom,
            vp_pc_ie_slot_hba_option_rom=vp_pc_ie_slot_hba_option_rom,
            vp_slot6_state=vp_slot6_state,
            vp_slot9_state=vp_slot9_state,
            vp_pc_ie_slot_n2_option_rom=vp_pc_ie_slot_n2_option_rom,
            vp_slot7_state=vp_slot7_state,
            vp_pc_ie_slot_n1_option_rom=vp_pc_ie_slot_n1_option_rom,
            vp_slot8_state=vp_slot8_state,
            vp_slot2_state=vp_slot2_state,
            vp_slot5_state=vp_slot5_state,
            vp_slot10_state=vp_slot10_state,
            vp_pc_ie_slot_mlom_option_rom=vp_pc_ie_slot_mlom_option_rom)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_trusted_platform(
        handle, name, parent_org_dn,
        vp_trusted_platform_module_support="platform-default"):
    """
    This method configures Trusted platform option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_trusted_platform_module_support: "enabled", "disabled"

    Returns:
        BiosVfTrustedPlatformModule: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_trusted_platform(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_trusted_platform_module_support="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfTrustedPlatformModule import \
        BiosVfTrustedPlatformModule

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfTrustedPlatformModule(
            parent_mo_or_dn=obj,
            vp_trusted_platform_module_support=
                vp_trusted_platform_module_support)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_trusted_execution(
        handle, name, parent_org_dn,
        vp_intel_trusted_execution_technology_support="platform-default"):
    """
    This method configures Trusted execution option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_trusted_platform_module_support: "enabled", "disabled"

    Returns:
        BiosVfIntelTrustedExecutionTechnology: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_trusted_platform(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_intel_trusted_execution_technology_support="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelTrustedExecutionTechnology import \
        BiosVfIntelTrustedExecutionTechnology

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelTrustedExecutionTechnology(
            parent_mo_or_dn=obj,
            vp_intel_trusted_execution_technology_support=
                vp_intel_trusted_execution_technology_support)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_option_retry(handle, name, parent_org_dn,
                                vp_boot_option_retry="platform-default"):
    """
    This method configures Boot retry option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_boot_option_retry: "enabled", "disabled"

    Returns:
        BiosVfBootOptionRetry: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_boot_option_retry(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_boot_option_retry="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfBootOptionRetry import BiosVfBootOptionRetry

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfBootOptionRetry(parent_mo_or_dn=obj,
                                   vp_boot_option_retry=vp_boot_option_retry)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_sas_raid(handle, name, parent_org_dn,
                             vp_sasraid="platform-default",
                             vp_sasraid_module="platform-default"):
    """
    This method configures SAS Raid option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_sasraid: "enabled", "disabled"
        vp_sasraid_module: "intel-esrtii", "it-ir-raid",etc

    Returns:
        BiosVfIntelEntrySASRAIDModule: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_intel_sas_raid(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_sasraid="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfIntelEntrySASRAIDModule import \
        BiosVfIntelEntrySASRAIDModule

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelEntrySASRAIDModule(parent_mo_or_dn=obj,
                                           vp_sasraid=vp_sasraid,
                                           vp_sasraid_module=vp_sasraid_module)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_onboard_scu__storage(
        handle, name, parent_org_dn,
        vp_onboard_scu_storage_support="platform-default"):
    """
    This method configures SAS Raid option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_onboard_scu_storage_support: "enabled", "disabled"

    Returns:
        BiosVfOnboardStorage: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_onboard_scu_storage(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_onboard_scu_storage_support="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfOnboardStorage import BiosVfOnboardStorage

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOnboardStorage(
            parent_mo_or_dn=obj,
            vp_onboard_scu_storage_support=vp_onboard_scu_storage_support)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_assert_nmi_serr(handle, name, parent_org_dn,
                              vp_assert_nmi_on_serr="platform-default"):
    """
    This method configures NMI SERR assert ption in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_assert_nmi_on_serr: "enabled", "disabled"

    Returns:
        BiosVfAssertNMIOnSERR: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_assert_nmi_serr(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_assert_nmi_on_serr="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfAssertNMIOnSERR import BiosVfAssertNMIOnSERR

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAssertNMIOnSERR(parent_mo_or_dn=obj,
                                   vp_assert_nmi_on_serr=vp_assert_nmi_on_serr)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_assert_nmi_perr(handle, name, parent_org_dn,
                              vp_assert_nmi_on_perr="platform-default"):
    """
    This method configures NMI PERR assert ption in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_assert_nmi_on_perr: "enabled", "disabled"

    Returns:
        BiosVfAssertNMIOnPERR: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_assert_nmi_perr(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_assert_nmi_on_perr="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfAssertNMIOnPERR import BiosVfAssertNMIOnPERR

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAssertNMIOnPERR(parent_mo_or_dn=obj,
                                   vp_assert_nmi_on_perr=vp_assert_nmi_on_perr)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer(
        handle, name, parent_org_dn,
        vp_os_boot_watchdog_timer="platform-default"):
    """
    This method configures watchdog timer option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_os_boot_watchdog_timer: "enabled", "disabled"

    Returns:
        BiosVfOSBootWatchdogTimer: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_boot_watchdog_timer(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_os_boot_watchdog_timer="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimer import \
        BiosVfOSBootWatchdogTimer

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimer(
            parent_mo_or_dn=obj,
            vp_os_boot_watchdog_timer=vp_os_boot_watchdog_timer)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer_policy(
        handle, name, parent_org_dn,
        vp_os_boot_watchdog_timer_policy="platform-default"):
    """
    This method configures watchdog timer policy option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_os_boot_watchdog_timer_policy: "power-off", "reset",
                                            "platform-default"
    Returns:
        BiosVfOSBootWatchdogTimerPolicy: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_boot_watchdog_timer_policy(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_os_boot_watchdog_timer_policy="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerPolicy import \
        BiosVfOSBootWatchdogTimerPolicy

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimerPolicy(
            parent_mo_or_dn=obj,
            vp_os_boot_watchdog_timer_policy=vp_os_boot_watchdog_timer_policy)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer_timeout(
        handle, name, parent_org_dn,
        vp_os_boot_watchdog_timer_timeout="platform-default"):
    """
    This method configures watchdog timer policy option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_os_boot_watchdog_timer_timeout: "10-minutes", "15-minutes",
                                            "platform-default",etc
    Returns:
        BiosVfOSBootWatchdogTimerTimeout: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_boot_watchdog_timer_timeout(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_os_boot_watchdog_timer_timeout="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerTimeout import \
        BiosVfOSBootWatchdogTimerTimeout

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimerTimeout(
            parent_mo_or_dn=obj,
            vp_os_boot_watchdog_timer_timeout=
                vp_os_boot_watchdog_timer_timeout)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)


def bios_conf_fr_b2_timer(handle, name, parent_org_dn,
                          vp_fr_b2_timer="platform-default"):
    """
    This method configures watchdog timer policy option in Bios Policy.

    Args:
        handle (UcsHandle)
        parent_org_dn (string): Dn of parent Org.
        name (string): Name of Bios policy.
        vp_fr_b2_timer: "disabled", "enabled", "platform-default"

    Returns:
        BiosVfFRB2Timer: Managed Object

    Raises:
        ValueError: If BiosVProfile is not present

    Example:
        bios_conf_fr_b2_timer(handle,name="sample_bios",
                    parent_dn="org-root/org-sample",
                    vp_fr_b2_timer="enabled")
    """

    from ucsmsdk.mometa.bios.BiosVfFRB2Timer import BiosVfFRB2Timer

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFRB2Timer(parent_mo_or_dn=obj,
                             vp_fr_b2_timer=vp_fr_b2_timer)
        handle.add_mo(mo, True)
        handle.commit()
        return mo
    else:
        raise ValueError("Bios policy '%s' not found." % profile_dn)
