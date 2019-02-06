from django import forms

from apps.notifications.models import Subscription, Topic


class SubscriptionUpdateForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['topic', 'protocol', 'endpoint']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['topic'].widget.attrs['class'] = 'custom-select'
        self.fields['protocol'].widget.attrs['class'] = 'custom-select'
        self.fields['endpoint'].widget.attrs['class'] = 'form-control'
        self.fields['topic'].queryset = Topic.objects.filter(
            owner__id=self.current_user.id)
