from social.backends.google import GoogleOAuth2
from social.utils import handle_http_errors

class GmailOAuth2(GoogleOAuth2):
    name = 'gmail-oauth2'
    
    def start(self):
        return self.strategy.redirect(self.auth_url())

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        data = self.user_data(access_token, *args, **kwargs)
        response = kwargs.get('response') or {}
        response.update(data or {})
        kwargs.update({'response': response, 'backend': self})
        """ remove authenticate function in  GoogleOAuth2 """

        self.data.update( {
            'email': response["emails"][0]["value"], 
            'display_name': response["displayName"], 
            'token_type': response["token_type"],
            'access_token': response["access_token"],
        })
        
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
        
