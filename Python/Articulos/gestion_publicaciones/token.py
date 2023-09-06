from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class GeneradorToken(PasswordResetTokenGenerator):

    def _make_hash_value(self, revision, timestamp):
        return six.text_type(revision.id) + six.text_type(timestamp)


token_estado = GeneradorToken()
