from django.urls import path

from apps.auth.views import signup

urlpatterns = [
    path('register/', signup, name='signup')
]