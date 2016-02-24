
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
import time
log = logging.getLogger('ucs')

def get_cimc_addresses(handle, phys_mo):
	log.debug('Get CIMC management IP addresses')
	from ucsmsdk.mometa.vnic.VnicIpV4PooledAddr import VnicIpV4PooledAddr
	mos = handle.query_children(in_mo=phys_mo, class_id="MgmtController", hierarchy=True)
	bmc_addrs = []

	# IP v4 addresses
	ipv4AddrSet = [x for x in mos if x._class_id == 'VnicIpV4PooledAddr' or
									x._class_id == 'VnicIpV4MgmtPooledAddr' or
									x._class_id == 'VnicIpV4ProfDerivedAddr' or
									x._class_id == 'VnicIpV4StaticAddr']
	for mo in ipv4AddrSet:
		if mo._class_id == 'VnicIpV4MgmtPooledAddr':
			access = 'in-band'
		else:
			access = 'oob'
		if mo.addr != '0.0.0.0':
			addr = {'addr': mo.addr, 'version': 4, 'access': access}
			log.debug("CIMC IP address: dn=%s, addr=%s, class=%s, access=%s",
				mo.dn, mo.addr, mo._class_id, access)
			bmc_addrs.append(addr)

	# IP v6 addresses
	ipv6AddrSet = [x for x in mos if x._class_id  == 'VnicIpV6MgmtPooledAddr' or
									x._class_id == 'VnicIpV6MgmtPooledAddr' or
									x._class_id == 'VnicIpV6StaticAddr']
	for mo in ipv6AddrSet:
		if mo.addr != '::':
			log.debug("CIMC IP address: dn=%s, addr=%s, class=%s",
				mo.dn, mo.addr, mo._class_id)
			if mo._class_id == 'VnicIpV6MgmtPooledAddr':
				access = 'in-band'
			else:
				access = 'oob'
			addr = {'addr': mo.addr, 'version': 6, 'access':access}
			log.debug("Server %s. CIMC address: %s, access: %s", phys_mo.dn, mo.addr, access)
			bmc_addrs.append(addr)
	return bmc_addrs

def is_reachable(hostname, retries=10):
	import os
	for retry in range (1, retries):
		ret = os.system("ping -c1 -w2 " + hostname + " > /dev/null 2>&1")
		if ret == 0:
			return True
		time.sleep(1)
	return False

def set_inband_profile(handle, vlan_name, ip_pool_name, vlan_group_name):
    """
    Configures CIMC inband profile

    Args:
        handle (UcsHandle)
		vlan_name(string): the name of the VLAN used for inband CIMC connectivity
		ip_pool_name(string): the name of the IP pool used to assign inband IP addresses to CIMC
		vlan_group_name(string): the name of the VLAN group used for CIMC connectivity

    Returns:
        MgmtInbandProfile: Managed object

    Raises:
        ValueError: If Inband profile does not exist

    Example:
        mo = set_inband_profile(handle=handle, vlan_name="inband_vlan", ip_pool_name="inband-ip-pool", vlan_group_name="inband-group")
    """
    from ucsmsdk.mometa.mgmt.MgmtInbandProfile import MgmtInbandProfile

    inband_profile_dn = "fabric/lan/ib-profile"
    mo = handle.query_dn(inband_profile_dn)
    if mo is None:
        raise ValueError("Inband Profile '%s' does not exist" % inband_profile_dn)

    mo.default_vlan_name = vlan_name
    mo.pool_name = ip_pool_name
    mo.name = vlan_group_name

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo

