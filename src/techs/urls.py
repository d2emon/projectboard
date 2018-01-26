from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<language>[\w-]+)/$', views.language, name='language'),
]
