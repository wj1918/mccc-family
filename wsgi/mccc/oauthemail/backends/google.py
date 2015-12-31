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
            'display_name': response.get("displayName"), 
            'token_type': response.get("token_type"),
            'access_token': response.get("access_token"),
        })
        
