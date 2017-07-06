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
    url(r'^', include(router.urls)),
    url(r'^project-users$', views.InviteList.as_view(), name='invite-1ist'),
    # url(r'^invites1234$', views.InviteModel.as_view(), name='invite-list'),
]
