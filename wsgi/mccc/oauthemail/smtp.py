
import smtplib
import ssl
import threading
import base64

from django.conf import settings
from django.core.mail.message import sanitize_address
from django.core.mail.utils import DNS_NAME
from django.core.mail.backends.smtp import EmailBackend
from .utils import get_user_auth_info

class OauthEmailBackend(EmailBackend):
    def __init__(self, fail_silently=False, timeout=None, **kwargs):
        self.user = kwargs.pop('user', None)
        self.authinfo=self.auth_info()
        super(OauthEmailBackend, self).__init__(host=self.authinfo["host"], port=self.authinfo["port"], use_tls=True, fail_silently=fail_silently, timeout=timeout, **kwargs)

    def auth_info(self):
        return get_user_auth_info(self.user);    

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        connection_class = smtplib.SMTP
        # If local_hostname is not specified, socket.getfqdn() gets used.
        # For performance, we use the cached FQDN for local_hostname.
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
        try:
            self.connection = connection_class(self.host, self.port, **connection_params)
            self.connection.set_debuglevel(settings.DEBUG)

            self.connection.ehlo()
            self.connection.starttls()
            self.connection.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(self.authinfo["auth_string"]))
            
            self.connection.ehlo()
            return True
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            
            
    def send_messages(self, email_messages):
        for message in email_messages:
            message.from_email="{0} {1} <{2}> ".format(self.user.first_name,self.user.last_name,self.user.email)
            
        return  super(OauthEmailBackend, self).send_messages(email_messages)
