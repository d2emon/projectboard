from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CreateProjectForm, InviteUserForm, AddNoticeForm, AddTodoListForm
from .models import Project, ProjectUser, Log, Notice, TodoList
from .serializers import ProjectSerializer, ProjectUserSerializer, LogSerializer, NoticeSerializer, TodoListSerializer

import users.views


def add_pager(objects, request):
    paginator = Paginator(objects, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items, page


def get_allowed_project(slug, user):
    project = get_object_or_404(Project, slug=slug)  # Only subscribed
    access = project.allowed(user)
    if not access:
        raise PermissionDenied
    return project


def index(request):
    """
    If the user is not logged in, show him the login/register forms, with some
    blurb about the services. Else redirect to /dashboard/
    """
    if request.user.is_authenticated():
        return redirect('projects:dashboard')
    if request.method == 'POST':
        return users.views.login(request)

    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    # request.session.set_test_cookie()

    return render(request, 'projects/index.pug', {
        'register_form': register_form,
        'login_form': login_form
    })


@login_required
def dashboard(request):
    """
    The point of entry for a logged in user.
    Shows the available active projects for the user, and allows him
    to create one.
    Shows the pending invites to other projects.
    Shows very critical information about available projects.
    """
    inactive = request.GET.get('inactive', False)
    projects = request.user.projectuser_set.order_by('-project__start_date')
    if inactive:
        subs = projects.all()
    else:
        subs = projects.filter(project__is_active=True)

    invites = request.user.projectuser_set.filter(status=ProjectUser.STATUS_INVITED)
    createform = CreateProjectForm()

    return render(request, 'projects/dashboard.html', {
        'subs': subs.filter(status=ProjectUser.STATUS_ACCEPTED),
        'invites': invites,
        'inactive': inactive,
        'createform': createform,
    })


@login_required
def project(request, project_name=None):
    """
    Point of entry for a specific project.
    Shows the important information for a project.
    Shows form to invite an user.
    Form to create a new top task.
    Actions available here:
    Invite: Owner
    New Top Task: Owner Participant
    Mark Done: Owner Participant
    """
    project = get_allowed_project(project_name, request.user)
    createform = CreateProjectForm(request.user, request.POST)
    if request.method == 'PUT':
        valid = createform.is_valid()
        if valid:
            createform.save()
        return redirect('projects:dashboard')
    elif request.method == 'POST':
        return {
            "project": project,
            "method": 'POST',
            "answer": 'Update project',
        }
    elif request.method == 'DELETE':
        return {
            "project": project,
            "method": 'DELETE',
            "answer": 'Delete project',
        }
    elif request.method == 'GET':
        inviteform = InviteUserForm(project)
        # taskform = bforms.CreateTaskForm(project, request.user)

        # Tasks
        new_tasks = project.get_new()
        overdue_tasks = project.get_overdue()

        context = {
            'project': project,

            'inviteform': inviteform,
            # 'taskform': taskform,

            'new_tasks': new_tasks,
            'overdue_tasks': overdue_tasks,
        }
        return render(request, 'projects/project.html', context)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def invitation(request, project_name, username):
    """
    Point of entry for a specific project.
    Shows the important information for a project.
    Shows form to invite an user.
    Form to create a new top task.
    Actions available here:
    Invite: Owner
    New Top Task: Owner Participant
    Mark Done: Owner Participant
    """
    project = get_object_or_404(Project, slug=project_name)
    user = User.objects.get(username=username)

    # user = project.user(request.user)
    # user_id = request.data.get('user_id')
    invited_user = ProjectUser.objects.filter(
        # user=request.user,
        user=user,
        project=project,
        # status=ProjectUser.STATUS_INVITED
    ).first()
    if request.method == 'PUT':
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
            user_id=user.id,
            status=ProjectUser.STATUS_INVITED,
        )
        serializer = ProjectUserSerializer(invited_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if invited_user is None:
            raise Exception("User is not invited")
        invited_user.accept()
        invited_user.save()
    elif request.method == 'DELETE':
        if invited_user is None:
            raise Exception("User is not invited")
        invited_user.decline()
        invited_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = ProjectUserSerializer(invited_user, context={'request': request})
        return Response(serializer.data)

    return Response({
        'user': invited_user.as_dict(),
        'invited': [invite.as_dict() for invite in project.invited_users],
        'active': [invite.as_dict() for invite in project.active_users],
    })


@require_POST
@login_required
def activestatus(request):
    projid = request.POST['projectid']
    project = Project.objects.get(id = projid)
    if request.POST['activestatus'] == 'true':
        project.is_active = False
    elif request.POST['activestatus'] == 'false':
        project.is_active = True
    project.save()
    return redirect('projects:dashboard')


@require_POST
@login_required
def markdone(request):
    print(request.POST)
    # handle_task_status(request)
    return redirect('projects:dashboard')


@require_POST
@login_required
def task(request):
    # if not (access in ('Owner', 'Participant')):
    #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
    # taskform = bforms.CreateTaskForm(project, user, request.POST)
    #     if taskform.is_valid():
    #         taskform.save()
    return redirect('projects:project', project_name="123")


@require_POST
@login_required
def project_markdone(request):
    # if not (access in ('Owner', 'Participant')):
    #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
    # if request.POST.has_key('xhr'):
    #     return handle_task_status(request, True)
    # return handle_task_status(request)
    return redirect('projects:project', project_name="123")


@require_POST
@login_required
def deletetask(request):
    # return delete_task(request)
    return redirect('projects:project', project_name="123")


@login_required
def full_logs(request, project_name):
    """
    Shows the logs for a project.
    Actions available here:
    None
    """
    project = get_allowed_project(project_name, request.user)
    if request.method == 'PUT':
        return {
            "project": project,
            "method": 'PUT',
            "answer": 'New project',
        }
    elif request.method == 'POST':
        return {
            "project": project,
            "method": 'POST',
            "answer": 'Update project',
        }
    elif request.method == 'DELETE':
        return {
            "project": project,
            "method": 'DELETE',
            "answer": 'Delete project',
        }
    elif request.method == 'GET':
        log_list = project.log_set.all()
        items, page = add_pager(log_list, request)
        context = {
            'project': project,
            'logs': items,
            'page': page,
        }
    return render(request, 'projects/logs.html', context)


@login_required
def project_settings(request, project_name):
    """Allows settings site sepcific settings."""
    project = get_allowed_project(project_name, request.user)
    # if not (access == 'Owner'):
    #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
    # username = request.POST['user']
    # sub = SubscribedUser.objects.get(project__shortname = project_name, user__username = username)
    if request.method == 'PUT':
        return {
            "project": project,
            "method": 'PUT',
            "answer": 'New project',
        }
    elif request.method == 'POST':
        # sub.group = request.POST['group']
        # sub.save()
        return redirect('projects:project', project_name="123")
    elif request.method == 'DELETE':
        # sub.delete()
        return redirect('projects:project', project_name="123")
    elif request.method == 'GET':
        return render(request, 'projects/settings.html', {
            'project': project,
        })


@login_required
def noticeboard(request, project_name):
    """A noticeboard for the project.
    Shows the notices posted by the users.
    Shows the add notice form.
    Actions available here:
    Add a notice: Owner Participant Viewer (All)
    """
    project = get_allowed_project(project_name, request.user)
    addnoticeform = AddNoticeForm()
    if request.method == 'PUT':
        # addnoticeform = bforms.AddNoticeForm(project, request.user, request.POST)
        # if addnoticeform.is_valid():
        #     addnoticeform.save()
        return redirect('projects:project', project_name="123")
    elif request.method == 'POST':
        return {
            "project": project,
            "method": 'POST',
            "answer": 'Update project',
        }
    elif request.method == 'DELETE':
        return {
            "project": project,
            "method": 'DELETE',
            "answer": 'Delete project',
        }
    elif request.method == 'GET':
        notice_list = project.notice_set.all()
        items, page = add_pager(notice_list, request)
        return render(request, 'projects/noticeboard.html', {
            'project': project,
            'addnoticeform': addnoticeform,
            'notices': items,
            'page': page,
        })


@login_required
def todo(request, project_name):
    """
    Allows to create a new todolist and todoitems.
    Actions available here:
    Add a todolist: Owner Participant
    Add a todoitem: Owner Participant
    """
    project = get_allowed_project(project_name, request.user)
    if request.method == 'PUT':
        # addlistform = bforms.AddTodoListForm(project, request.user, request.POST)
        # if addlistform.is_valid():
        #     addlistform.save()
        return redirect('projects:project', project_name="123")
    elif request.method == 'POST':
        return {
            "project": project,
            "method": 'POST',
            "answer": 'Update project',
        }
    elif request.method == 'DELETE':
        return {
            "project": project,
            "method": 'DELETE',
            "answer": 'Delete project',
        }
    elif request.method == 'GET':
        addlistform = AddTodoListForm()
        # lists = TodoList.objects.all()
        lists = project.todolist_set.all()
        # if request.GET.get('includecomplete', 0):
        #     lists = TodoList.objects.filter(user = request.user, project = project)
        # else:
        #     lists = TodoList.objects.filter(user = request.user, project = project, is_complete_attr = False)
        return render(request, 'projects/todo.html', {
            'project': project,
            'lists': lists,
            'addlistform': addlistform,
        })


@require_POST
def add_todo_item(request):
    # id = int(request.POST['id'])
    # list = TodoList.objects.get(id = id)
    # text_id = '%s-text'%list.id
    # if request.POST[text_id]:
    #     item = TodoItem(list = list, text = request.POST[text_id])
    #     item.save()
    return redirect('projects:project', project_name="123")


@require_POST
def todo_listmarkdone(request):
    # id = int(request.POST['id'])
    # list = TodoList.objects.get(id = id)
    # list.is_complete = True
    # list.save()
    return redirect('projects:project', project_name="123")


@require_POST
def todo_itemmarkdone(request):
    # id = int(request.POST['id'])
    # todoitem = TodoItem.objects.get(id = id)
    # todoitem.is_complete = True
    # todoitem.save()
    return redirect('projects:project', project_name="123")


@login_required
def clone_from_git(request, project_name):
    """
    Clone from git
    """
    project = get_allowed_project(project_name, request.user)

    import logging
    logger = logging.getLogger('git')
    output, error = project.clone_from_git(cwd=settings.PROJECTS_DIR)
    if error:
        logger.error(error.decode('utf-8'))
    logger.info(output.decode('utf-8'))
    return redirect('projects:project', project_name=project.slug)


@login_required
def setup_py(request, project_name):
    """
    Generate setup.py
    """
    project = get_allowed_project(project_name, request.user)
    return render(
        request,
        'projectfiles/setup.py',
        {
            'project': project,
        },
        content_type="application/x-python"
    )


# CSV
@login_required
def dashboard_csv(request):
    # response, writer = reponse_for_cvs()
    # writer.writerow(('Project',))
    # for sub in subs:
    #     writer.writerow((sub.project.name, ))
    # writer.writerow(())
    # writer.writerow(('Project', 'Task Name', 'Due On'))
    # for sub in subs:
    #     for task in sub.project.overdue_tasks():
    #         writer.writerow((task.project.name, task.name, task.expected_end_date))
    # return response
    pass


@require_POST
@login_required
def project_csv(request):
    #    response, writer = reponse_for_cvs()
    #    writer.writerow(Project.as_csv_header())
    #    writer.writerow(project.as_csv())
    #    writer.writerow(())
    #    writer.writerow(Task.as_csv_header())
    #    for task in new_tasks:
    #        writer.writerow(task.as_csv())
    #    writer.writerow(())
    #    writer.writerow(Task.as_csv_header())
    #    for task in overdue_tasks:
    #        writer.writerow(task.as_csv())
    #    return response
    return redirect('projects:dashboard')


@require_POST
def full_logs_csv(request):
    # response, writer = reponse_for_cvs(project=project)
    # writer.writerow((Log.as_csv_header()))
    # for log in query_set:
    #     writer.writerow((log.as_csv()))
    # return response
    return redirect('projects:project', project_name="123")


@require_POST
def noticeboard_csv(request):
    # response, writer = reponse_for_cvs(project=project)
    # writer.writerow((Notice.as_csv_header()))
    # for notice in query_set:
    #     writer.writerow((notice.as_csv()))
    # return response
    return redirect('projects:project', project_name="123")


@require_POST
def todo_csv(request):
    # response, writer = reponse_for_cvs(project=project)
    # writer.writerow(('Todo Lists',))
    # writer.writerow((TodoList.as_csv_header()))
    # lists = TodoList.objects.filter(user = request.user, project = project)
    # for list in lists:
    #     writer.writerow(list.as_csv())
    # for list in lists:
    #     for item in list.todoitem_set.all():
    #         writer.writerow(item.as_csv())
    # return response
    return redirect('projects:project', project_name="123")


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
    serializer_class = ProjectUserSerializer


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
    def get(self, request, project_name, format=None):
        project = get_object_or_404(Project, slug=project_name)
        project_users = ProjectUser.objects.filter(project=project).all()
        serializer = ProjectUserSerializer(
            project_users,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, project_name, format=None):
        project = get_object_or_404(Project, slug=project_name)
        serializer = ProjectUserSerializer(data=request.data)
        serializer.project = project
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
