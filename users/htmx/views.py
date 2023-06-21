from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from users.models import Notification


class UnreadNotificationsIconHTMXView(LoginRequiredMixin, TemplateView):
    model = Notification
    template_name = 'registration/htmx/unread_notifications_icon_htmx.html'

    def get_context_data(self, **kwargs):
        context = super(UnreadNotificationsIconHTMXView, self).get_context_data(**kwargs)
        context.update({'object_list_count': self.request.user.unread_notifications().count()})
        return context


class UnreadNotificationsHTMXView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'registration/htmx/unread_notifications_htmx.html'

    def get_queryset(self):
        pk_list = list(self.request.user.unread_notifications().values_list('pk', flat=True))
        queryset = Notification.objects.filter(pk__in=pk_list)
        queryset.update(read=True)
        return queryset
