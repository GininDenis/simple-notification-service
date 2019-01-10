from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views import View
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from apps.auth_core.tokens import account_activation_token
from apps.auth_core.forms import SignUpForm
from apps.auth_core.models import User


class SignUpView(SuccessMessageMixin, FormView):

    form_class = SignUpForm
    template_name = 'auth/registration.html'
    success_url = reverse_lazy('success')
    success_message = 'Used created successfully'

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('auth/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(user)
        return super().form_valid(form)


class ActivateAccountView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('signup')
        else:
            return render(request, 'auth/base.html')
