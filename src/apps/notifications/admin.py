from django.contrib import admin

from apps.notifications.models import Topic, Subscription, Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'is_active')
    list_display_links = ('key', 'user', 'is_active')
    list_filter = ('user',)
    search_fields = ('key',)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner',)
    list_display_links = ('title', 'owner',)
    list_filter = ('owner',)
    search_fields = ('title', 'owner__first_name', 'owner__email',
                     'owner__username')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'status', 'endpoint')
    list_display_links = ('topic', 'status', 'endpoint')
    list_filter = ('topic',)
    search_fields = ('endpoint',)
    readonly_fields = ('status',)

admin.site.register(Token, TokenAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
