"""
IMAP Library - a IMAP email testing library.
"""
import base64
from email import message_from_string
from imaplib import IMAP4, IMAP4_SSL
from re import findall
from time import sleep, time
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from builtins import str


class CustomImapLibrary(object):

    PORT = 143
    PORT_SECURE = 993
    FOLDER = 'INBOX'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """ImapLibrary can be imported without argument.

        Examples:
        | = Keyword Definition =  | = Description =       |
        | Library `|` ImapLibrary | Initiate Imap library |
        """
        self._email_index = None
        self._imap = None
        self._mails = []
        self._mp_iter = None
        self._mp_msg = None
        self._part = None

    def close_mailbox(self):
        """Close IMAP email client session.

        Examples:
        | Close Mailbox |
        """
        self._imap.close()

    def delete_all_emails(self):
        """Delete all emails.

        Examples:
        | Delete All Emails |
        """
        typ, mails = self._imap.uid('search', None, 'ALL')
        self._mails = mails[0].split()

        print("Deleting e-mails from ID: [{0}]".format(', '.join(map(str, self._mails))))

        for mail in self._mails:
            self.delete_email(mail)
        self._imap.expunge()

    def decode_email_body(self, body_email_encoded):
        """Returns the email body encoded on base64 decoded to a string UTF-8.

        Arguments:
        - ``body_email_encoded``: An string from the email body encoded on base64.

        Examples:
        | BODY           | Get Email Body    | EMAIL_INDEX |
        | BODYDECODED    | Decode Email Body | BODY        |
        | Log            | BODY              |
        """
        print("Deconding [%s] to string." % (body_email_encoded))

        if not body_email_encoded.endswith("=="):
            body_email_encoded = body_email_encoded + "=="

        email_decoded = base64.b64decode(body_email_encoded)

        return email_decoded.decode('UTF-8')

    def delete_all_emails_with_kwargs(self, **kwargs):
        """Delete all emails.

        Examples:
        | Delete All Emails |
        """
        self._mails = self._check_emails(**kwargs)

        for mail in self._mails:
            self.delete_email(mail)
        self._imap.expunge()

    def delete_email(self, email_index):
        """Delete email on given ``email_index``.

        Arguments:
        - ``email_index``: An email index to identity the email message.

        Examples:
        | Delete Email | INDEX |
        """
        self._imap.uid('store', email_index, '+FLAGS', r'(\DELETED)')
        self._imap.expunge()

    def get_email_body(self, email_index):
        """Returns the decoded email body on multipart email message,
        otherwise returns the body text.

        Arguments:
        - ``email_index``: An email index to identity the email message.

        Examples:
        | Get Email Body | INDEX |
        """
        if self._is_walking_multipart(email_index):
            body = self.get_multipart_payload(decode=True)
        else:
            body = self._imap.uid('fetch',
                                  email_index,
                                  '(BODY[TEXT])')[1][0][1].\
                decode('quoted-printable')
        return body

    def get_links_from_email(self, email_index):
        """Returns all links found in the email body from given ``email_index``.

        Arguments:
        - ``email_index``: An email index to identity the email message.

        Examples:
        | Get Links From Email | INDEX |
        """
        body = self.get_email_body(email_index)
        return findall(r'href=[\'"]?([^\'" >]+)', body)

    def get_matches_from_email(self, email_index, pattern):
        """Returns all Regular Expression ``pattern`` found in the email body
        from given ``email_index``.

        Arguments:
        - ``email_index``: An email index to identity the email message.
        - ``pattern``: It consists of one or more character literals, operators, or constructs.

        Examples:
        | Get Matches From Email | INDEX | PATTERN |
        """
        body = self.get_email_body(email_index)
        return findall(pattern, body)

    def get_multipart_content_type(self):
        """Returns the content type of current part of selected multipart email message.

        Examples:
        | Get Multipart Content Type |
        """
        return self._part.get_content_type()

    def get_multipart_field(self, field):
        """Returns the value of given header ``field`` name.

        Arguments:
        - ``field``: A header field name: ``From``, ``To``, ``Subject``, ``Date``, etc.
                     All available header field names of an email message can be found by running
                     `Get Multipart Field Names` keyword.

        Examples:
        | Get Multipart Field | Subject |
        """
        return self._mp_msg[field]

    def get_multipart_field_names(self):
        """Returns all available header field names of selected multipart email message.

        Examples:
        | Get Multipart Field Names |
        """
        return list(self._mp_msg.keys())

    def get_multipart_payload(self, decode=False):
        """Returns the payload of current part of selected multipart email message.

        Arguments:
        - ``decode``: An indicator flag to decode the email message. (Default False)

        Examples:
        | Get Multipart Payload |
        | Get Multipart Payload | decode=True |
        """
        payload = self._part.get_payload(decode=decode)
        charset = self._part.get_content_charset()
        if charset is not None:
            return payload.decode(charset)
        return payload

    def mark_all_emails_as_read(self):
        """Mark all received emails as read.

        Examples:
        | Mark All Emails As Read |
        """
        for mail in self._mails:
            self._imap.uid('store', mail, '+FLAGS', r'\SEEN')

    def mark_as_read(self):
        """****DEPRECATED****
        Shortcut to `Mark All Emails As Read`.
        """
        self.mark_all_emails_as_read()

    def mark_email_as_read(self, email_index):
        """Mark email on given ``email_index`` as read.

        Arguments:
        - ``email_index``: An email index to identity the email message.

        Examples:
        | Mark Email As Read | INDEX |
        """
        self._imap.uid('store', email_index, '+FLAGS', r'\SEEN')

    def open_link_from_email(self, email_index, link_index=0):
        """Open link URL from given ``link_index`` in email message body of given ``email_index``.
        Returns HTML content of opened link URL.

        Arguments:
        - ``email_index``: An email index to identity the email message.
        - ``link_index``: The link index to be open. (Default 0)

        Examples:
        | Open Link From Email |
        | Open Link From Email | 1 |
        """
        urls = self.get_links_from_email(email_index)

        if len(urls) > link_index:
            resp = urlopen(urls[link_index])
            content_type = resp.headers.getheader('content-type')
            if content_type:
                enc = content_type.split('charset=')[-1]
                return str(resp.read(), enc)
            else:
                return resp.read()
        else:
            raise AssertionError("Link number %i not found!" % link_index)

    def open_link_from_mail(self, email_index, link_index=0):
        """****DEPRECATED****
        Shortcut to `Open Link From Email`.
        """
        return self.open_link_from_email(email_index, link_index)

    def open_mailbox(self, **kwargs):
        """Open IMAP email client session to given ``host`` with given ``user`` and ``password``.

        Arguments:
        - ``host``: The IMAP host server. (Default None)
        - ``is_secure``: An indicator flag to connect to IMAP host securely or not. (Default True)
        - ``password``: The plaintext password to be use to authenticate mailbox on given ``host``.
        - ``port``: The IMAP port number. (Default None)
        - ``user``: The username to be use to authenticate mailbox on given ``host``.
        - ``folder``: The email folder to read from. (Default INBOX)

        Examples:
        | Open Mailbox | host=HOST | user=USER | password=SECRET |
        | Open Mailbox | host=HOST | user=USER | password=SECRET | is_secure=False |
        | Open Mailbox | host=HOST | user=USER | password=SECRET | port=8000 |
        | Open Mailbox | host=HOST | user=USER | password=SECRET | folder=Drafts
        """
        host = kwargs.pop('host', kwargs.pop('server', None))
        is_secure = kwargs.pop('is_secure', 'True') == 'True'
        port = int(kwargs.pop('port', self.PORT_SECURE if is_secure else self.PORT))
        folder = '"%s"' % str(kwargs.pop('folder', self.FOLDER))
        self._imap = IMAP4_SSL(host, port) if is_secure else IMAP4(host, port)
        self._imap.login(kwargs.pop('user', None), kwargs.pop('password', None))
        self._imap.select(folder)
        self._init_multipart_walk()

    def wait_for_email(self, **kwargs):
        """Wait for email message to arrived base on any given filter criteria.
        Returns email index of the latest email message received.

        Arguments:
        - ``poll_frequency``: The delay value in seconds to retry the mailbox check. (Default 10)
        - ``recipient``: Email recipient. (Default None)
        - ``sender``: Email sender. (Default None)
        - ``status``: A mailbox status filter: ``MESSAGES``, ``RECENT``, ``UIDNEXT``,
                      ``UIDVALIDITY``, and ``UNSEEN``.
                      Please see [https://goo.gl/3KKHoY|Mailbox Status] for more information.
                      (Default None)
        - ``subject``: Email subject. (Default None)
        - ``text``: Email body text. (Default None)
        - ``timeout``: The maximum value in seconds to wait for email message to arrived.
                       (Default 60)
        - ``folder``: The email folder to check for emails. (Default INBOX)

        Examples:
        | Wait For Email | sender=noreply@domain.com |
        | Wait For Email | sender=noreply@domain.com | folder=OUTBOX
        """
        poll_frequency = float(kwargs.pop('poll_frequency', 10))
        timeout = int(kwargs.pop('timeout', 60))
        end_time = time() + timeout
        while time() < end_time:
            self._mails = self._check_emails(**kwargs)
            if len(self._mails) > 0:
                return self._mails[-1]
            if time() < end_time:
                sleep(poll_frequency)
        raise AssertionError("No email received within %ss" % timeout)

    def wait_for_mail(self, **kwargs):
        """****DEPRECATED****
        Shortcut to `Wait For Email`.
        """
        return self.wait_for_email(**kwargs)

    def walk_multipart_email(self, email_index):
        """Returns total parts of a multipart email message on given ``email_index``.
        Email message is cache internally to be used by other multipart keywords:
        `Get Multipart Content Type`, `Get Multipart Field`, `Get Multipart Field Names`,
        `Get Multipart Field`, and `Get Multipart Payload`.

        Arguments:
        - ``email_index``: An email index to identity the email message.

        Examples:
        | Walk Multipart Email | INDEX |
        """
        if not self._is_walking_multipart(email_index):
            data = self._imap.uid('fetch', email_index, '(RFC822)')[1][0][1]
            msg = message_from_string(data)
            self._start_multipart_walk(email_index, msg)
        try:
            self._part = next(self._mp_iter)
        except StopIteration:
            self._init_multipart_walk()
            return False
        # return number of parts
        return len(self._mp_msg.get_payload())

    def _check_emails(self, **kwargs):
        """Returns filtered email."""
        folder = '"%s"' % str(kwargs.pop('folder', self.FOLDER))
        criteria = self._criteria(**kwargs)
        # Calling select before each search is necessary with gmail
        status, data = self._imap.select(folder)
        if status != 'OK':
            raise Exception("imap.select error: %s, %s" % (status, data))
        typ, msgnums = self._imap.uid('search', None, *criteria)
        if typ != 'OK':
            raise Exception('imap.search error: %s, %s, criteria=%s' % (typ, msgnums, criteria))
        return msgnums[0].split()

    @staticmethod
    def _criteria(**kwargs):
        """Returns email criteria."""
        criteria = []
        recipient = kwargs.pop('recipient', kwargs.pop('to_email', kwargs.pop('toEmail', None)))
        sender = kwargs.pop('sender', kwargs.pop('from_email', kwargs.pop('fromEmail', None)))
        status = kwargs.pop('status', None)
        subject = kwargs.pop('subject', None)
        text = kwargs.pop('text', None)
        if recipient:
            criteria += ['TO', '"%s"' % recipient]
        if sender:
            criteria += ['FROM', '"%s"' % sender]
        if subject:
            criteria += ['SUBJECT', '"%s"' % subject]
        if text:
            criteria += ['TEXT', '"%s"' % text]
        if status:
            criteria += [status]
        if not criteria:
            criteria = ['UNSEEN']
        return criteria

    def _init_multipart_walk(self):
        """Initialize multipart email walk."""
        self._email_index = None
        self._mp_msg = None
        self._part = None

    def _is_walking_multipart(self, email_index):
        """Returns boolean value whether the multipart email walk is in-progress or not."""
        return self._mp_msg is not None and self._email_index == email_index

    def _start_multipart_walk(self, email_index, msg):
        """Start multipart email walk."""
        self._email_index = email_index
        self._mp_msg = msg
        self._mp_iter = msg.walk()
