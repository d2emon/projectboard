from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    # (r'^accounts/logout/$', 'logout'),
    # (r'^accounts/profile/$', 'profile'),
    # (r'^accounts/settings/$', 'settings'),
    # url(r'^auth/', include('django.contrib.auth')),
    # (r'^accounts/', include('registration.backends.default.urls')),
    # (r'^(?P<project_name>\w+)/user/(?P<username>\w+)/$', 'user_details'),
]
