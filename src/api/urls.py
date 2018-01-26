from django.conf.urls import url, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
# router.register(r'main', views.MainViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'project_users', views.ProjectUserViewSet, base_name='invites')
router.register(r'logs', views.LogViewSet)
router.register(r'notices', views.NoticeViewSet)
router.register(r'todo_lists', views.TodoListViewSet)
# router.register(r'invites', views.InviteModel.as_view(), 'projectuser-detail')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^main$', views.MainView.as_view(), name='api-main'),
    url(r'^invites1234$', views.InviteModel.as_view(), name='projectuser-detail'),
    url(r'^project-users$', views.InviteList.as_view(), name='invite-1ist'),
]
