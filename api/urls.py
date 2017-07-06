from django.conf.urls import url, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'project_users', views.ProjectUserViewSet)
router.register(r'logs', views.LogViewSet)
router.register(r'notices', views.NoticeViewSet)
router.register(r'todo_lists', views.TodoListViewSet)
router.register(r'invites', views.InviteList, 'invites')


urlpatterns = [
    url(r'^invites1234$', views.InviteList.as_view(), name='invite_list'),
    url(r'^', include(router.urls), name='api'),
]
