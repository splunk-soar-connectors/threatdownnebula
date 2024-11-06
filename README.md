[comment]: # "Auto-generated SOAR connector documentation"
# ThreatDown Nebula

Publisher: ThreatDown  
Connector Version: 2.1.1  
Product Vendor: ThreatDown  
Product Name: Malwarebytes Endpoint Protection  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.2.2  

This app integrates with the ThreatDown (powered by Malwarebytes) Nebula platform to perform prevention, detection, remediation, and forensics endpoint management tasks

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) ThreatDown, 2019-2024"
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
## Authentication

The ThreatDown App uses the same Cloud console credential to authenticate and issue RESTful API
commands.

[![](img/threatdown_login.png)](img/threatdown_login.png)


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Malwarebytes Endpoint Protection asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**accountid** |  required  | string | ThreatDown Nebula Account ID
**clientid** |  required  | string | ThreatDown Nebula Client ID
**clientsecret** |  required  | password | ThreatDown Nebula Client Secret

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[scan and remediate](#action-scan-and-remediate) - Scan an endpoint and remediate threats found  
[scan and report](#action-scan-and-report) - Scan an endpoint and report threats found  
[isolate endpoint](#action-isolate-endpoint) - When threats are found, isolate a network, process, or desktop endpoint  
[isolate process](#action-isolate-process) - When threats are found, isolate a process endpoint  
[isolate network](#action-isolate-network) - Network Isolation on an endpoint when threats are found  
[isolate desktop](#action-isolate-desktop) - Desktop Isolation an endpoint when threats are found  
[deisolate endpoint](#action-deisolate-endpoint) - Deisolate endpoint after threats are removed  
[list endpoints](#action-list-endpoints) - List all the endpoints/sensors configured on the device  
[get endpoint info](#action-get-endpoint-info) - Get information about an endpoint  
[get scan info](#action-get-scan-info) - Get information about a scan job  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'scan and remediate'
Scan an endpoint and remediate threats found

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to scan and remediate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'scan and report'
Scan an endpoint and report threats found

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to scan and report | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'isolate endpoint'
When threats are found, isolate a network, process, or desktop endpoint

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to isolate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'isolate process'
When threats are found, isolate a process endpoint

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to isolate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'isolate network'
Network Isolation on an endpoint when threats are found

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to isolate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'isolate desktop'
Desktop Isolation an endpoint when threats are found

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to isolate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'deisolate endpoint'
Deisolate endpoint after threats are removed

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of endpoint to deisolate | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'list endpoints'
List all the endpoints/sensors configured on the device

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.data.\*.machines.\*.created_at | string |  |   2018-10-19T17:59:32.877626Z 
action_result.data.\*.machines.\*.id | string |  |   9c3999cb-bdd0-4b01-b7f3-42a2f17ec429 
action_result.data.\*.machines.\*.last_seen_at | string |  |   2018-11-05T05:23:18.615218Z 
action_result.data.\*.machines.\*.name | string |  |   test 
action_result.data.\*.machines.\*.online | boolean |  |   True  False 
action_result.data.\*.machines.\*.os_architecture | string |  |   AMD64 
action_result.data.\*.machines.\*.os_platform | string |  |   WINDOWS 
action_result.data.\*.machines.\*.os_release_name | string |  |   Microsoft Windows 10 Pro 
action_result.data.\*.total_count | numeric |  |   7 
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   2 
summary.total_objects_successful | numeric |  |   0   

## action: 'get endpoint info'
Get information about an endpoint

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname of the endpoint to get information | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hostname | string |  `host name`  |   test 
action_result.data.\*.created_at | string |  |   2019-05-01T22:03:31.019437Z 
action_result.data.\*.id | string |  |   6013e073d5a384b4bc1b494f9258a43a6af11a50 
action_result.data.\*.last_seen_at | string |  |   2019-05-04T17:28:00.211005Z 
action_result.data.\*.name | string |  |   WIN-V9TNRP1M0G4 
action_result.data.\*.online | boolean |  |   True  False 
action_result.data.\*.os_architecture | string |  |   AMD64 
action_result.data.\*.os_platform | string |  |   WINDOWS 
action_result.data.\*.os_release_name | string |  |   Microsoft Windows 10 Pro 
action_result.summary | string |  |  
action_result.message | string |  |   Message from action 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get scan info'
Get information about a scan job

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**scan_id** |  required  | Scan ID for the job | string |  `scan id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.scan_id | string |  `scan id`  |   0f03a753-553e-4dbd-a3d6-94b18a96799b 
action_result.data.\*.deleted_count | numeric |  |   0 
action_result.data.\*.duration_seconds | numeric |  |   90 
action_result.data.\*.found_count | numeric |  |   2 
action_result.data.\*.from_cloud | boolean |  |   True  False 
action_result.data.\*.id | string |  |   fd47c2e9-83a3-4675-bac4-0133ab3a4f65 
action_result.data.\*.machine_id | string |  |   ebc10d20-7a2e-4f69-8313-97a472bc712b 
action_result.data.\*.machine_name | string |  |   test.domain.com 
action_result.data.\*.ondemand | boolean |  |   True  False 
action_result.data.\*.os_platform | string |  |   WINDOWS 
action_result.data.\*.quarantined_count | numeric |  |   2 
action_result.data.\*.reported_at | string |  |   2019-04-25T16:01:39.093722Z 
action_result.data.\*.scan_type | string |  |   ThreatScan 
action_result.data.\*.started_at | string |  |   2019-04-25T16:01:01Z 
action_result.data.\*.started_at_local | string |  |   2019-04-25T09:01:01-07:00 
action_result.data.\*.total_count | numeric |  |   2 
action_result.summary | string |  |  
action_result.message | string |  |   Message from action 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 