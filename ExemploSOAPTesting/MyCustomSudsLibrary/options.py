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

from suds.xsd.doctor import Import
from suds.xsd.sxbasic import Import as BasicImport
from suds import ServiceNotFound
from suds.transport.https import HttpAuthenticated
from suds.transport.https import WindowsHttpAuthenticated
from suds.transport.http import HttpAuthenticated as AlwaysSendTransport
from .utils import *
import robot


class _OptionsKeywords(object):

    def set_service(self, service):
        """Sets the `service` to use in future requests.

        `service` should be the name or the index of the service as it appears in the WSDL.
        """
        service = parse_index(service)
        self._client().set_options(service=service)

    def set_port(self, port):
        """Sets the `port` to use in future requests.

        `port` should be the name or the index of the port as it appears in the WSDL.
        """
        port = parse_index(port)
        self._client().set_options(port=port)

    def set_proxies(self, *protocol_url_pairs):
        """Sets the http proxy settings.

        | Set Proxy | http | localhost:5000 | https | 10.0.4.23:80 |
        """
        if len(protocol_url_pairs) % 2 != 0:
            raise ValueError("There should be an even number of protocol-url pairs.")
        proxy = {}
        for i in range(0, len(protocol_url_pairs), 2):
            proxy[protocol_url_pairs[i]] = protocol_url_pairs[i + 1]
        self._client().set_options(proxy=proxy)

    def set_headers(self, *dict_or_key_value_pairs):
        """Sets _extra_ http headers to send in future requests.

        For HTTP headers; not to be confused with the SOAP header element.

        Example:
        | Set Headers | X-Requested-With  | autogen          | # using key-value pairs |
        or using a dictionary:
        | ${headers}= | Create Dictionary | X-Requested-With | autogen                 |
        | Set Headers | ${headers}        |                  | # using a dictionary    |
        """
        length = len(dict_or_key_value_pairs)
        if length == 1:
            headers = dict_or_key_value_pairs[0]
        elif length % 2 == 0:
            headers = {}
            for i in range(0, len(dict_or_key_value_pairs), 2):
                headers[dict_or_key_value_pairs[i]] = dict_or_key_value_pairs[i + 1]
        else:
            raise ValueError("There should be an even number of name-value pairs.")
        self._client().set_options(headers=headers)

    def set_soap_headers(self, *headers):
        """Sets SOAP headers to send in future requests.

        Example:
        | ${auth header}=           | Create Wsdl Object | AuthHeader           |          |
        | Set Wsdl Object Attribute | ${auth header}     | UserID               | gcarlson |
        | Set Wsdl Object Attribute | ${auth header}     | Password             | heyOh    |
        | Set Soap Headers          | ${auth header}     | # using WSDL object  |          |
        or using a dictionary:
        | ${auth dict}=             | Create Dictionary  | UserName             | gcarlson  | Password | heyOh |
        | Set Soap Headers          | ${auth dict}       | # using a dictionary |           |          |       |

        For setting WS-Security elements in the SOAP header, see
        `Apply Username Token` and `Apply Security Timestamp`.
        """
        self._client().set_options(soapheaders=headers)

    def set_return_xml(self, return_xml):
        """Sets whether to return XML in future requests.

        The default value is _False_. If `return_xml` is _True_, then return
        the SOAP envelope as a string in future requests. Otherwise, return a
        Python object graph. `Get Last Received` returns the XML received
        regardless of this setting.

        See also `Call Soap Method`, `Call Soap Method Expecting Fault`, and
        `Specific Soap Call`.

        Example:
        | ${old value}= | Set Return Xml | True |
        """
        return_xml = to_bool(return_xml)
        # not using the retxml option built into Suds because Suds does not raise exceptions when a SOAP fault occurs
        # when retxml=True. Instead just use the XML that is already being captured with a plugin
        old_value = self._get_external_option("return_xml", False)
        self._set_external_option("return_xml", return_xml)
        return old_value

    def set_http_authentication(self, username, password, type='STANDARD'):
        """Sets http authentication type and credentials.

        Available types are STANDARD, ALWAYS_SEND, and NTLM. Type STANDARD
        will only send credentials to the server upon request (HTTP/1.0 401
        Authorization Required) by the server only. Type ALWAYS_SEND will
        cause an Authorization header to be sent in every request. Type NTLM
        is a Microsoft proprietary authentication scheme that requires the
        python-ntlm package to be installed, which is not packaged with Suds
        or SudsLibrary.
        """
        transport = self._get_transport(type, username=username, password=password)
        self._client().set_options(transport=transport)

    def set_location(self, url, service=None, names=None):
        """Sets location to use in future requests.

        This is for when the location(s) specified in the WSDL are not correct.
        `service` is the name or index of the service to change and ignored
        unless there is more than one service. `names` should be either a
        comma-delimited list of methods names or an iterable (e.g. a list). If
        no methods names are given, then sets the location for all methods of
        the service(s).

        Example:
        | Set Location | http://localhost:8080/myWS |
        """
        wsdl = self._client().wsdl
        service_count = len(wsdl.services)
        if (service_count == 1):
            service = 0
        elif not service is None:
            service = parse_index(service)
        if isinstance(names, bytes):
            names = names.split(b",")
        if service is None:
            for svc in wsdl.services:
                svc.setlocation(url, names)
        elif isinstance(service, int):
            wsdl.services[service].setlocation(url, names)
        else:
            for svc in wsdl.services:
                if svc.name == service:
                    svc.setlocation(url, names)
                    return
            raise ServiceNotFound(service)

    def add_doctor_import(self, import_namespace, location=None, filters=None):
        """Adds an import be used in the next client.

        Doctor imports are applied to the _next_ client created with
        `Create Soap Client`. Doctor imports are necessary when references are
        made in one schema to named objects defined in another schema without
        importing it. Use `location` to specify the location to download the
        schema file. `filters` should be either a comma-delimited list of
        namespaces or an iterable (e.g. a list).

        The following example would import the SOAP encoding schema into only
        the namespace http://some/namespace/A if it is not already imported:
        | Add Doctor Import | http://schemas.xmlsoap.org/soap/encoding/ | filters=http://some/namespace/A |
        """
        if isinstance(filters, bytes):
            filters = filters.split(b",")
        imp = Import(import_namespace, location)
        if not filters is None:
            for filter in filters:
                imp.filter.add(filter)
        self._imports.append(imp)

    def bind_schema_to_location(self, namespace, location):
        """Sets the `location` for the given `namespace` of a schema.

        This is for when an import statement specifies a schema but not its
        location. If the schemaLocation is present and incorrect, this will
        not override that. Bound schemas are shared amongst all instances of
        SudsLibrary. Schemas should be bound if necessary before `Add Doctor
        Import` or `Create Soap Client` where appropriate.
        """
        BasicImport.bind(namespace, location)

    def set_soap_timeout(self, timeout):
        """Sets the timeout for SOAP requests.

        `timeout` must be given in Robot Framework's time format (e.g.
        '1 minute', '2 min 3 s', '4.5'). The default timeout is 90 seconds.

        Example:
        | Set Soap Timeout | 3 min |
        """
        self._set_soap_timeout(timeout)
        timestr = format_robot_time(timeout)
        self._logger.info("SOAP timeout set to %s" % timestr)

    # private

    def _set_boolean_option(self, name, value):
        value = to_bool(value)
        self._client().set_options(**{name: value})

    def _set_soap_timeout(self, timeout):
        timeout_in_secs = robot.utils.timestr_to_secs(timeout)
        self._client().set_options(timeout=timeout_in_secs)

    def _get_external_option(self, name, default):
        value = default
        if self._client() in self._external_options:
            options = self._external_options[self._client()]
            value = options.get(name, default)
        return value

    def _set_external_option(self, name, value):
        if self._client() not in self._external_options:
            self._external_options[self._client()] = {}
        old_value = self._external_options[self._client()].get(name, None)
        self._external_options[self._client()][name] = value
        return old_value

    def _get_transport(self, auth_type, username, password):
        classes = {
            'STANDARD': HttpAuthenticated,
            'ALWAYS_SEND': AlwaysSendTransport,
            'NTLM': WindowsHttpAuthenticated
        }
        try:
            _class = classes[auth_type.upper().strip()]
        except KeyError:
            raise ValueError("'%s' is not a supported authentication type." % auth_type)
        transport = _class(username=username, password=password)
        return transport
