# Copyright 2013-2015 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

"""This module implements the HaaS client library."""
from haas import config
from haas.config import cfg

from haas.rest import APIError, ServerError
import requests


class Haas:
    """Client class for making Haas API calls.
    Note that this client library is not yet complete, and will filled out as
    needed.

    Example:
        h = Haas(endpoint="http://127.0.0.1:5000")
        h.node_connect_network("node-2000", "eth1", "production-network",
        "vlan/native")

    Errors are thrown when receiving HTTP status_codes from the HaaS server
    that are not in the [200,300) range
    """

    def __init__(self, endpoint=None):
        """Initiatlize an instance.

        If endpoint is None, use the endpoint specification from:
            1) The HAAS_ENDPOINT env variable or
            2) Take the endpoint from [client] endpoint

        Exceptions:
            LookupError - no endpoint could be found
        """

        if endpoint != None:
            self.endpoint = endpoint
        else:
            self.endpoint = os.environ.get('HAAS_ENDPOINT')
            if self.endpoint is None:
                try:
                    self.endpoint = cfg.get('client', 'endpoint')
                except e:
                    throw LookupError("no endpoint found")

    def object_url(self, *args):
        """Append the arguments to the endpoint URL"""
        url = self.endpoint
        for arg in args:
            url += '/' + urllib.quote(arg,'')
        return url


    def node_connect_network(self, node, nic, network, channel="vlan/native"):
        """Connect <node> to <network> on given <nic> and <channel>.
        If no channel is specified, the action is applied to the native vlan.
        Returns text sent from server"""

        url = object_url('node', node, 'nic', nic, 'connect_network')
        data={'network': network, 'channel': channel})
        r = requests.post(url, data=json.dumps(data))

        if not (r.status_code >= 200 and r.status_code < 300):
            """We weren't successful. Throw an exception"""
            if r.status_code >= 400 and r.status_code < 500:
                raise APIError(r.text)
            elif r.status_code >= 500 and r.status_code < 600:
                raise ServerError(r.text)
            else:
                raise Exception(r.text)

        #TODO: when async statuses are incorporated, we could create a status
        #      class, or just return this.
        return r.text
