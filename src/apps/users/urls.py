from django.urls import path

from apps.users.views import SignUpView, SignInView, ActivateAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('activate/<str:uidb64>/<str:token>/',
        ActivateAccountView.as_view(), name='activate'),
]
