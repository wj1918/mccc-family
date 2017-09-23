"""
Fix 
https://github.com/omab/python-social-auth/issues/483
"""

from social_core.backends.live import LiveOAuth2

class LiveConnect(LiveOAuth2):
    REDIRECT_STATE = False
