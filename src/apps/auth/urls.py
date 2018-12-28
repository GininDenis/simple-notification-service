from django.urls import path

from apps.auth.views import SignUpView, ActivateAccountView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        ActivateAccountView.as_view(), name='activate'),
]
