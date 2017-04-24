from django.conf.urls import url

from dynforms import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),

    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^languages$', views.LanguagesView.as_view(), name='languages'),
]
