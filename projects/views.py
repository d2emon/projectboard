from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import CreateProjectForm
from .models import Project

from users.forms import UserCreationForm, LoginForm
from users.models import get_userdata

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
    user = request.user
    subs = Project.objects.all()
    print(subs)
    invites = []
    # if request.GET.get('includeinactive', 0):
    #     subs = user.subscribeduser_set.all()
    # else:
    #     subs = user.subscribeduser_set.filter(project__is_active = True)
    # invites = user.inviteduser_set.filter(rejected = False)
    createform = CreateProjectForm()

    context = {
        'subs': subs,
        'createform': createform,
        'invites': invites,

        'userdata': get_userdata(),
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
