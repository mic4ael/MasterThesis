from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, View

from dynforms.forms import LoginForm, RegistrationForm
from dynforms.models import Language
from masterthesis import settings


class LoginView(TemplateView):
    template_name = 'dynforms/login.html'

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            form_data = login_form.cleaned_data
            authenticated_user = authenticate(username=form_data['username'],
                                              password=form_data['password'])
            if authenticated_user:
                login(request, authenticated_user)
                redirect_url = settings.LOGIN_REDIRECT_URL
                if request.GET.get('next'):
                    redirect_url = request.GET['next']
                return HttpResponseRedirect(redirect_url)
        return render(request, self.template_name, {'form': login_form})

    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm()})


class LogoutView(LoginRequiredMixin, View):
    def _logout_user(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

    def get(self, request):
        return self._logout_user(request)

    def post(self, request):
        return self._logout_user(request)


class RegistrationView(TemplateView):
    template_name = 'dynforms/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            translator_account = User.objects.create_user(**form.cleaned_data)
            permission_to_translate = Permission.objects.get(codename='can_translate_forms')
            translator_account.user_permissions.add(permission_to_translate)
            translator_account.save()
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dynforms/home.html'


class LanguagesView(LoginRequiredMixin, TemplateView):
    template_name = 'dynforms/languages.html'

    def get_context_data(self, **kwargs):
        context = super(LanguagesView, self).get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context
