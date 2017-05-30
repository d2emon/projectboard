from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^(?P<project_name>\w+)/$', views.project, name='project'),
    url(r'^create/$', views.createproject, name='createproject'),
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
#
# (r'^foo/$', TemplateView.as_view(template_name='project/dummy.html')),
# (r'^admin/', include(admin.site.urls)),
# (r'^dashboard/$', 'dashboard'),
# (r'^(?P<project_name>\w+)/$', 'project_details'),
# (r'^(?P<project_name>\w+)/settings/$', 'settings'),
# (r'^(?P<project_name>\w+)/logs/$', 'full_logs'),
# (r'^(?P<project_name>\w+)/noticeboard/$', 'noticeboard'),
# (r'^(?P<project_name>\w+)/todo/$', 'todo'),
#
