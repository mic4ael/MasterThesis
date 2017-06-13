from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView, View

from dynforms.forms import (LoginForm, RegistrationForm, NewLanguageForm,
                            NewFormTemplateForm)
from dynforms.models import Language, FormModel
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


def _login_url(self):
    if self.request.user.is_authenticated:
        return reverse('home')
    else:
        return reverse('login')


class UserIsSuperAdminTest(UserPassesTestMixin):
    redirect_field_name = None

    def test_func(self):
        return self.request.user.is_superuser

    login_url = property(_login_url)


class LanguagesView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/languages.html'

    def get_context_data(self, **kwargs):
        context = super(LanguagesView, self).get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context

    def post(self, request):
        form = NewLanguageForm(request.POST)
        if form.is_valid():
            Language.objects.create(**form.cleaned_data).save()
        return HttpResponseRedirect(reverse('languages'))

    def delete(self, request):
        pass


class FormsView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/forms.html'

    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context['forms'] = FormModel.objects.all()
        return context


class NewFormsView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/create_form.html'

    def get_context_data(self, **kwargs):
        context = super(NewFormsView, self).get_context_data(**kwargs)
        context['form'] = NewFormTemplateForm()
        return context

    def post(self, request):
        form = NewFormTemplateForm(request.POST)
        if form.is_valid():
            FormModel.objects.create(**form.cleaned_data).save()
            return HttpResponseRedirect(reverse('forms'))
        return render(request, self.template_name, {'form': form})


class FormsDetailsView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/forms_details.html'

    def get_context_data(self, **kwargs):
        context = super(FormsDetailsView, self).get_context_data(**kwargs)
        context['form_model'] = FormModel.objects.get(pk=self.kwargs['forms_id'])
        return context
