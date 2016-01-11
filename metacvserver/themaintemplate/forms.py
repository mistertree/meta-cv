from random import randint

from django.utils.translation import ugettext as _
from django.forms import ChoiceField, Form, ValidationError
from django.contrib.humanize.templatetags.humanize import ordinal
from django.conf import settings

class LetterField(ChoiceField):
    ALPHABET = [(letter, letter) for letter in "abcdefghijklmnopqrstuvwxyz"]
    def __init__(self, letter_position, *args, **kwargs):
        super(LetterField, self).__init__(choices = LetterField.ALPHABET,
            label=_("%s letter ") % ordinal(letter_position+1),
            initial='--', *args, **kwargs)
        self.letter_position = letter_position

    def validate(self, value):
        if settings.FIRST_NAME[self.letter_position].lower() != value.lower():
            raise ValidationError(_(
                "{value} is not the {position} letter in my first name.").format(
                    value = value,
                    position = ordinal(self.letter_position + 1)
                ))

class NameCaptchaForm(Form):
    def __init__(self, session, *args, **kwargs):
        super(NameCaptchaForm, self).__init__(*args, **kwargs)
        self.session = session
        if not self.session.has_key('namecaptchaform_letters'):
            self.session['namecaptchaform_letters'] = [
                randint(0, len(settings.FIRST_NAME)-1) for i in range(0,2) 
            ]

        self.fields.update({
            _("letter_%s") % (i+1) : LetterField(l)\
            for i, l in enumerate(self.session['namecaptchaform_letters'])
        })

    def is_valid(self, *args, **kwargs):
        is_valid = super(NameCaptchaForm, self).is_valid(*args, **kwargs)
        if is_valid:
            del self.session['namecaptchaform_letters']
        return is_valid
