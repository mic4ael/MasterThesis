from django.views.generic.base import TemplateView


class LoginView(TemplateView):
    template_name = 'dynforms/login.html'

