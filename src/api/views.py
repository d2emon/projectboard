from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from django.core import serializers
# from django.forms.models import model_to_dict

from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from users.serializers import UserSerializer, GroupSerializer
from projects.models import Project, ProjectUser, Log, Notice, TodoList
from projects.serializers import ProjectSerializer, LogSerializer, NoticeSerializer, TodoListSerializer, InviteUserSerializer, ProjectUserSerializer

import random

class MainView(APIView):
    """
    The point of entry for a logged in user.
    Shows the available active projects for the user, and allows him to create one.
    Shows the pending invites to other projects.
    Shows very critical information about available projects.
    """
    serializer_class = InviteUserSerializer

    def get(self, request, project_name=None, format=None):
        # if request.user.is_authenticated():
        #   return HttpResponseRedirect('/dashboard/')
        # if request.method == 'POST':
        #   return login(request)
        # register_form = bforms.UserCreationForm(prefix='register')
        # login_form = bforms.LoginForm()
        # request.session.set_test_cookie()

        usernames = [
            'Yiorgos Avraamu',
            'Avram Tarasios',
            'Quintin Ed',
            'Enéas Kwadwo',
            'Agapetus Tadeáš',
            'Friderik Dávid',
        ]
        dates = [
            '',
            'Jan 1, 2015',
            '10 sec ago',
            '5 minutes ago',
            '1 hour ago',
            'Last month',
            'Last week',
        ]
        statuses = [
            '',
            'success',
            'danger',
            'warning',
        ]
        countries = [
            { 'name': 'Russia', 'flag': 'ru' },
            { 'name': 'USA', 'flag': 'us' },
            { 'name': 'Brazil', 'flag': 'br' },
            { 'name': 'India', 'flag': 'in' },
            { 'name': 'France', 'flag': 'fr' },
            { 'name': 'Spain', 'flag': 'es' },
            { 'name': 'Poland', 'flag': 'pl' },
        ]

        users = [{
            'name': random.choice(usernames),
            'new': random.randint(0, 1) > 0,
            'registered': random.choice(dates),
            'avatar': '/media/avatars/' + str(random.randint(1, 6)) + '.jpg',
            'status': random.choice(statuses),
            'country': random.choice(countries),
        } for i in range(10)]

        tasks = [{
            'id': i + 1,
            'name': 'Task' + str(i + 1),
            'url': '/project/task',
            'url_edit': '/project/task/edit',
            'url_del': '/project/task/delete',
            'expected_start_date': random.choice(dates),
            'expected_end_date': random.choice(dates),
            'actual_start_date': random.choice(dates),
            'actual_end_date': random.choice(dates),
            'user': random.choice(users),
            'project': None,
            'is_complete': random.randint(0, 1) > 0,
            'progress': random.randrange(100),
        } for i in range(25)]

        projects = request.user.projectuser_set.order_by('-project__start_date')
        subs = []
        for p in projects:
            project = p.project
            subs.append({
                'shortname': project.slug,
                'name': project.name,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'url': '/project',
                'is_active': project.is_active,
                'tasks': [],
                'overdue_tasks': [],
                'invites': [],
                'users': [{
                    'name': random.choice(usernames),
                    'new': random.randint(0, 1) > 0,
                    'registered': random.choice(dates),
                    'avatar': 'static/img/avatars/' + str(random.randint(1, 6)) + '.jpg',
                    'status': random.choice(statuses),
                    'country': random.choice(countries),
                } for i in range(random.randint(1, 10))],

                'description': project.description,
                'created_on': project.created_on,
                'git': project.git,
                'uri': project.uri,
                'owner': {
                  'username': project.owner.username,
                  'email': project.owner.email,
                  # 'groups': project.owner.groups,
                  # 'profile': project.owner.profile,
                },
            })
        #    #    "owner": {
        #    #        "url": "http://localhost:8000/api/users/11/",
        #    #        "username": "ljudmila02",
        #    #        "email": "jakovblinov@rambler.ru",
        #    #        "groups": [],
        #    #        "profile": {
        #    #            "avatar": "http://localhost:8000/media/avatars/4.jpg"
        #    #        }
        #    #    }

        invites = []
        for i in range(10):
            for i in range(5):
                user = random.choice(users)
                # project['invites'].append(user)
                invites.append({
                    'id': i + 1,
                    'project': random.choice(subs),
                    'user': user
                })
            # projects.append(project)

        for task in tasks:
            project = random.choice(subs)
            # task['project'] = project
            project['tasks'].append(task)
            project['overdue_tasks'].append(task)
        invites = invites
        # ----
        # user = request.user
        # if request.GET.get('includeinactive', 0):
        #     subs = user.subscribeduser_set.all()
        # else:
        #     subs = user.subscribeduser_set.filter(project__is_active = True)
        # invites = user.inviteduser_set.filter(rejected = False)
        # createform = bforms.CreateProjectForm()

        # if request.method == 'POST':
        #     if request.POST.has_key('createproject'):
        #         createform = bforms.CreateProjectForm(user, request.POST)
        #         if createform.is_valid():
        #             createform.save()
        #             return HttpResponseRedirect('.')
        #     elif request.POST.has_key('acceptinv'):
        #         project = Project.objects.get(id = request.POST['projid'])
        #         invite = InvitedUser.objects.get(id = request.POST['invid'])
        #         subscribe = SubscribedUser(project = project, user = user, group = invite.group)
        #         subscribe.save()
        #         invite.delete()
        #         return HttpResponseRedirect('.')
        #     elif request.POST.has_key('activestatus'):
        #         projid = request.POST['projectid']
        #         project = Project.objects.get(id = projid)
        #         if request.POST['activestatus'] == 'true':
        #             project.is_active = False
        #         elif request.POST['activestatus'] == 'false':
        #             project.is_active = True
        #         project.save()
        #         return HttpResponseRedirect('.')
        #     elif request.POST.has_key('markdone'):
        #         print request.POST
        #         handle_task_status(request)

        # elif request.method == 'GET':
        createform = "bforms.CreateProjectForm()"

        return Response({
          'subs': subs,
          'createform':createform,
          'invites':invites,
          'template': "project/dashboard.html",
          'tasks': tasks,
        })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # lookup_fsield = 'username'


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

    def get_project_user(self):
        projectname = self.request.data.get('projectname')
        username = self.request.data.get('username')
        # project = get_object_or_404(Project, slug=projectname)
        # user = get_object_or_404(User, username=username)
        project = Project.objects.filter(slug=projectname).first()
        user = User.objects.filter(username=username).first()
        if project is None or user is None:
            project_user = None
            # ProjectUser(
            #     project=project,
            #     user=user,
            #     status=0
            # )
        else:
            project_user = ProjectUser.objects.filter(project=project, user=user).first()
        return project_user

    # @detail_route(methods=['put', ])
    @list_route(methods=['get', 'post', ])
    def accept(self, request, pk=None, format=None):
        project_user = self.get_project_user()
        if project_user is None:
            return Response({"errors": 1})

        project_user.status = ProjectUser.STATUS_ACCEPTED
        project_user.save()
        serializer = InviteUserSerializer(
            project_user,
            context={'request': request}
        )
        return Response(serializer.data)

    # @detail_route(methods=['delete', ])
    @list_route(methods=['get', 'post', ])
    def decline(self, request, pk=None, format=None):
        project_user = self.get_project_user()
        if project_user is None:
            return Response({"errors": 1})

        project_user.status = ProjectUser.STATUS_DECLINED
        project_user.save()
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
