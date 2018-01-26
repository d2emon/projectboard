from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.project, name='createproject'),
    url(r'^(?P<project_name>[\w-]+)/$', views.project, name='project'),
    url(r'^(?P<project_name>[\w-]+)/invite/(?P<username>[\w]+)$', views.invitation, name='invitation'),
    url(r'^(?P<project_name>[\w-]+)/logs$', views.full_logs, name='logs'),
    url(r'^(?P<project_name>[\w-]+)/settings$', views.project_settings, name='settings'),
    url(r'^(?P<project_name>[\w-]+)/noticeboard$', views.noticeboard, name='noticeboard'),
    url(r'^(?P<project_name>[\w-]+)/todo$', views.todo, name='todo'),
    url(r'^(?P<project_name>[\w-]+)/from_git$', views.clone_from_git, name='from_git'),
    url(r'^(?P<project_name>[\w-]+)/setup.py$', views.setup_py, name='setup_py'),
]

# project.foo
# project.users
# project.json.task
# project.rss.proj_feed
# project.main
# project.tasks
# project.wiki
# project.metrics
# project.files
# project.pcalendar
