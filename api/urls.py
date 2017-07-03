from django.conf import settings
from django.conf.urls import url, include

from rest_framework import routers

from api import views
from projects import views as projects_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'projects', projects_views.ProjectViewSet)
router.register(r'project_users', projects_views.ProjectUserViewSet)
router.register(r'logs', projects_views.LogViewSet)
router.register(r'notices', projects_views.NoticeViewSet)
router.register(r'todo_lists', projects_views.TodoListViewSet)


urlpatterns = [
    url(r'^', include(router.urls), name='api'),
]
