from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer, GroupSerializer
from projects.models import Project, ProjectUser, Log, Notice, TodoList
from projects.serializers import ProjectSerializer, UserStatusSerializer, LogSerializer, NoticeSerializer, TodoListSerializer, InviteUserSerializer, ProjectUserSerializer


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


class InviteList(APIView):
    """
    List all project users, or invite new user.
    """
    serializer_class = InviteUserSerializer

    def get(self, request, project_name=None, format=None):
        project_name = request.GET.get('project_name')
        project = get_object_or_404(Project, slug=project_name)
        # project_users = ProjectUser.objects.filter(project=project).all()
        serializer = ProjectUserSerializer(
            project,
            # many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, project_name=None, format=None):
        serializer = InviteUserSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
