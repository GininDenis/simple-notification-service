from django.urls import path, include
from rest_framework import routers

from apps.api.views import (
    TestEndpointApiView, LoginApiView, LogoutApiView, RestoreSessionApiView
)
from apps.api.viewsets import SubscriptionViewSet, TopicViewSet

router = routers.DefaultRouter()
router.register('subscriptions', SubscriptionViewSet, base_name='subscriptions')
router.register('topics', TopicViewSet, base_name='topics')

app_name = 'api'

urlpatterns = [

    path('', include(router.urls)),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('restore/session', RestoreSessionApiView.as_view(), name='restore-session'),
    path('test/endpoint/', TestEndpointApiView.as_view(), name='test-endpoint'),

]
