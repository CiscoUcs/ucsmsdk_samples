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

import logging
log = logging.getLogger('ucs')


def bios_create(handle,parent_org_dn,name, descr="",
                reboot_on_update="no",
                vp_cdn_control="platform-default",
                vp_front_panel_lockout="platform-default",
                vp_post_error_pause="platform-default",
                vp_quiet_boot="platform-default",
                vp_resume_on_ac_power_loss="platform-default"):

    from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
    from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import \
        BiosVfConsistentDeviceNameControl
    from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import \
        BiosVfFrontPanelLockout
    from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
    from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
    from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import \
        BiosVfResumeOnACPowerLoss

    mo = BiosVProfile(parent_mo_or_dn=parent_org_dn,
                      name=name, descr=descr, reboot_on_update=reboot_on_update)
    mo_1 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo,
                                             vp_cdn_control=vp_cdn_control)
    mo_2 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo,
                                   vp_front_panel_lockout=vp_front_panel_lockout)
    mo_3 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo,
                                vp_post_error_pause=vp_post_error_pause)
    mo_4 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot=vp_quiet_boot)
    mo_5 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo,
                                     vp_resume_on_ac_power_loss=
                                     vp_resume_on_ac_power_loss)
    handle.add_mo(mo)
    handle.commit()


def bios_remove(handle,name,parent_org_dn):
    profile_dn = parent_org_dn + "/bios-prof-" + name
    mo = handle.query_dn(profile_dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found.Nothing to remove" % parent_org_dn)


def bios_conf_quite_boot(handle, name, parent_org_dn,
                              vp_quite_boot="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQuietBoot(parent_mo_or_dn=obj, vp_quiet_boot=vp_quite_boot)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_error_pause(handle, name, parent_org_dn,
                          vp_post_error_pause="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPOSTErrorPause(parent_mo_or_dn=obj,
                              vp_post_error_pause=vp_post_error_pause)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_power_loss(handle, name, parent_org_dn,
                         vp_resume_on_ac_power_loss="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import \
        BiosVfResumeOnACPowerLoss
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=obj,
                                       vp_resume_on_ac_power_loss=
                                       vp_resume_on_ac_power_loss)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_front_panel_lockout(handle, name, parent_org_dn,
                                  vp_front_panel_lockout="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import \
        BiosVfFrontPanelLockout

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFrontPanelLockout(parent_mo_or_dn=obj,
                                     vp_front_panel_lockout=vp_front_panel_lockout)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)

def bios_conf_device_name_control(handle, name, parent_org_dn,
                                  vp_cdn_control="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import \
       BiosVfConsistentDeviceNameControl

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=obj,
                                               vp_cdn_control=vp_cdn_control)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_turbo_boost(handle, name, parent_org_dn,
                          vp_intel_turbo_boost_tech="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfIntelTurboBoostTech import\
        BiosVfIntelTurboBoostTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelTurboBoostTech(parent_mo_or_dn=obj,
                                       vp_intel_turbo_boost_tech=
                                       vp_intel_turbo_boost_tech)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_speed_step(handle, name, parent_org_dn,
                               vp_enhanced_intel_speed_step_tech=
                               "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfEnhancedIntelSpeedStepTech import \
        BiosVfEnhancedIntelSpeedStepTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=obj,
                                              vp_enhanced_intel_speed_step_tech=
                                              vp_enhanced_intel_speed_step_tech)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_hyper_threading(handle, name, parent_org_dn,
                              vp_intel_hyper_threading_tech="platform-default"):

    from ucsmsdk.mometa.bios.BiosVfIntelHyperThreadingTech import \
        BiosVfIntelHyperThreadingTech

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=obj,
                                           vp_intel_hyper_threading_tech=
                                           vp_intel_hyper_threading_tech)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_core_multi_processing(handle, name, parent_org_dn,
                                    vp_core_multi_processing="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfCoreMultiProcessing import \
        BiosVfCoreMultiProcessing

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfCoreMultiProcessing(parent_mo_or_dn=obj,
                                       vp_core_multi_processing=
                                       vp_core_multi_processing)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_disable_bit(handle, name, parent_org_dn,
                          vp_execute_disable_bit="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfExecuteDisableBit import\
        BiosVfExecuteDisableBit

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfExecuteDisableBit(parent_mo_or_dn=obj,
                                     vp_execute_disable_bit=
                                     vp_execute_disable_bit)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_virtual_tech(handle, name, parent_org_dn,
                        vp_intel_virtualization_technology="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfIntelVirtualizationTechnology import \
        BiosVfIntelVirtualizationTechnology

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=obj,
                                                 vp_intel_virtualization_technology=
                                                 vp_intel_virtualization_technology)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_prefetch(handle, name, parent_org_dn,
                                 vp_dcuip_prefetcher="platform-default",
                                 vp_adjacent_cache_line_prefetcher=
                                 "platform-default",
                                 vp_hardware_prefetcher="platform-default",
                                 vp_dcu_streamer_prefetch="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfProcessorPrefetchConfig import \
        BiosVfProcessorPrefetchConfig

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=obj,
                                           vp_dcuip_prefetcher=
                                           vp_dcuip_prefetcher,
                                           vp_adjacent_cache_line_prefetcher=
                                           vp_adjacent_cache_line_prefetcher,
                                           vp_hardware_prefetcher=
                                           vp_hardware_prefetcher,
                                           vp_dcu_streamer_prefetch=
                                           vp_dcu_streamer_prefetch)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_direct_cache_access(handle, name, parent_org_dn,
                                  vp_direct_cache_access="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfDirectCacheAccess import \
        BiosVfDirectCacheAccess
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDirectCacheAccess(parent_mo_or_dn=obj,
                                     vp_direct_cache_access=
                                     vp_direct_cache_access)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c_state(handle, name, parent_org_dn,
                                vp_processor_c_state="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfProcessorCState import BiosVfProcessorCState
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorCState(parent_mo_or_dn=obj,
                                   vp_processor_c_state=vp_processor_c_state)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c1_e(handle, name, parent_org_dn,
                             vp_processor_c1_e="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfProcessorC1E import BiosVfProcessorC1E

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC1E(parent_mo_or_dn=obj,
                                vp_processor_c1_e=vp_processor_c1_e)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c3_report(handle, name, parent_org_dn,
                                  vp_processor_c3_report="platform-default"):

    from ucsmsdk.mometa.bios.BiosVfProcessorC3Report import \
        BiosVfProcessorC3Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC3Report(parent_mo_or_dn=obj,
                                     vp_processor_c3_report=
                                     vp_processor_c3_report)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c6_report(handle, name, parent_org_dn,
                                  vp_processor_c6_report="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfProcessorC6Report import \
        BiosVfProcessorC6Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC6Report(parent_mo_or_dn=obj,
                                     vp_processor_c6_report=
                                     vp_processor_c6_report)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_c7_report(handle, name, parent_org_dn,
                                  vp_processor_c7_report="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfProcessorC7Report import \
        BiosVfProcessorC7Report

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorC7Report(parent_mo_or_dn=obj,
                                     vp_processor_c7_report=
                                     vp_processor_c7_report)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_cpu_performance(handle, name, parent_org_dn,
                              vp_cpu_performance="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfCPUPerformance import BiosVfCPUPerformance

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfCPUPerformance(parent_mo_or_dn=obj,
                                  vp_cpu_performance=vp_cpu_performance)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_max_variable_mtrr(handle, name, parent_org_dn,
                                vp_processor_mtrr="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfMaxVariableMTRRSetting import \
        BiosVfMaxVariableMTRRSetting

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=obj,
                                          vp_processor_mtrr=vp_processor_mtrr)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_local_x2_apic(handle, name, parent_org_dn,
                            vp_local_x2_apic="platform-default"):

    from ucsmsdk.mometa.bios.BiosVfLocalX2Apic import BiosVfLocalX2Apic

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfLocalX2Apic(parent_mo_or_dn=obj,
                               vp_local_x2_apic=vp_local_x2_apic)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_processor_energy(handle, name, parent_org_dn,
                               vp_power_technology="platform-default",
                               vp_energy_performance="platform-default"):

    from ucsmsdk.mometa.bios.BiosVfProcessorEnergyConfiguration import \
        BiosVfProcessorEnergyConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=obj,
                                                vp_power_technology=
                                                vp_power_technology,
                                                vp_energy_performance=
                                                vp_energy_performance)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_frequency_floor_override(handle, name, parent_org_dn,
                                       vp_frequency_floor_override=
                                       "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfFrequencyFloorOverride import \
        BiosVfFrequencyFloorOverride
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFrequencyFloorOverride(parent_mo_or_dn=obj,
                                         vp_frequency_floor_override=
                                         vp_frequency_floor_override)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_pstate_coordination(handle, name, parent_org_dn,
                                  vp_pstate_coordination="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfPSTATECoordination import \
        BiosVfPSTATECoordination

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPSTATECoordination(parent_mo_or_dn=obj,
                                      vp_pstate_coordination=vp_pstate_coordination)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_dram_clock(handle, name, parent_org_dn,
                         vp_dram_clock_throttling="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfDRAMClockThrottling import \
        BiosVfDRAMClockThrottling

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDRAMClockThrottling(parent_mo_or_dn=obj,
                                       vp_dram_clock_throttling=
                                       vp_dram_clock_throttling)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_inter_leave(handle, name, parent_org_dn,
                          vp_channel_interleaving="platform-default",
                          vp_rank_interleaving="platform-default",
                          vp_memory_interleaving="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfInterleaveConfiguration import \
        BiosVfInterleaveConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfInterleaveConfiguration(parent_mo_or_dn=obj,
                                           vp_channel_interleaving=vp_channel_interleaving,
                                           vp_rank_interleaving=vp_rank_interleaving,
                                           vp_memory_interleaving=vp_memory_interleaving)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_scrub_policy(handle, name, parent_org_dn,
                           vp_patrol_scrub="platform-default",
                           vp_demand_scrub="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfScrubPolicies import BiosVfScrubPolicies

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfScrubPolicies(parent_mo_or_dn=obj,
                                 vp_patrol_scrub=vp_patrol_scrub,
                                 vp_demand_scrub=vp_demand_scrub)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_altitude(handle, name, parent_org_dn,
                       vp_altitude="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfAltitude import BiosVfAltitude
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAltitude(parent_mo_or_dn=obj, vp_altitude=vp_altitude)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_directed_io(handle, name, parent_org_dn,
                                vp_intel_vtd_pass_through_dma_support="platform-default",
                                vp_intel_vtdats_support="platform-default",
                                vp_intel_vtd_interrupt_remapping="platform-default",
                                vp_intel_vtd_coherency_support="platform-default",
                                vp_intel_vt_for_directed_io="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfIntelVTForDirectedIO import \
        BiosVfIntelVTForDirectedIO
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelVTForDirectedIO(parent_mo_or_dn=obj,
                                        vp_intel_vtd_pass_through_dma_support=
                                        vp_intel_vtd_pass_through_dma_support,
                                        vp_intel_vtdats_support=vp_intel_vtdats_support,
                                        vp_intel_vtd_interrupt_remapping=
                                        vp_intel_vtd_interrupt_remapping,
                                        vp_intel_vtd_coherency_support=
                                        vp_intel_vtd_coherency_support,
                                        vp_intel_vt_for_directed_io=
                                        vp_intel_vt_for_directed_io)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_ras_memory(handle, name, parent_org_dn,
                         vp_select_memory_ras_configuration="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfSelectMemoryRASConfiguration import \
        BiosVfSelectMemoryRASConfiguration
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfSelectMemoryRASConfiguration(parent_mo_or_dn=obj,
                                                vp_select_memory_ras_configuration=vp_select_memory_ras_configuration)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_numa_optimized(handle, name, parent_org_dn,
                             vp_numa_optimized="platfrom-default"):
    from ucsmsdk.mometa.bios.BiosVfNUMAOptimized import BiosVfNUMAOptimized
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfNUMAOptimized(parent_mo_or_dn=obj,
                                 vp_numa_optimized=vp_numa_optimized)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_ddr_mode(handle, name, parent_org_dn,
                       vp_lv_ddr_mode="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfLvDIMMSupport import BiosVfLvDIMMSupport
    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfLvDIMMSupport(parent_mo_or_dn=obj,
                                 vp_lv_ddr_mode=vp_lv_ddr_mode)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_dram_refresh_rate(handle, name, parent_org_dn,
                                vp_dram_refresh_rate="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfDramRefreshRate import BiosVfDramRefreshRate

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfDramRefreshRate(parent_mo_or_dn=obj,
                                   vp_dram_refresh_rate=vp_dram_refresh_rate)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_serial_port_a(handle, name, parent_org_dn,
                            vp_serial_port_a_enable="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfSerialPortAEnable import \
        BiosVfSerialPortAEnable

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfSerialPortAEnable(parent_mo_or_dn=obj,
                                     vp_serial_port_a_enable=vp_serial_port_a_enable)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_boot(handle, name, parent_org_dn,
                       vp_legacy_usb_support="platform-default",
                       vp_make_device_non_bootable="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfUSBBootConfig import BiosVfUSBBootConfig

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBBootConfig(parent_mo_or_dn=obj,
                                 vp_legacy_usb_support=vp_legacy_usb_support,
                                 vp_make_device_non_bootable=vp_make_device_non_bootable)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_idle_power(handle, name, parent_org_dn,
                             vp_usb_idle_power_optimizing="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfUSBSystemIdlePowerOptimizingSetting import\
        BiosVfUSBSystemIdlePowerOptimizingSetting

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBSystemIdlePowerOptimizingSetting(parent_mo_or_dn=obj,
                                                       vp_usb_idle_power_optimizing=vp_usb_idle_power_optimizing)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_front_panel_lock(handle, name, parent_org_dn,
                                   vp_usb_front_panel_lock="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfUSBFrontPanelAccessLock import \
        BiosVfUSBFrontPanelAccessLock

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBFrontPanelAccessLock(parent_mo_or_dn=obj,
                                           vp_usb_front_panel_lock=vp_usb_front_panel_lock)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_port(handle, name, parent_org_dn,
                       vp_usb_port_front="platform-default",
                       vp_usb_port_v_media="platform-default",
                       vp_usb_port_kvm="platform-default",
                       vp_port6064_emulation="platform-default",
                       vp_usb_port_rear="platform-default",
                       vp_usb_port_internal="platform-default",
                       vp_usb_port_sd_card="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfUSBPortConfiguration import \
        BiosVfUSBPortConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBPortConfiguration(parent_mo_or_dn=obj,
                                        vp_usb_port_front=vp_usb_port_front,
                                        vp_usb_port_v_media=vp_usb_port_v_media,
                                        vp_usb_port_kvm=vp_usb_port_kvm,
                                        vp_port6064_emulation=vp_port6064_emulation,
                                        vp_usb_port_rear=vp_usb_port_rear,
                                        vp_usb_port_internal=vp_usb_port_internal,
                                        vp_usb_port_sd_card=vp_usb_port_sd_card)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_ucs_all(handle, name, parent_org_dn,
                      vp_all_usb_devices="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfAllUSBDevices import BiosVfAllUSBDevices

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAllUSBDevices(parent_mo_or_dn=obj,
                                 vp_all_usb_devices=vp_all_usb_devices)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_usb_vf(handle, name, parent_org_dn,
                     vp_xhci_mode="platform-default",
                     vp_legacy_usb_support="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfUSBConfiguration import \
        BiosVfUSBConfiguration

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfUSBConfiguration(parent_mo_or_dn=obj,
                                    vp_xhci_mode=vp_xhci_mode,
                                    vp_legacy_usb_support=vp_legacy_usb_support)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_max_mem_below_4gb(handle, name, parent_org_dn,
                                vp_maximum_memory_below4_gb="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfMaximumMemoryBelow4GB import \
        BiosVfMaximumMemoryBelow4GB

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMaximumMemoryBelow4GB(parent_mo_or_dn=obj,
                                         vp_maximum_memory_below4_gb=
                                         vp_maximum_memory_below4_gb)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_mapped_mem_io(handle, name, parent_org_dn,
                            vp_memory_mapped_io_above4_gb="platform-defalut"):
    from ucsmsdk.mometa.bios.BiosVfMemoryMappedIOAbove4GB import \
        BiosVfMemoryMappedIOAbove4GB

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfMemoryMappedIOAbove4GB(parent_mo_or_dn=obj,
                                          vp_memory_mapped_io_above4_gb=
                                          vp_memory_mapped_io_above4_gb)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_vga_priority(handle, name, parent_org_dn,
                           vp_vga_priority="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfVGAPriority import BiosVfVGAPriority

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfVGAPriority(parent_mo_or_dn=obj,
                               vp_vga_priority=vp_vga_priority)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_qpi_link_frequency(handle, name, parent_org_dn,
                                 vp_qpi_link_frequency_select="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfQPILinkFrequencySelect import \
        BiosVfQPILinkFrequencySelect

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQPILinkFrequencySelect(parent_mo_or_dn=obj,
                                          vp_qpi_link_frequency_select=
                                          vp_qpi_link_frequency_select)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_qpi_snoop_mode(handle, name, parent_org_dn,
                             vp_qpi_snoop_mode="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfQPISnoopMode import BiosVfQPISnoopMode

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfQPISnoopMode(parent_mo_or_dn=obj,
                                vp_qpi_snoop_mode=vp_qpi_snoop_mode)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_rom_slot_option(handle, name, parent_org_dn,
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
    from ucsmsdk.mometa.bios.BiosVfPCISlotOptionROMEnable import \
        BiosVfPCISlotOptionROMEnable

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfPCISlotOptionROMEnable(parent_mo_or_dn=obj,
                                          vp_slot3_state=vp_slot3_state,
                                          vp_slot4_state=vp_slot4_state,
                                          vp_slot1_state=vp_slot1_state,
                                          vp_pc_ie_slot_sas_option_rom=
                                          vp_pc_ie_slot_sas_option_rom,
                                          vp_pc_ie_slot_hba_option_rom=
                                          vp_pc_ie_slot_hba_option_rom,
                                          vp_slot6_state=vp_slot6_state,
                                          vp_slot9_state=vp_slot9_state,
                                          vp_pc_ie_slot_n2_option_rom=
                                          vp_pc_ie_slot_n2_option_rom,
                                          vp_slot7_state=vp_slot7_state,
                                          vp_pc_ie_slot_n1_option_rom=
                                          vp_pc_ie_slot_n1_option_rom,
                                          vp_slot8_state=vp_slot8_state,
                                          vp_slot2_state=vp_slot2_state,
                                          vp_slot5_state=vp_slot5_state,
                                          vp_slot10_state=vp_slot10_state,
                                          vp_pc_ie_slot_mlom_option_rom=
                                          vp_pc_ie_slot_mlom_option_rom)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_trusted_platform(handle, name, parent_org_dn,
                               vp_trusted_platform_module_support=
                               "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfTrustedPlatformModule import \
        BiosVfTrustedPlatformModule

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfTrustedPlatformModule(parent_mo_or_dn=obj,
                                         vp_trusted_platform_module_support=
                                         vp_trusted_platform_module_support)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_trusted_execution(handle, name, parent_org_dn,
                                vp_intel_trusted_execution_technology_support=
                                "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfIntelTrustedExecutionTechnology import \
        BiosVfIntelTrustedExecutionTechnology

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfIntelTrustedExecutionTechnology(parent_mo_or_dn=obj,
                                                   vp_intel_trusted_execution_technology_support=
                                                   vp_intel_trusted_execution_technology_support)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_option_retry(handle, name, parent_org_dn,
                                vp_boot_option_retry="platform-default"):

    from ucsmsdk.mometa.bios.BiosVfBootOptionRetry import BiosVfBootOptionRetry

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfBootOptionRetry(parent_mo_or_dn=obj,
                                   vp_boot_option_retry=vp_boot_option_retry)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_intel_sas_raid(handle, name, parent_org_dn,
                             vp_sasraid="platform-default",
                             vp_sasraid_module="platform-default"):
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
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_onboard_scu__storage(handle, name, parent_org_dn,
                                   vp_onboard_scu_storage_support=
                                   "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfOnboardStorage import BiosVfOnboardStorage

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOnboardStorage(parent_mo_or_dn=obj,
                                  vp_onboard_scu_storage_support=
                                  vp_onboard_scu_storage_support)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_assert_nmi_serr(handle, name, parent_org_dn,
                              vp_assert_nmi_on_serr="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfAssertNMIOnSERR import BiosVfAssertNMIOnSERR

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAssertNMIOnSERR(parent_mo_or_dn=obj,
                                   vp_assert_nmi_on_serr=vp_assert_nmi_on_serr)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_assert_nmi_perr(handle, name, parent_org_dn,
                              vp_assert_nmi_on_perr="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfAssertNMIOnPERR import BiosVfAssertNMIOnPERR

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfAssertNMIOnPERR(parent_mo_or_dn=obj,
                                   vp_assert_nmi_on_perr=vp_assert_nmi_on_perr)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer(handle, name, parent_org_dn,
                                  vp_os_boot_watchdog_timer="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimer import \
        BiosVfOSBootWatchdogTimer

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimer(parent_mo_or_dn=obj,
                                       vp_os_boot_watchdog_timer=
                                       vp_os_boot_watchdog_timer)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer_policy(handle, name, parent_org_dn,
                                         vp_os_boot_watchdog_timer_policy=
                                         "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerPolicy import \
        BiosVfOSBootWatchdogTimerPolicy

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimerPolicy(parent_mo_or_dn=obj,
                                             vp_os_boot_watchdog_timer_policy=
                                             vp_os_boot_watchdog_timer_policy)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_boot_watchdog_timer_timeout(handle, name, parent_org_dn,
                                          vp_os_boot_watchdog_timer_timeout=
                                          "platform-default"):
    from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerTimeout import \
        BiosVfOSBootWatchdogTimerTimeout

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfOSBootWatchdogTimerTimeout(parent_mo_or_dn=obj,
                                              vp_os_boot_watchdog_timer_timeout=
                                              vp_os_boot_watchdog_timer_timeout)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_fr_b2_timer(handle, name, parent_org_dn,
                          vp_fr_b2_timer="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfFRB2Timer import BiosVfFRB2Timer

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfFRB2Timer(parent_mo_or_dn=obj, vp_fr_b2_timer=vp_fr_b2_timer)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)


def bios_conf_console_redirection(handle, name, parent_org_dn,
                                  vp_terminal_type="platform-default",
                                  vp_flow_control="platform-default",
                                  vp_baud_rate="platform-default",
                                  vp_putty_key_pad="platform-default",
                                  vp_console_redirection="platform-default",
                                  vp_legacy_os_redirection="platform-default"):
    from ucsmsdk.mometa.bios.BiosVfConsoleRedirection import \
        BiosVfConsoleRedirection

    profile_dn = parent_org_dn + "/bios-prof-" + name
    obj = handle.query_dn(profile_dn)
    if obj:
        mo = BiosVfConsoleRedirection(parent_mo_or_dn=obj,
                                      vp_terminal_type=vp_terminal_type,
                                      vp_flow_control=vp_flow_control,
                                      vp_baud_rate=vp_baud_rate,
                                      vp_putty_key_pad=vp_putty_key_pad,
                                      vp_console_redirection=
                                      vp_console_redirection,
                                      vp_legacy_os_redirection=
                                      vp_legacy_os_redirection)
        handle.add_mo(mo, True)
        handle.commit()
    else:
        log.info("Bios policy '%s' not found." % profile_dn)