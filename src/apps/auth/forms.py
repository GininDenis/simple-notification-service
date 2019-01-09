from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text=_('Optional.'), label=_('First name'))
    last_name = forms.CharField(max_length=30, required=False,
                                help_text=_('Optional.'), label=_('Last name'))
    email = forms.EmailField(max_length=254, help_text=_(
        'Required. Inform a valid email address.'), label=_('Email address'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_(u'Email addresses must be unique.'))
        return email
