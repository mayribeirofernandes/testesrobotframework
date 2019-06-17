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

from .utils import *
from suds.wsse import Security
from suds.wsse import Token
from suds.wsse import Timestamp
from suds.wsse import UsernameToken
from suds.sax.element import Element
from random import random
from hashlib import sha1
import base64
import re
from datetime import timedelta, datetime
import robot


TEXT_TYPE = 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText'
DIGEST_TYPE = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest"
BASE64_ENC_TYPE = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
WSSENS = \
    ('wsse',
     'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
WSUNS = \
    ('wsu',
     'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd')


def iso_utc(dt=None):
    if dt is None:
        dt = datetime.utcnow()
    # precision only to milliseconds per WS-Security recommendation
    return re.sub(r'(?<=\.\d{3})\d+', '', dt.isoformat()) + 'Z'


class AutoTimestamp(Timestamp):

    def __init__(self, validity=None):
        Token.__init__(self)
        self.validity = validity

    def xml(self):
        self.created = datetime.utcnow()
        root = Element("Timestamp", ns=WSUNS)
        created = Element('Created', ns=WSUNS)
        created.setText(iso_utc(self.created))
        root.append(created)
        if self.validity is not None:
            self.expires = self.created + timedelta(seconds=self.validity)
            expires = Element('Expires', ns=WSUNS)
            expires.setText(iso_utc(self.expires))
            root.append(expires)
        return root


class AutoUsernameToken(UsernameToken):

    def __init__(self, username=None, password=None, setcreated=False,
                 setnonce=False, digest=False):
        UsernameToken.__init__(self, username, password)
        self.autosetcreated = setcreated
        self.autosetnonce = setnonce
        self.digest = digest

    def setnonce(self, text=None):
        if text is None:
            hash = sha1()
            hash.update(str(random()))
            hash.update(iso_utc())
            self.nonce = hash.hexdigest()
        else:
            self.nonce = text

    def xml(self):
        if self.digest and self.password is None:
            raise RuntimeError("Cannot generate password digest without the password.")
        if self.autosetnonce:
            self.setnonce()
        if self.autosetcreated:
            self.setcreated()
        root = Element('UsernameToken', ns=WSSENS)
        u = Element('Username', ns=WSSENS)
        u.setText(self.username)
        root.append(u)
        if self.password is not None:
            password = self.password
            if self.digest:
                password = self.get_digest()
            p = Element('Password', ns=WSSENS)
            p.setText(password)
            p.set('Type', DIGEST_TYPE if self.digest else TEXT_TYPE)
            root.append(p)
        if self.nonce is not None:
            n = Element('Nonce', ns=WSSENS)
            n.setText(base64.encodestring(self.nonce)[:-1])
            n.set('EncodingType', BASE64_ENC_TYPE)
            root.append(n)
        if self.created:
            c = Element('Created', ns=WSUNS)
            c.setText(iso_utc(self.created))
            root.append(c)
        return root

    def get_digest(self):
        nonce = str(self.nonce) if self.nonce else ""
        created = iso_utc(self.created) if self.created else ""
        password = str(self.password)
        message = nonce + created + password
        return base64.encodestring(sha1(message).digest())[:-1]


class _WsseKeywords(object):

    def apply_security_timestamp(self, duration=None):
        """Applies a Timestamp element to future requests valid for the given `duration`.

        The SOAP header will contain a Timestamp element as specified in the
        WS-Security extension. The Created and Expires values are updated
        every time a request is made. If `duration` is None, the Expires
        element will be absent.

        `duration` must be given in Robot Framework's time format (e.g.
        '1 minute', '2 min 3 s', '4.5').

        Example:
        | Apply Security Timestamp | 5 min |
        """
        if duration is not None:
            duration = robot.utils.timestr_to_secs(duration)
        wsse = self._get_wsse()
        wsse.tokens = [x for x in wsse.tokens if not isinstance(x, Timestamp)]
        wsse.tokens.insert(0, AutoTimestamp(duration))
        self._client().set_options(wsse=wsse)

    def apply_username_token(self, username, password=None, setcreated=False,
                             setnonce=False, digest=False):
        """Applies a UsernameToken element to future requests.

        The SOAP header will contain a UsernameToken element as specified in
        Username Token Profile 1.1 that complies with Basic Security Profile
        1.1. The Created and Nonce values, if enabled, are generated
        automatically and updated every time a request is made. If `digest` is
        True, a digest derived from the password is sent.

        Example:
        | Apply Username Token | ying | myPa$$word |
        """
        setcreated = to_bool(setcreated)
        setnonce = to_bool(setnonce)
        digest = to_bool(digest)
        if digest and password is None:
            raise RuntimeError("Password is required when digest is True.")
        token = AutoUsernameToken(username, password, setcreated, setnonce,
                                  digest)
        wsse = self._get_wsse()
        wsse.tokens = [x for x in wsse.tokens if not isinstance(x, UsernameToken)]
        wsse.tokens.append(token)
        self._client().set_options(wsse=wsse)

    # private

    def _get_wsse(self, create=True):
        wsse = self._client().options.wsse
        if wsse is None and create:
            wsse = Security()
            wsse.mustUnderstand = '1'
        return wsse
