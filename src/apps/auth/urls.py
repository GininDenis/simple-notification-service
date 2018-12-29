from django.urls import path

from apps.auth.views import SignUpView, ActivateAccountView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='signup'),
    path('activate/(<str:uidb64>)/(<str:token>)/',
        ActivateAccountView.as_view(), name='activate'),
]
