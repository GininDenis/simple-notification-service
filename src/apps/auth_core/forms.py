from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from apps.auth_core.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text=_('Optional.'), label=_('First name'))
    last_name = forms.CharField(max_length=30, required=False,
                                help_text=_('Optional.'), label=_('Last name'))
    email = forms.EmailField(max_length=254, help_text=_(
        'Required. Inform a valid email address.'), label=_('Email address'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1',
                  'password2',)
