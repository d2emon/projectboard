from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, LoginForm, CreateProjectForm
import users.views


def index(request):
    """
    If the user is not logged in, show him the login/register forms, with some
    blurb about the services. Else redirect to /dashboard/
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('projects:dashboard'))
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
    subs = []
    invites = []
    # if request.GET.get('includeinactive', 0):
    #     subs = user.subscribeduser_set.all()
    # else:
    #     subs = user.subscribeduser_set.filter(project__is_active = True)
    # invites = user.inviteduser_set.filter(rejected = False)
    createform = CreateProjectForm()
    if request.method == 'POST':
        if request.POST.has_key('createproject'):
            createform = CreateProjectForm(user, request.POST)
            if createform.is_valid():
                createform.save()
                return HttpResponseRedirect('.')
        elif request.POST.has_key('acceptinv'):
            # project = Project.objects.get(id = request.POST['projid'])
            # invite = InvitedUser.objects.get(id = request.POST['invid'])
            # subscribe = SubscribedUser(project = project, user = user, group = invite.group)
            # subscribe.save()
            # invite.delete()
            return HttpResponseRedirect('.')
        elif request.POST.has_key('activestatus'):
            projid = request.POST['projectid']
            # project = Project.objects.get(id = projid)
            if request.POST['activestatus'] == 'true':
                # project.is_active = False
                pass
            elif request.POST['activestatus'] == 'false':
                # project.is_active = True
                pass
            # project.save()
            return HttpResponseRedirect('.')
        elif request.POST.has_key('markdone'):
            print(request.POST)
            # handle_task_status(request)
    elif request.method == 'GET':
        createform = CreateProjectForm()

    context = {
        'subs': subs,
        'createform': createform,
        'invites': invites
    }
    if request.GET.get('csv', ''):
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
    return render(request, 'project/dashboard.html', context)
