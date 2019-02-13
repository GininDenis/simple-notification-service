from django.urls import path

from apps.notifications.views import (
    TopicListView, TopicUpdateView, TopicCreateView,
    SubscriptionListView, SubscriptionUpdateView, SubscriptionCreateView,
    SubscriptionRemoveView, SubscriptionConfirmView
)

app_name = 'notifications'

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/add/', TopicCreateView.as_view(), name='topic-add'),
    path('topics/<int:pk>/', TopicUpdateView.as_view(), name='topic-update'),
    path('subscriptions/', SubscriptionListView.as_view(),
         name='subscription-list'),
    path('subscriptions/add/', SubscriptionCreateView.as_view(),
         name='subscription-add'),
    path('subscriptions/<int:pk>/', SubscriptionUpdateView.as_view(),
         name='subscription-update'),
    path('subscriptions/remove/<int:pk>/', SubscriptionRemoveView.as_view(),
         name='subscription-remove'),
    path('subscriptions/confirm/<str:uid>/<str:token>/', SubscriptionConfirmView.as_view(),
         name='subscription-confirm'),
]
