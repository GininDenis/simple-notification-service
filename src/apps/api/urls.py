from django.urls import path, include
from rest_framework import routers

from apps.api.views import (
    TestEndpointView, ConfirmSubscriptionApiView, SubscriptionViewSet
)

router = routers.DefaultRouter()
router.register('subscription', SubscriptionViewSet, base_name='subscription')

app_name = 'api'

urlpatterns = [

    path('', include(router.urls)),
    path('test/endpoint/', TestEndpointView.as_view(), name='test-endpoint'),
    path('confirm/subscription/', ConfirmSubscriptionApiView.as_view(), name='subscription-confirm'),

]
