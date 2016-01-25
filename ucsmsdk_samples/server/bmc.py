
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

def get_cimc_addresses(handle, physMos):
	log.debug('Get CIMC management IP addresses')
	from ucsmsdk.mometa.vnic.VnicIpV4PooledAddr import VnicIpV4PooledAddr
	bmcMap = {} 
	for physMo in physMos:
		mos = handle.query_children(in_mo=physMo, class_id="MgmtController", hierarchy=True)
		bmcAddrs = []
		bmcMap[physMo.dn] = bmcAddrs
		ipv4AddrSet = [x for x in mos if x._class_id == 'VnicIpV4PooledAddr' or
										x._class_id == 'VnicIpV4MgmtPooledAddr' or
										x._class_id == 'VnicIpV4StaticAddr']
		for mo in ipv4AddrSet:
			if mo._class_id == 'VnicIpV4MgmtPooledAddr':
				access = 'in-band'
			else:
				access = 'oob'
			addr = {'addr': mo.addr, 'version': 4, 'access': access}
			bmcAddrs.append(addr)
		ipv6AddrSet = [x for x in mos if x._class_id  == 'VnicIpV6MgmtPooledAddr' or
										x._class_id == 'VnicIpV6MgmtPooledAddr' or
										x._class_id == 'VnicIpV6StaticAddr']
		for mo in ipv6AddrSet:
			if mo.addr != '::':
				if mo._class_id == 'VnicIpV6MgmtPooledAddr':
					access = 'in-band'
				else:
					access = 'oob'
				addr = {'addr': mo.addr, 'version': 6, 'access':access}
				bmcAddrs.append(addr)
		log.debug("cimc addresses: %s: %s", physMo.dn, bmcAddrs)
	return bmcMap

def is_reachable(hostname):
	import os
	ret = os.system("ping -c1 -w2 " + hostname + " > /dev/null 2>&1")
	if ret == 0:
		return True
	else:
		return False

