from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'


class ChatView(TemplateView):
    template_name = 'chat.html'
