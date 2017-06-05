from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import CreateProjectForm, InviteUserForm
from .models import Project

from users.forms import UserCreationForm, LoginForm

import users.views


def index(request):
    """
    If the user is not logged in, show him the login/register forms, with some
    blurb about the services. Else redirect to /dashboard/
    """
    if request.user.is_authenticated():
        return redirect('projects:dashboard')
    if request.method == 'POST':
        return users.views.login(request)
    register_form = UserCreationForm(prefix='register')
    login_form = LoginForm()
    request.session.set_test_cookie()

    context = {
        'register_form': register_form,
        'login_form': login_form
    }
    return render(request, 'project/index.html', context)


@login_required
def dashboard(request):
    """
    The point of entry for a logged in user.
    Shows the available active projects for the user, and allows him
    to create one.
    Shows the pending invites to other projects.
    Shows very critical information about available projects.
    """
    subs = request.user.projectuser_set.all()
    # if request.GET.get('includeinactive', 0):
    #     subs = user.subscribeduser_set.all()
    # else:
    #     subs = user.subscribeduser_set.filter(project__is_active = True)
    invites = request.user.projectuser_set.all()
    # invites = user.inviteduser_set.filter(rejected = False)
    createform = CreateProjectForm()

    context = {
        'subs': subs,
        'createform': createform,
        'invites': invites,
    }
    return render(request, 'project/dashboard.html', context)


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
def createproject(request):
    createform = CreateProjectForm(request.user, request.POST)
    if createform.is_valid():
        createform.save()
    return redirect('projects:dashboard')


@login_required
def project(request, project_name):
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
    project = get_object_or_404(Project, slug=project_name)  # Only subscribed
    # access = get_access(project, request.user)
    inviteform = InviteUserForm(project)
    # taskform = bforms.CreateTaskForm(project, user)
    new_tasks = project.get_new()
    overdue_tasks = project.get_overdue()

    # inviteform = bforms.InviteUserForm()
    # taskform = bforms.CreateTaskForm(project, request.user)

    context = {
        'project': project,
        'inviteform': inviteform,
        # 'taskform': taskform,
        'new_tasks': new_tasks,
        'overdue_tasks': overdue_tasks,
        # 'access': access,
    }
    # return render(request, 'project/projdetails.html', payload)
    return render(request, 'project/project.html', context)


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
@login_required
def acceptinv(request):
    project = Project.objects.get(id = request.POST['projid'])
    # invite = InvitedUser.objects.get(id = request.POST['invid'])
    # subscribe = SubscribedUser(project = project, user = user, group = invite.group)
    # subscribe.save()
    # invite.delete()
    return redirect('projects:dashboard')


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
def invite(request):
    # if not (access == 'Owner'):
    #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
    # inviteform = bforms.InviteUserForm(project, request.POST)
    # if inviteform.is_valid():
    #     inviteform.save()
    return redirect('projects:project', kwargs={'project_name': "123"})


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
    """Shows the logs for a project.
    Actions available here:
    None"""
    project = get_object_or_404(Project, slug=project_name)  # Only subscribed
    # access = get_access(project, request.user)
    # query_set = Log.objects.filter(project = project)
    # logs, page_data = get_paged_objects(query_set, request, logs_per_page)
    logs = []
    page = []
    context = {
        'project': project,
        'logs': logs,
        'page': page,
    }
    return render(request, 'project/logs.html', context)


@require_POST
def full_logs_csv(request):
    # response, writer = reponse_for_cvs(project=project)
    # writer.writerow((Log.as_csv_header()))
    # for log in query_set:
    #     writer.writerow((log.as_csv()))
    # return response
    return redirect('projects:project', project_name="123")


@login_required
def settings(request, project_name):
    """Allows settings site sepcific settings."""
    project = get_object_or_404(Project, slug=project_name)  # Only subscribed
    # access = get_access(project, request.user)
    # if not (access == 'Owner'):
    #     return HttpResponseForbidden('%s(%s) does not have enough rights' % (request.user.username, access))
    context = {
        'project': project,
    }
    return render(request, 'project/settings.html', context)


@require_POST
def remove_settings(request):
    # username = request.POST['user']
    # sub = SubscribedUser.objects.get(project__shortname = project_name, user__username = username)
    # sub.delete()
    return redirect('projects:project', project_name="123")


@require_POST
def chgroup_settings(request):
    # username = request.POST['user']
    # sub = SubscribedUser.objects.get(project__shortname = project_name, user__username = username)
    # sub.group = request.POST['group']
    # sub.save()
    return redirect('projects:project', project_name="123")


@login_required
def noticeboard(request, project_name):
    """A noticeboard for the project.
    Shows the notices posted by the users.
    Shows the add notice form.
    Actions available here:
    Add a notice: Owner Participant Viewer (All)
    """
    project = get_object_or_404(Project, slug=project_name)  # Only subscribed
    # access = get_access(project, request.user)
    # query_set = Notice.objects.filter(project = project)
    notices = []
    page = []
    # notices, page_data = get_paged_objects(query_set, request, notices_per_page)
    addnoticeform = []
    # addnoticeform = bforms.AddNoticeForm()
    context = {
        'project': project,
        'notices':notices,
        'addnoticeform':addnoticeform,
        'page_data':page,
    }
    return render(request, 'project/noticeboard.html', context)


@require_POST
def add_notice(request):
    # addnoticeform = bforms.AddNoticeForm(project, request.user, request.POST)
    # if addnoticeform.is_valid():
    #     addnoticeform.save()
    return redirect('projects:project', project_name="123")


def noticeboard_csv(request):
    # response, writer = reponse_for_cvs(project=project)
    # writer.writerow((Notice.as_csv_header()))
    # for notice in query_set:
    #     writer.writerow((notice.as_csv()))
    # return response
    return redirect('projects:project', project_name="123")


@login_required
def todo(request, project_name):
    """Allows to create a new todolist and todoitems.
    Actions available here:
    Add a todolist: Owner Participant
    Add a todoitem: Owner Participant
    """
    project = get_object_or_404(Project, slug=project_name)  # Only subscribed
    # access = get_access(project, request.user)
    lists = []
    # if request.GET.get('includecomplete', 0):
    #     lists = TodoList.objects.filter(user = request.user, project = project)
    # else:
    #     lists = TodoList.objects.filter(user = request.user, project = project, is_complete_attr = False)
    addlistform = []
    # addlistform = bforms.AddTodoListForm()
    context = {
        'project': project,
        'lists': lists,
        'addlistform': addlistform,
    }
    return render(request, 'project/todo.html', context)


@require_POST
def add_todo_list(request):
    # addlistform = bforms.AddTodoListForm(project, request.user, request.POST)
    # if addlistform.is_valid():
    #     addlistform.save()
    return redirect('projects:project', project_name="123")


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