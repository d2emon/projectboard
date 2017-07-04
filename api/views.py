from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from users.serializers import UserSerializer, GroupSerializer
from projects.models import Project, ProjectUser, Log, Notice, TodoList
from projects.serializers import ProjectSerializer, UserStatusSerializer, LogSerializer, NoticeSerializer, TodoListSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows project users to be viewed or edited
    """
    queryset = ProjectUser.objects.all()
    serializer_class = UserStatusSerializer


class LogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows logs to be viewed or edited
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notices to be viewed or edited
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todo lists to be viewed or edited
    """
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
