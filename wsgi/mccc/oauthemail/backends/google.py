from social.backends.google import GoogleOAuth2
from social.utils import handle_http_errors

class GmailOAuth2(GoogleOAuth2):
    name = 'gmail-oauth2'
    
    def start(self):
        return self.strategy.redirect(self.auth_url())

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        state = self.validate_state()
        self.process_error(self.data)
