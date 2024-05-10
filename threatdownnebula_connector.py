# File: threatdownnebula_connector.py
#
# Copyright (c) ThreatDown, 2019-2024
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

# Phantom App imports

# Usage of the consts file is recommended
# from threatdownnebula_consts import *
import json
import time
from datetime import datetime

import phantom.app as phantom
import requests
from oauthlib.oauth2 import BackendApplicationClient
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from requests_oauthlib import OAuth2Session

__author__ = "Rohin Sambath Kumar"
__copyright__ = "Copyright 2019-2024, ThreatDown"
__credits__ = ["Rohin Sambath Kumar"]
__license__ = "GPL"
__version__ = "2.1.1"
__maintainer__ = "Rohin Sambath Kumar"
__email__ = "support@threatdown.com"
__status__ = "Production"


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class ThreatDownNebulaConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(ThreatDownNebulaConnector, self).__init__()

        self._state = None
        self._base_url = None
        self.HEADER = {"Content-Type": "application/json"}

    def NEBULA_URL(self, path):
        return "{NEBULA_URL}{PATH}".format(NEBULA_URL="https://cloud.threatdown.com", PATH=path)

    def _handle_test_connectivity(self, param):

        # Add an action result object to self(BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Connecting to ThreatDown Nebula")

        try:
            self.save_progress("Account ID: {}".format(self.account_id))
            self.save_progress("Client ID: {}".format(self.client_id))
            client = BackendApplicationClient(self.client_id, scope=self.client_scope)
            nebula = OAuth2Session(client=client, scope=self.client_scope)
            nebula.headers.update(self.HEADER)
            nebula.fetch_token(token_url="{}/oauth2/token".format(self._base_url), client_secret=self.client_secret, scope=self.client_scope)
            self.save_progress("Login to ThreatDown Nebula is successful")
        except Exception as err:
            if "'ascii' codec can't decode" in str(err):
                return action_result.set_status(phantom.APP_ERROR,
                "Error Connecting to ThreatDown Nebula. Please provide valid asset configuration parameters.")
            return action_result.set_status(phantom.APP_ERROR,
            "Error Connecting to ThreatDown Nebula. Details: {0}".format(str(err)))

        # Return success
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_endpoints(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self(BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # make call to get endpoints
        try:
            more_data = True
            total_count = 0
            running_count = 0
            next_cursor = ''
            results = {'machines': []}
            machines = []
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()

            while more_data:
                resp = nebula.get(self.NEBULA_URL('/api/v2/endpoints?next_cursor=' + next_cursor))
                data = json.loads(resp.text)

                rate_limit = int(resp.headers.get('x-rate-limit-remaining'))
                if rate_limit < 10:
                    time.sleep(60)

                total_count = data.get('total_count')
                next_cursor = data.get('next_cursor')
                machines += data.get('machines')
                running_count += len(data.get('machines'))
                if total_count > running_count:
                    more_data = True
                else:
                    more_data = False

            self.save_progress("Total endpoints found: {0}".format(str(len(results['machines']))))
            # Add the response into the data section
            results = {'machines': machines}
            action_result.add_data(results)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in list_endpoints. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_scan_remediate_endpoint(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "command": "command.threat.scan",
            "data": {"scan_settings": {"type": "ThreatScan", "remove": True}},
            "machine_ids": [id]}

        # scan and remediate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in list_endpoints. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_scan_report_endpoint(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "command": "command.threat.scan",
            "data": {"scan_settings": {"type": "ThreatScan", "remove": False}},
            "machine_ids": [id]}

        # scan and remediate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in list_endpoints. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_isolate_endpoint(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "machine_ids": [id],
            "data": {"process": True, "network": True, "desktop": True}
        }

        # Isolate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs/endpoints/isolate'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in isolate_endpoint. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_isolate_process(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "machine_ids": [id],
            "data": {"process": True}
        }

        # Isolate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs/endpoints/isolate'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in isolate_process. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_isolate_network(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "machine_ids": [id],
            "data": {"network": True}
        }

        # Isolate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs/endpoints/isolate'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in isolate_network. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_isolate_desktop(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "machine_ids": [id],
            "data": {"desktop": True}
        }

        # Isolate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs/endpoints/isolate'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in isolate_desktop. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_deisolate_endpoint(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        headers = self.HEADER
        headers.update({"content-type": "application/json; charset=UTF-8"})

        body = {
            "machine_ids": [id]
        }

        # Isolate endpoint
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.post(self.NEBULA_URL('/api/v2/jobs/endpoints/unlock'), data=json.dumps(body), headers=headers)
            self.save_progress("response: {0}".format(response.text))
            action_result.add_data(response.text)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in deisolate_endpoint. Details: {0}".format(str(err))))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_endpoint_info(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        hostname = param["hostname"]
        ret_val, id = self._get_agent_id(hostname, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("ID for host " + hostname + " - " + id)

        if id == "0":
            return action_result.set_status(phantom.APP_SUCCESS, "Endpoint not found")
        elif id == "99":
            return action_result.set_status(phantom.APP_SUCCESS, "More than one endpoint found")
        else:
            summary = action_result.update_summary({})
            summary["hostname"] = hostname
            summary["machine_id"] = id

        # make call to get endpoint info
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.get(self.NEBULA_URL('/api/v2/endpoints/' + id))
            data = json.loads(response.text)
            self.save_progress("response: {0}".format(response.text))
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in get_endpoint_info. Details: {0}".format(str(err))))

        # Add the response into the data section
        action_result.add_data(data)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_scan_info(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        scan_id = param["scan_id"]
        self.save_progress("Requesting scan details for scan_id: " + scan_id)

        summary = action_result.update_summary({})
        summary["scan_id"] = scan_id

        # make call to get scan info
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            response = nebula.get(self.NEBULA_URL('/api/v2/scans/' + scan_id))
            data = json.loads(response.text)
            self.save_progress("response: {0}".format(response.text))
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error in get_scan_info. Details: {0}".format(str(err))))

        # Add the response into the data section
        action_result.add_data(data)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_agent_id(self, search_text, action_result):
        # First lookup the Agent ID
        try:
            ret_val, nebula = self._get_nebula_client(action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status(), None
            response = nebula.get(self.NEBULA_URL('/api/v2/endpoints?search_string=' + search_text))
            data = json.loads(response.text)
            self.save_progress("response: {0}".format(response.text))
        except Exception as err:
            return RetVal(action_result.set_status( phantom.APP_ERROR, "Error in _get_agent_id. Details: {0}".format(str(err))), None)

        endpoints_found = data.get("total_count")
        self.save_progress("Endpoints found: " + str(endpoints_found))
        # action_result.add_data(response)

        if endpoints_found == 0:
            return phantom.APP_SUCCESS, "0"
        elif endpoints_found > 1:
            return phantom.APP_SUCCESS, "99"
        elif data.get('machines') and data.get('machines')[0].get('id'):
            return phantom.APP_SUCCESS, data.get('machines')[0].get('id')
        else:
            return RetVal(action_result.set_status( phantom.APP_ERROR, "Error while getting the agent ID"), None)

    def _get_nebula_client(self, action_result):
        try:
            client = BackendApplicationClient(self.client_id, scope=self.client_scope)
            nebula = OAuth2Session(client=client, scope=self.client_scope)
            nebula.headers.update(self.HEADER)
            nebula.fetch_token(token_url=self._base_url + '/oauth2/token', client_secret=self.client_secret, scope=self.client_scope)
            # ThreatDown Telemerty Code.
            try:
                TELEMETRY_LINK = "https://api-msp-telemetry.threatdown.com/data"
                APP_VERSION = "2.1.1"
                telemetry_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                data = {
                        "timestamp": str(telemetry_ts),
                        "integration_code": "TA-PH",
                        "integration_name": "Splunk Phantom",
                        "integration_app": "ThreatDown Nebula",
                        "integration_app_version": APP_VERSION,
                        "nebula_account_id": self.account_id.decode("utf8"),
                        "ov_account_id": "",
                        "mbbr_license_key": "",
                        "api_client_id": self.client_id.decode("utf8"),
                        "custom_fields": [],
                        "msg_type": "INTEGRATION INUSE",
                        "token": "Bearer " + str(nebula.access_token)
                }
                body = json.dumps(data)
                telemetry_response = nebula.post(TELEMETRY_LINK, data=body)
                response_code = json.loads(telemetry_response.text).get("statusCode")
                if response_code != 201:
                    self.debug_print("Telemetry response code is not equal <201>. Actual code:")
                else:
                    self.debug_print("Telemetry successfully sent!")
            except Exception:
                self.debug_print("Error in telemetry! Skipping this step.")

            return(phantom.APP_SUCCESS, nebula)
        except Exception as err:
            return RetVal(action_result.set_status(phantom.APP_ERROR,
            "Error Connecting to ThreatDown Nebula. Details: {0}".format(str(err))), None)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_endpoints':
            ret_val = self._handle_list_endpoints(param)

        elif action_id == 'scan_remediate_endpoint':
            ret_val = self._handle_scan_remediate_endpoint(param)

        elif action_id == 'scan_report_endpoint':
            ret_val = self._handle_scan_report_endpoint(param)

        elif action_id == 'isolate_endpoint':
            ret_val = self._handle_isolate_endpoint(param)

        elif action_id == 'deisolate_endpoint':
            ret_val = self._handle_deisolate_endpoint(param)

        elif action_id == 'isolate_process':
            ret_val = self._handle_isolate_process(param)

        elif action_id == 'isolate_desktop':
            ret_val = self._handle_isolate_desktop(param)

        elif action_id == 'isolate_network':
            ret_val = self._handle_isolate_network(param)

        elif action_id == 'get_endpoint_info':
            ret_val = self._handle_get_endpoint_info(param)

        elif action_id == 'get_scan_info':
            ret_val = self._handle_get_scan_info(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        # Access values in asset config by the name
        # Required values can be accessed directly
        self._base_url = 'https://cloud.threatdown.com'
        self.account_id = config['accountid'].encode('utf-8')
        self.client_id = config['clientid'].encode('utf-8')
        self.client_secret = config['clientsecret']
        self.client_scope = "read write execute"
        self.HEADER = {"x-mwb-clientid": self.client_id, "x-mwb-accountid": self.account_id}

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)
    argparser.add_argument('-v', '--verify', action='store_true', help='verify', required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if(username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        login_url = BaseConnector._get_phantom_base_url() + "login"
        try:
            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=60)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=60)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = ThreatDownNebulaConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(1)
