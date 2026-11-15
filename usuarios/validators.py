import re

from django.core.exceptions import ValidationError


class ComposicionPasswordValidator:

    def validate(self, password, user=None):
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra.')
        if not re.search(r'\d', password):
            raise ValidationError('La contraseña debe contener al menos un dígito.')
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')

    def get_help_text(self):
        return 'La contraseña debe contener al menos una letra, un número y un carácter especial.'