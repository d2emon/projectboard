from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from users.serializers import UserSerializer, GroupSerializer
from projects.models import Project, ProjectUser, Log, Notice, TodoList
from projects.serializers import ProjectSerializer, LogSerializer, NoticeSerializer, TodoListSerializer, InviteUserSerializer, ProjectUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # lookup_field = 'username'


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
    lookup_field = 'slug'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows project users to be viewed or edited
    """
    # queryset = ProjectUser.objects.all()
    serializer_class = InviteUserSerializer

    def get_queryset(self):
        projectname = self.request.GET.get('projectname')
        if projectname is None:
            projectname = self.request.data.get('projectname')

        if projectname:
            project = get_object_or_404(Project, slug=projectname)
            return ProjectUser.objects.filter(project=project).all()
        return ProjectUser.objects.all()

    @list_route()
    def list_invites(self, request, format=None):
        projectname = request.GET.get('projectname')
        if projectname is None:
            project_users = ProjectUser.objects.all()
            serializer = self.get_serializer(project_users, many=True)
            return Response(serializer.data)

        project = get_object_or_404(Project, slug=projectname)
        serializer = ProjectUserSerializer(
            project,
            context={'request': request}
        )
        return Response(serializer.data)

    @detail_route(methods=['put', ])
    def accept(self, request, pk=None, format=None):
        projectname = self.request.data.get('projectname')
        project = get_object_or_404(Project, slug=projectname)
        username = self.request.data.get('username')
        user = get_object_or_404(User, username=username)
        project_user = ProjectUser.objects.filter(project=project, user=user).first()
        if project_user is None:
            project_user = get_object_or_404(ProjectUser, pk)

        serializer = InviteUserSerializer(
            project_user,
            context={'request': request}
        )
        return Response(serializer.data)

    @detail_route(methods=['delete', ])
    def decline(self, request, pk=None, format=None):
        projectname = self.request.data.get('projectname')
        project = get_object_or_404(Project, slug=projectname)
        username = self.request.data.get('username')
        user = get_object_or_404(User, username=username)
        project_user = ProjectUser.objects.filter(project=project, user=user).first()
        if project_user is None:
            project_user = get_object_or_404(ProjectUser, pk)

        serializer = InviteUserSerializer(
            project_user,
            context={'request': request}
        )
        return Response(serializer.data)


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


class InviteModel(APIView):
    """
    Aceept or decline invitations, get user status.
    """
    serializer_class = InviteUserSerializer

    def put(self, request, projectname=None, username=None, format=None):
        projectname = request.data.get('projectname')
        project = get_object_or_404(Project, slug=projectname)

        username = request.data.get('username')
        user = User.objects.get(username=username)

        invited_user = ProjectUser.objects.filter(
            project=project,
            user=user,
            status=ProjectUser.STATUS_INVITED
        ).first()

        # if not (access == 'Owner'):
        #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
        # inviteform = bforms.InviteUserForm(project, request.POST)
        # if inviteform.is_valid():
        #     inviteform.save()
        if not project.allowed(request.user):
            raise PermissionDenied

        if ProjectUser.objects.filter(
            project=project,
            user_id=user.id,
            status__in=[
                ProjectUser.STATUS_INVITED,
                ProjectUser.STATUS_ACCEPTED,
            ],
        ).count():
            raise Exception("user allready invited")

        project_user = ProjectUser(
            project=project,
            user=user,
            status=ProjectUser.STATUS_INVITED,
        )

        serializer = ProjectUserSerializer(invited_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, projectname=None, username=None, format=None):
        projectname = request.GET.get('projectname')
        project = get_object_or_404(Project, slug=projectname)

        username = request.GET.get('username')
        user = User.objects.get(username=username)

        project_user = ProjectUser.objects.filter(
            project=project,
            user=user,
        ).first()
        serializer = ProjectUserSerializer(project_user, context={'request': request})
        return Response(serializer.data)

    def post(self, request, projectname=None, username=None, format=None):
        projectname = request.data.get('projectname')
        project = get_object_or_404(Project, slug=projectname)

        username = request.data.get('username')
        user = User.objects.get(username=username)

        invited_user = ProjectUser.objects.filter(
            project=project,
            user=user,
            status=ProjectUser.STATUS_INVITED
        ).first()

        if invited_user is None:
            raise Exception("User is not invited")

        invited_user.accept()
        invited_user.save()
        serializer = ProjectUserSerializer(
            invited_user,
            # many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, projectname=None, username=None, format=None):
        projectname = request.data.get('projectname')
        project = get_object_or_404(Project, slug=projectname)

        username = request.data.get('username')
        user = User.objects.get(username=username)

        invited_user = ProjectUser.objects.filter(
            project=project,
            user=user,
            status=ProjectUser.STATUS_INVITED
        ).first()

        if invited_user is None:
            raise Exception("User is not invited")

        invited_user.decline()
        invited_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
