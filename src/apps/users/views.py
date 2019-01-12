from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views import View
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from apps.users.tokens import account_activation_token
from apps.users.forms import SignUpForm
from apps.users.models import User


class SignUpView(SuccessMessageMixin, FormView):

    form_class = SignUpForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:signin')
    success_message = 'User created successfully, activation email has been sent'

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('users/account_activation_email.html', {
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
            messages.add_message(request, messages.INFO,
                                 _('User activated successfully'))

        else:
            messages.add_message(request, messages.INFO,
                                 _('Invalid activation link'))
        return redirect(reverse_lazy('users:signin'))


class SignInView(LoginView):

    template_name = 'users/login.html'
    success_url = reverse_lazy('users:index')

    def get_success_url(self):
        return self.success_url


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users:signin')
    template_name = 'dashboard/index.html'
