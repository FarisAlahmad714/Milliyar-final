import smtplib
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class CustomSMTPBackend(DjangoSMTPBackend):
    """
    Custom SMTP backend to fix Django 2.2 compatibility with newer Python versions.
    Fixes the 'keyfile' argument error in SMTP.starttls().
    """
    
    def open(self):
        """
        Ensure an open connection to the email server. Return whether or not a
        new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        
        connection_params = {}
        if hasattr(self, 'local_hostname') and self.local_hostname:
            connection_params['local_hostname'] = self.local_hostname
        if hasattr(self, 'timeout') and self.timeout is not None:
            connection_params['timeout'] = self.timeout
            
        if self.use_ssl:
            if hasattr(self, 'ssl_keyfile') and self.ssl_keyfile:
                connection_params['keyfile'] = self.ssl_keyfile
            if hasattr(self, 'ssl_certfile') and self.ssl_certfile:
                connection_params['certfile'] = self.ssl_certfile
            if hasattr(smtplib, 'SMTP_SSL'):
                self.connection = smtplib.SMTP_SSL(self.host, self.port, **connection_params)
            else:
                raise RuntimeError("SSL not supported by your Python installation")
        else:
            self.connection = smtplib.SMTP(self.host, self.port, **connection_params)
        
        # TLS/STARTTLS are mutually exclusive, so only attempt TLS over
        # non-secure connections.
        if not self.use_ssl and self.use_tls:
            # Try with starttls() without parameters first (newer Python compatibility)
            try:
                self.connection.starttls()
            except Exception:
                # If that fails, try the old way with parameters
                tls_params = {}
                if hasattr(self, 'ssl_keyfile') and self.ssl_keyfile:
                    tls_params['keyfile'] = self.ssl_keyfile
                if hasattr(self, 'ssl_certfile') and self.ssl_certfile:
                    tls_params['certfile'] = self.ssl_certfile
                self.connection.starttls(**tls_params)
        
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True