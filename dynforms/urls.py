from django.conf.urls import url

from dynforms import views

urlpatterns = [
    url(r'^$', views.FormsView.as_view(), name='index'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),

    url(r'^languages$', views.LanguagesView.as_view(), name='languages'),
    url(r'^forms$', views.FormsView.as_view(), name='forms'),
    url(r'^forms/new$', views.NewFormsView.as_view(), name='new_forms_template'),
    url(r'^forms/(?P<forms_id>[0-9]+)$', views.EditFormsView.as_view(), name='manage_form'),
    url(r'^forms/template/(?P<forms_id>[0-9]+)$', views.FormsTemplateView.as_view(), name='forms_template'),
    url(r'^forms/submission/(?P<forms_id>[0-9]+)$', views.FormsSubmission.as_view(), name='forms_submission'),
    url(r'^forms/submissions/(?P<forms_id>[0-9]+)$', views.FormsSubmissions.as_view(), name='forms_submissions'),
    url(r'^forms/translations$', views.FormsTranslations.as_view(), name='forms_translations'),
    url(r'^forms/translations/(?P<translations_id>[0-9]+)$', views.FormsTranslationsEdit.as_view(),
        name='forms_translations_edit')
]
