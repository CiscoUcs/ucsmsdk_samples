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


import time
import datetime
import logging
log = logging.getLogger('ucs')

from ucsmsdk.ucseventhandler import UcsEventHandle
from ucsmsdk.mometa.ls.LsServer import LsServerConsts

# TODO: should not be global. This will not work when multiple nodes are associate in parallel
end_script = False


# ###########################################
# Service Profile Association
# ###########################################


def _sp_associate_callback(mce):
    global end_script
    if mce.mo.assoc_state == LsServerConsts.ASSOC_STATE_ASSOCIATED:
        log.debug("SP:" + mce.mo.dn + " Assoc Successful. assoc_state: " +
               mce.mo.assoc_state)
    elif mce.mo.assoc_state == LsServerConsts.ASSIGN_STATE_FAILED:
        log.error("SP:" + mce.mo.dn + " Assoc Failed. assoc_state: " +
               mce.mo.assoc_state)
    end_script = True



def _sp_associate_monitor(event_handle, mo): event_handle.add(managed_object=mo, prop="assoc_state",
                     success_value=[LsServerConsts.ASSOC_STATE_ASSOCIATED],
                     failure_value=[LsServerConsts.ASSOC_STATE_FAILED],
                     timeout_sec=600, call_back=_sp_associate_callback)

# #########################################################################
# Wait until the specified physical server has completed the association FSM
# Return an error if the Service Profile has a config error
#
def wait_assoc_completion(handle, sp_dn, server_dn, assoc_completion_timeout=20*60):
	start = datetime.datetime.now()
	# TODO: This event handle does not work for me....
	# add a watch on sp
	#event_handle = UcsEventHandle(handle)
	#_sp_associate_monitor(event_handle=event_handle, mo=sp)

	sp_mo = handle.query_dn(sp_dn)
	if sp_mo == None:
		raise Exception("Service Profile %s does not exist", sp_dn)
	if sp_mo.config_state == 'failed-to-apply':
		log.debug("Service Profile %s has config failure: %s", sp_dn, sp_mo.config_qualifier)
		ls_issues = handle.query_dn(sp_dn + "/config-issue")
		qualifier = sp_mo.config_qualifier
		if ls_issues:
			qualifier = ""
			if ls_issues.iscsi_config_issues:
				qualifier = qualifier + "iSCSI: " + ls_issues.iscsi_config_issues
			if ls_issues.network_config_issues:
				if len(qualifier) > 0 : qualifier = qualifier  + ". "
				qualifier = qualifier + "Network: " + ls_issues.network_config_issues
			if ls_issues.server_config_issues:
				if len(qualifier) > 0 : qualifier = qualifier  + ". "
				qualifier = qualifier + "Server: " + ls_issues.server_config_issues
			if ls_issues.storage_config_issues:
				if len(qualifier) > 0 : qualifier = qualifier  + ". "
				qualifier = qualifier + "Storage: " + ls_issues.storage_config_issues
			if ls_issues.vnic_config_issues:
				if len(qualifier) > 0 : qualifier = qualifier  + ". "
				qualifier = qualifier + "vNIC: " + ls_issues.vnic_config_issues

		raise Exception("Service Profile %s config failure: %s qualifier: %s" %
				(sp_mo.name, sp_mo.config_state, qualifier))
	physMo = handle.query_dn(server_dn)
	if physMo == None:
		raise Exception("Server %s does not exist" % sp_dn)
	while physMo.association != 'associated':
		time.sleep(10)
		if (datetime.datetime.now() - start).total_seconds() > assoc_completion_timeout:
			log.error('Server %s has not completed association', server_dn)
			break
		log.debug('Server %s fsmStatus: %s, elapsed=%ds', server_dn, physMo.fsm_status, 
			(datetime.datetime.now() - start).total_seconds())
		# Query again to update association state
		physMo = handle.query_dn(server_dn)

	if physMo.association == 'associated':
		log.debug('Server %s has completed association in %d seconds',
				server_dn, (datetime.datetime.now() - start).total_seconds())	

def sp_associate(handle, sp_dn, server_dn, wait_for_assoc_completion=True, assoc_completion_timeout=20*60):

    from ucsmsdk.mometa.ls.LsBinding import LsBinding

    # check if sp exists
    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("Service profile '%s' does not exist." % sp_dn)

    # check if dn exists
    blade = handle.query_dn(server_dn)
    if blade is None:
        raise ValueError("Server '%s' does not exist." % server_dn)

    # check if sp is already associated with blade
    if sp.assoc_state == LsServerConsts.ASSOC_STATE_ASSOCIATED \
            and sp.pn_dn == server_dn:
        raise ValueError("Service Profile is already associated with Server %s" % (server_dn))

    # check if sp already has lsBinding with blade
    binding = handle.query_dn(sp_dn + "/pn")
    if binding is not None and binding.pn_dn == server_dn:
        raise ValueError("Service Profile is already administratively associated with Server %s" % (server_dn))

    mo = LsBinding(parent_mo_or_dn=sp_dn, pn_dn=server_dn,
                   restrict_migration="no")
    handle.add_mo(mo, modify_present=True)
    handle.commit()

    if wait_for_assoc_completion:
		wait_assoc_completion(handle, sp_dn=sp_dn, server_dn=server_dn, assoc_completion_timeout=assoc_completion_timeout)

# ###########################################
# Service Profile Dissociation
# ###########################################

def _sp_disassociate_callback(mce):
    global end_script
    if mce.mo.assoc_state == LsServerConsts.ASSOC_STATE_UNASSOCIATED:
        print("SP:" + mce.mo.dn + " Assoc Successful. assoc_state: " +
               mce.mo.assoc_state)
    elif mce.mo.assoc_state == LsServerConsts.ASSIGN_STATE_FAILED:
        print("SP:" + mce.mo.dn + " Assoc Failed. assoc_state: " +
               mce.mo.assoc_state)
    end_script = True


def _sp_disassociate_monitor(event_handle, mo):
    event_handle.add(managed_object=mo,
                     prop="assoc_state",
                     success_value=[LsServerConsts.ASSOC_STATE_UNASSOCIATED],
                     failure_value=[LsServerConsts.ASSOC_STATE_FAILED],
                     timeout_sec=600,
                     call_back=_sp_disassociate_callback)


def sp_disassociate(handle, sp_dn):

    # check if sp exists
    sp = handle.query_dn(sp_dn)
    if sp is None:
        raise ValueError("Service profile '%s' does not exist." % sp_dn)

    dn = sp.dn + "/pn"
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Service Profile '%s' already dissociated." % dn)

    handle.remove_mo(mo)
    handle.commit()

    # add a watch on sp
    event_handle = UcsEventHandle(handle)
    _sp_disassociate_monitor(event_handle=event_handle, mo=sp)

    while not end_script:
        time.sleep(1)
	event_handle.cleanup()




