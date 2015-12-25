from datetime import date

from django.conf import settings
from django.utils import six
from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import get_random_string

# changed from PasswordResetTokenGenerator

class AccessTokenGenerator(object):

    def make_token(self):
        return self._make_token_with_timestamp(self._num_days(self._today()))

    def check_token(self, token):
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check the timestamp is within limit
        if (self._num_days(self._today()) - ts) > settings.ACCESS_TOKEN_EXPIRATION_DAYS:
            return False

        # TODO: Check if token is valid
        #if not is_token_valid(token):
        #    return False

        return True

    def _make_token_with_timestamp(self, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        random_string = get_random_string()
        return "%s-%s" % (ts_b36, random_string)

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()

access_token_generator = AccessTokenGenerator()