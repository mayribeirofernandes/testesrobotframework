# Copyright 2012 Kevin Ormbrek
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

import xml.dom.minidom
from xml.parsers.expat import ExpatError
from suds.plugin import MessagePlugin
from robot.api import logger
from .utils import *


class _SoapLogger(MessagePlugin):

    def __init__(self):
        self._sent = None
        self._received = None
        self.log = True
        self.prettyxml = True
        self._indent = 2

    def sending(self, context):
        self._sent = context.envelope
        self._received = None
        if self.log:
            logger.info('Sending:\n%s' % self.last_sent(self.prettyxml))

    def last_sent(self, prettyxml=False):
        # possible that text inserted into the post body, making it invalid XML
        try:
            return self._prettyxml(self._sent) if prettyxml else self._sent
        except ExpatError:
            return self._sent

    def received(self, context):
        self._received = context.reply
        if self.log:
            logger.info('Received:\n%s' % self.last_received(self.prettyxml))

    def last_received(self, prettyxml=False):
        return self._prettyxml(self._received) if prettyxml else self._received

    def set_indent(self, indent):
        try:
            self._indent = int(indent)
        except ValueError:
            raise ValueError("Cannot convert indent value '%s' to an integer"
                             % indent)

    def _prettyxml(self, xml_string):
        dom = xml.dom.minidom.parseString(xml_string)
        return dom.toprettyxml(indent=(self._indent * " "))


class _SoapLoggingKeywords(object):

    def set_soap_logging(self, log, prettyxml=None, indent=None):
        """Sets whether to log the request and response for the current client.

        By default, the message sent and received is logged at level INFO,
        pretty-formatted with an indent of 2 spaces per level. Setting `log`
        to false will disable logging, reducing the size of the log. Boolean
        option `prettyxml` controls whether the XML is pretty-formatted.
        `indent` should be the number of spaces to indent per level. Leaving
        `prettyxml` or `indent` at the default value of None will preserve the
        previous settings. Returns the current value of log.

        Examples:
        | ${old log value} | Set Soap Logging | False    |   |
        | Call Soap Method | lengthyResponse  |          |   |
        | Set Soap Logging | True             | True     | 4 |
        """
        new_value = to_bool(log)
        soap_logger = self._get_soap_logger()
        if soap_logger:
            old_value = soap_logger.log
        else:
            soap_logger = self._add_soap_logger()
            old_value = False
        soap_logger.log = new_value
        if not prettyxml is None:
            soap_logger.prettyxml = to_bool(prettyxml)
        if not indent is None:
            soap_logger.set_indent(indent)
        return old_value

    def get_last_sent(self):
        """Gets the message text last sent.

        Unless a plugin is used to modify the message, it will always be a XML
        document."""
        soap_logger = self._get_soap_logger(True)
        return soap_logger.last_sent(False)

    def get_last_received(self):
        """Gets the XML last received."""
        soap_logger = self._get_soap_logger(True)
        return soap_logger.last_received(False)

    # private

    def _get_soap_logger(self, required=False):
        plugins = self._client().options.plugins
        matches = [x for x in plugins if isinstance(x, _SoapLogger)]
        if matches:
            return matches[0]
        else:
            if required:
                raise RuntimeError("The SudsLibrary SOAP logging message plugin has been removed.")
            return None

    def _add_soap_logger(self):
        client = self._client()
        plugins = client.options.plugins
        soap_logger = _SoapLogger()
        plugins.append(soap_logger)
        client.set_options(plugins=plugins)
        return soap_logger
