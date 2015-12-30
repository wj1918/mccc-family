from social.backends.live import LiveOAuth2
from social.utils import handle_http_errors

class HotmailOAuth2(LiveOAuth2):
    name = 'hotmail-oauth2'
    
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

        #return response;
        self.data.update( {
            'email': response["emails"]["account"], 
            'display_name': response["name"], 
            'token_type': response["token_type"],
            'access_token': response["access_token"],
        })
        