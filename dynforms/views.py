import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView, View

from dynforms.forms import (LoginForm, RegistrationForm, NewLanguageForm,
                            NewFormTemplateForm)
from dynforms.models import Language, FormModel, FormField
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


def _login_url(self):
    if self.request.user.is_authenticated:
        return reverse('forms')
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
            languages = form.cleaned_data.pop('languages')
            new_form = FormModel.objects.create(**form.cleaned_data)
            for lang in languages:
                new_form.languages.add(lang)
            new_form.save()
            return HttpResponseRedirect(reverse('forms'))
        return render(request, self.template_name, {'form': form})


class EditFormsView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/edit_form.html'

    def get_context_data(self, **kwargs):
        context = super(EditFormsView, self).get_context_data(**kwargs)
        forms_model = FormModel.objects.get(pk=self.kwargs['forms_id'])
        initial_data = {'name': forms_model.name, 'description': forms_model.description,
                        'max_submissions': forms_model.max_submissions, 'languages': forms_model.languages.all()}
        context['form'] = NewFormTemplateForm(initial=initial_data)
        return context

    def post(self, request, forms_id):
        form = NewFormTemplateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            forms_model = FormModel.objects.get(pk=forms_id)
            forms_model.name = cleaned_data['name']
            forms_model.description = cleaned_data['description']
            forms_model.max_submissions = cleaned_data['max_submissions']
            forms_model.languages = cleaned_data['languages']
            forms_model.save()
            return HttpResponseRedirect(reverse('forms'))
        return render(request, self.template_name, {'form': form})

    def delete(self, request, forms_id):
        forms_model = get_object_or_404(FormModel, pk=forms_id)
        forms_model.delete()
        return JsonResponse({'success': True})


class FormsTemplateView(LoginRequiredMixin, UserIsSuperAdminTest, TemplateView):
    template_name = 'dynforms/forms_template.html'

    def get_context_data(self, **kwargs):
        context = super(FormsTemplateView, self).get_context_data(**kwargs)
        context['form_model'] = FormModel.objects.get(pk=self.kwargs['forms_id'])
        return context

    def post(self, request, forms_id):
        fields = json.loads(request.POST['fields'])
        form_model = get_object_or_404(FormModel, pk=forms_id)
        response = []
        for field in fields:
            if field['id'] is None:
                field_to_save = FormField()
                field_to_save.form = form_model
            else:
                field_to_save = get_object_or_404(FormField, pk=field['id'])

            field_to_save.field_type = field['type']
            field_to_save.field_label = field['label']
            field_to_save.field_placeholder = field.get('placeholder')
            field_to_save.field_required = field.get('required', False)
            field_to_save.save()
            response.append(field_to_save.as_dict())

        return JsonResponse({'success': True, 'fields': json.dumps(response)})
