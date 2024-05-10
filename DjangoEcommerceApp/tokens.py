from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type


class TokenGenerator (PasswordResetTokenGenerator):
   def _make_hash_value(self, user,timestrap):
       return(
                      text_type(user.pk) + text_type(timestrap)
             )
        
    
generate_token = TokenGenerator()