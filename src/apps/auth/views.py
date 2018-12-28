from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.views import View
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from apps.auth.tokens import account_activation_token
from apps.auth.forms import SignUpForm


class SignUpView(View):

    def get(self, request):
        return render(request, 'auth/registration.html',
                      {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'auth/registration.html', {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            print(uidb64)
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('signup')
        else:
            # invalid link
            return render(request, 'auth/base.html')
