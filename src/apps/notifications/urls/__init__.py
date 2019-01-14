from django.urls import path

from apps.notifications.views import (
    TopicListView, TopicUpdateView, TopicCreateView
)

app_name = 'notifications'

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/add/', TopicCreateView.as_view(), name='topic-add'),
    path('topics/<int:pk>/', TopicUpdateView.as_view(), name='topic-update'),
]
