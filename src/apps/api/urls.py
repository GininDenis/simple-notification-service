from django.urls import path

from apps.api.views import SubscriptionConfirmView, TestEndpointView

app_name = 'api'

urlpatterns = [

    path('subscription/confirm/<str:token>/',
         SubscriptionConfirmView.as_view(), name='subscription-confirm'),
    path('test/endpoint/',
         TestEndpointView.as_view(), name='test-endpoint')

]
