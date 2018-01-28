from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class SpecialCharactersPasswordValidator(object):
    """Validator checks to see if a special
    character exists per the list below"""
    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain '
                                    'at least on special character'))

    def get_help_text(self):
        return "Your password must contain " \
               "at least on special character."


class CaseSensitivityPasswordValidator(object):
    """Validator checks to see if a password contains
    both an upper and lowercase letter"""
    def validate(self, password, user=None):
        uppers = [letter for letter in password if letter.isupper()]
        lowers = [letter for letter in password if letter.islower()]
        if len(uppers) == 0 or len(lowers) == 0:
            raise ValidationError(_('Password must contain at least '
                                    'one upper or lowercase letter.'))

    def get_help_text(self):
        return "Your password must contain at least " \
               "one upper or lowercase letter."


class NumericalDigitPasswordValidator(object):
    """Validator checks to see that there is at least one
    numerical digit in password"""
    def validate(self, password, user=None):
        numbers = [letter for letter in password if letter.isdigit()]
        if len(numbers) == 0:
            raise ValidationError(_('Password must contain '
                                    'at least one number.'))

    def get_help_text(self):
        return "Your password must contain at least " \
               "one numerical digit."


class CantBeSameAsOldPasswordValidator(object):
    def validate(self, password, user=None):
        pass

    def get_help_text(self):
        return "Your password must not be the same " \
               "as your current password."
