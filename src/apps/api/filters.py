from django_filters import rest_framework as filters
from apps.notifications.models import Topic


class TopicFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = ['title']
