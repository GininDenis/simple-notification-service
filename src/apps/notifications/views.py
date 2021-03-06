from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib import messages

from apps.notifications.models import Topic, Subscription
from apps.notifications.forms import SubscriptionUpdateForm
from apps.notifications.tokens import subscription_activation_token


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'dashboard/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.topics.all().order_by('title')


class TopicUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Topic
    template_name = 'dashboard/topic_update.html'
    fields = ['title']
    success_url = reverse_lazy('notifications:topic-list')
    success_message = _('Topic updated successfully.')

    def get_queryset(self):
        return self.request.user.topics.all()


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'dashboard/topic_create.html'
    fields = ['title']
    success_url = reverse_lazy('notifications:topic-list')
    success_message = _('Topic created successfully.')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'dashboard/subscription_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 10

    def get_queryset(self):
        return Subscription.objects.filter(
            topic__owner=self.request.user).order_by('topic')


class SubscriptionUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                             UpdateView):
    model = Subscription
    template_name = 'dashboard/subscription_update.html'
    success_url = reverse_lazy('notifications:subscription-list')
    success_message = _('Subscription updated successfully.')
    form_class = SubscriptionUpdateForm

    def get_queryset(self):
        return Subscription.objects.filter(topic__owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SubscriptionCreateView(SuccessMessageMixin, LoginRequiredMixin,
                             CreateView):
    model = Subscription
    template_name = 'dashboard/subscription_create.html'
    form_class = SubscriptionUpdateForm
    success_url = reverse_lazy('notifications:subscription-list')
    success_message = _('Subscription created successfully.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SubscriptionRemoveView(LoginRequiredMixin, DeleteView):
    model = Subscription
    template_name = 'dashboard/subscription_delete.html'
    success_url = reverse_lazy('notifications:subscription-list')
    success_message = _('Subscription deleted successfully.')

    def get_queryset(self):
        return Subscription.objects.filter(topic__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SubscriptionConfirmView(View):

    redirect_url = reverse_lazy('users:index')

    def post(self, uid, token):
        try:
            id = force_text(urlsafe_base64_decode(uid))
            subscription = Subscription.objects.get(pk=id)
        except (
        TypeError, ValueError, OverflowError, Subscription.DoesNotExist):
            subscription = None

        if subscription is not None and subscription_activation_token.check_token(
                subscription,
                token):
            subscription.status = Subscription.STATUS_CHOICES.confirmed
            subscription.save()
        return HttpResponseRedirect(self.redirect_url)
