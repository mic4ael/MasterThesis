from django.conf.urls import url

from dynforms import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),

    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^languages$', views.LanguagesView.as_view(), name='languages'),
    url(r'^forms$', views.FormsView.as_view(), name='forms'),
    url(r'^forms/new$', views.NewFormsView.as_view(), name='new_forms_template'),
    url(r'^forms/(?P<forms_id>[0-9]+)$$', views.FormsDetails.as_view(), name='forms_details')
]
