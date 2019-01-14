from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView

from apps.notifications.models import Topic

class TopicListView(LoginRequiredMixin, ListView):

    model = Topic
    template_name = 'dashboard/topic_list.html'
    ordering = ['title']
    context_object_name = 'topics'
    paginate_by = 10
    login_url = reverse_lazy('users:signin')

    def get_queryset(self):
        return self.request.user.topics.all()


class TopicUpdateView(LoginRequiredMixin, UpdateView):

    model = Topic
    template_name = 'dashboard/topic_update.html'
    fields = ['title']
    success_url = reverse_lazy('notifications:topic-list')
    login_url = reverse_lazy('users:signin')


class TopicCreateView(LoginRequiredMixin, CreateView):

    model = Topic
    template_name = 'dashboard/topic_update.html'
    fields = ['title']
    success_url = reverse_lazy('notifications:topic-list')
    login_url = reverse_lazy('users:signin')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())