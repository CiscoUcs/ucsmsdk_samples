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



def domain_serials(handle):
    """
    This function will query all of the models and serial numbers from the ucs domain

    Args:
        handle (UcsHandle)
    
    Returns:
        Dictionary of dn, model, and serial for chassis, interconnects, and blades

    Raises:
        None

    Example:
        domain_serials(handle)
    """
    
    query_dict = {}
    query_dict['chassis'] = {}
    query_dict['fi'] = {}
    query_dict['blade'] = {}

    query_data = handle.query_classids('orgOrg', 'EquipmentChassis', 'NetworkElement', 'ComputeBlade')

    for chassis in query_data['EquipmentChassis']:
        query_dict['chassis'][chassis.dn] = {}
        query_dict['chassis'][chassis.dn]['model'] = chassis.model
        query_dict['chassis'][chassis.dn]['serial'] = chassis.serial

    for fi in query_data['NetworkElement']:
        query_dict['fi'][fi.dn] = {}
        query_dict['fi'][fi.dn]['model'] = fi.model
        query_dict['fi'][fi.dn]['serial'] = fi.serial

    for blade in query_data['ComputeBlade']:
        query_dict['blade'][blade.dn] = {}
        query_dict['blade'][blade.dn]['model'] = blade.model
        query_dict['blade'][blade.dn]['serial'] = blade.serial

    return query_dict