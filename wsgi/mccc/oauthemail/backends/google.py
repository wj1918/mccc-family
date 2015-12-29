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

    @handle_http_errors
    def get_access_token(self, state, code):
        self.data ['code']=code
        response = self.request_access_token(
            self.access_token_url(),
            data=self.auth_complete_params(state),
            headers=self.auth_headers(),
            auth=self.auth_complete_credentials(),
            method=self.ACCESS_TOKEN_METHOD
        )
        self.process_error(response)
        return response['access_token']
        
