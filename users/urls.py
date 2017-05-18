from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]

# (r'^accounts/login/$', 'login'),
# (r'^accounts/logout/$', 'logout'),
# (r'^accounts/profile/$', 'profile'),
# (r'^accounts/settings/$', 'settings'),
# (r'^accounts/', include('registration.backends.default.urls')),
# (r'^(?P<project_name>\w+)/user/(?P<username>\w+)/$', 'user_details'),
