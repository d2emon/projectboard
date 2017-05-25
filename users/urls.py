from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    # (r'^accounts/logout/$', 'logout'),
    # (r'^accounts/profile/$', 'profile'),
    # (r'^accounts/settings/$', 'settings'),
    # url(r'^auth/', include('django.contrib.auth')),
    # (r'^accounts/', include('registration.backends.default.urls')),
    # (r'^(?P<project_name>\w+)/user/(?P<username>\w+)/$', 'user_details'),

    # Dummy views
    url(r'^list$', views.login, name='list'),
    url(r'^settings$', views.login, name='settings'),
    url(r'^notifications(?:/(?P<filter>\w+))?$', views.notify, name='notify'),
    url(r'^payments$', views.login, name='payments'),
    url(r'^projects$', views.login, name='projects'),
    url(r'^pins$', views.login, name='pins'),
    url(r'^profile$', views.login, name='profile'),
    url(r'^lock$', views.login, name='lock'),
    url(r'^logout$', views.login, name='logout'),
    url(r'^chat$', views.login, name='chat'),
]
