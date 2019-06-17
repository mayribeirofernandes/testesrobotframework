# Copyright 2013 Kevin Ormbrek
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from suds import WebFault
from suds import byte_str
from suds.sax.text import Raw
from .utils import *
import socket


class RawSoapMessage(object):

    def __init__(self, string):
        if isinstance(string, bytes):
            self.message = string.decode()
        else:
            self.message = str(string)

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message


class _ProxyKeywords(object):

    def call_soap_method(self, name, *args):
        """Calls the SOAP method with the given `name` and `args`.

        Returns a Python object graph or SOAP envelope as a XML string
        depending on the client options.
        """

        return self._call(None, None, False, name, *args)

    def specific_soap_call(self, service, port, name, *args):
        """Calls the SOAP method overriding client settings.

        If there is only one service specified then `service` is ignored.
        `service` and `port` can be either by name or index. If only `port` or
        `service` need to be specified, leave the other one ${None} or
        ${EMPTY}. The index is the order of appearence in the WSDL starting
        with 0.

        Returns a Python object graph or SOAP envelope as a XML string
        depending on the client options.
        """

        return self._call(service, port, False, name, *args)

    def call_soap_method_expecting_fault(self, name, *args):
        """Calls the SOAP method expecting the server to raise a fault.

        Fails if the server does not raise a fault.  Returns a Python object
        graph or SOAP envelope as a XML string depending on the client
        options.

        A fault has the following attributes:\n
        | faultcode   | required |
        | faultstring | required |
        | faultactor  | optional |
        | detail      | optional |
        """
        return self._call(None, None, True, name, *args)

    def create_raw_soap_message(self, message):
        """Returns an object that can used in lieu of SOAP method arguments.

        `message` should be an entire SOAP message as a string. The object
        returned can be used in lieu of *args for `Call Soap Method`, `Call
        Soap Method Expecting Fault`, and `Specific Soap Call`.

        Example:\n
        | ${message}=      | Create Raw Soap Message | <SOAP-ENV:Envelope ...</ns2:Body></SOAP-ENV:Envelope> |
        | Call Soap Method | addContact              | ${message}                                            |
        """
        return RawSoapMessage(message)

    # private

    def _call(self, service, port, expect_fault, name, *args):
        client = self._client()
        self._backup_options()
        if service or (service == 0):
            client.set_options(service=parse_index(service))
        if port or (port == 0):
            client.set_options(port=parse_index(port))
        method = getattr(client.service, name)
        received = None
        try:
            if len(args) == 1 and isinstance(args[0], RawSoapMessage):
                message = byte_str(args[0].message)
                received = method(__inject={'msg': message})
            else:
                received = method(*args)
            if expect_fault:
                raise AssertionError('The server did not raise a fault.')
        except WebFault as e:
            if not expect_fault:
                raise e
            received = e.fault
        finally:
            self._restore_options()
        return_xml = self._get_external_option("return_xml", False)
        if return_xml:
            received = self.get_last_received()
        return received

    # private

    def _backup_options(self):
        options = self._client().options
        self._old_options = dict([[n, getattr(options, n)] for n in ('service', 'port')])
        if self._global_timeout:
            self._old_timeout = socket.getdefaulttimeout()

    def _restore_options(self):
        self._client().set_options(**self._old_options)
        # restore the default socket timeout because suds does not
        if self._global_timeout:
            socket.setdefaulttimeout(self._old_timeout)
