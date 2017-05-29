from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from .forms import CreateProjectForm
from .models import Project

from users.forms import UserCreationForm, LoginForm

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
    subs = Project.objects.all()
    print(subs)
    invites = []
    # if request.GET.get('includeinactive', 0):
    #     subs = user.subscribeduser_set.all()
    # else:
    #     subs = user.subscribeduser_set.filter(project__is_active = True)
    # invites = user.inviteduser_set.filter(rejected = False)
    createform = CreateProjectForm()
    if request.method == 'POST':
        if 'createproject' in request.POST:
            createform = CreateProjectForm(user, request.POST)
            if createform.is_valid():
                createform.save()
                return HttpResponseRedirect('.')
        elif 'acceptinv' in request.POST:
            project = Project.objects.get(id = request.POST['projid'])
            # invite = InvitedUser.objects.get(id = request.POST['invid'])
            # subscribe = SubscribedUser(project = project, user = user, group = invite.group)
            # subscribe.save()
            # invite.delete()
            return HttpResponseRedirect('.')
        elif 'activestatus' in request.POST.has_key:
            projid = request.POST['projectid']
            project = Project.objects.get(id = projid)
            if request.POST['activestatus'] == 'true':
                project.is_active = False
            elif request.POST['activestatus'] == 'false':
                project.is_active = True
            project.save()
            return HttpResponseRedirect('.')
        elif request.POST.has_key('markdone'):
            print(request.POST)
            # handle_task_status(request)
    elif request.method == 'GET':
        createform = CreateProjectForm()

    import random
    notifications = {
        'updates': 0,
        'messages': 0,
        'tasks': 0,
        'comments': 0,
        'payments': 0,
        'projects': 0,
    }
    for k in notifications:
        n = random.randint(-50, 100)
        if n < 0:
            notifications[k] = 0
            continue
        for d in range(100, 0, -10):
            if n > d:
                n = str(d) + "+"
                break
        notifications[k] = n
    userdata = {
        'notifications': notifications,
        'avatar': str(random.randint(1, 8)) + ".jpg",
        'username': "d2emon",
        'email': "d2emonium@gmail.com",
    }
    graphs = [
        {
            'style': 'card-primary',
            'total': random.randrange(0, 10000),
            'chart': 'card-chart1',
            'settings': True,
        },
        {
            'style': 'card-info',
            'total': random.randrange(0, 10000),
            'chart': 'card-chart2',
            'location': True,
        },
        {
            'style': 'card-warning',
            'total': random.randrange(0, 10000),
            'chart': 'card-chart3',
            'settings': True,
            'location': True,
        },
        {
            'style': 'card-danger',
            'total': random.randrange(0, 10000),
            'chart': 'card-chart4',
            'settings': True,
        },
    ]
    total = random.randrange(0, 100000)
    counts = [random.randrange(0, total) for i in range(5)]
    bars = [
        {
            'title': "Visits",
            'total': total,
            'count': counts[0],
            'rate': counts[0] * 100 / total,
            'style': "bg-success",
            'show_count': True,
        },
        {
            'title': "Unique",
            'total': total,
            'count': counts[1],
            'style': "bg-info",
            'show_count': True,
        },
        {
            'title': "Pageviews",
            'total': total,
            'count': counts[2],
            'style': "bg-warning",
            'show_count': True,
        },
        {
            'title': "New Users",
            'total': total,
            'count': counts[3],
            'style': "bg-danger",
            'show_count': True,
        },
        {
            'title': "Bounce Rate",
            'total': total,
            'count': counts[4],
            'rate': counts[4] * 100 / total,
            'style': "",
            'show_count': False,
        },
    ]
    social_friends = []
    social_friends_raw = [random.randint(0, 1000) for i in range(4)]
    for id, friends in enumerate(social_friends_raw):
        if random.randint(0, 2) < 1:
            social_friends.append("%dk" % friends)
            continue
        if friends < 100:
            social_friends.append(friends)
            continue
        for d in range(1000, 0, -100):
            if friends > d:
                social_friends.append("%d+" % d)
                break
        pass
    social_feeds = [random.randint(0, 2000) for i in range(4)]
    socials = [
        {
            'style': "facebook",
            'icon': "fa-facebook",
            'friends': social_friends[0],
            'feeds': social_feeds[0],
            'chart': "social-box-chart-1",
            'friends_label': 'Friends',
            'feeds_label': 'Feeds',
        },
        {
            'style': "twitter",
            'icon': "fa-twitter",
            'friends': social_friends[1],
            'feeds': social_feeds[1],
            'chart': "social-box-chart-2",
            'friends_label': 'Followers',
            'feeds_label': 'Tweets',
        },
        {
            'style': "linkedin",
            'icon': "fa-linkedin",
            'friends': social_friends[2],
            'feeds': social_feeds[2],
            'chart': "social-box-chart-3",
            'friends_label': 'Contacts',
            'feeds_label': 'Feeds',
        },
        {
            'style': "google-plus",
            'icon': "fa-google-plus",
            'friends': social_friends[3],
            'feeds': social_feeds[3],
            'chart': "social-box-chart-4",
            'friends_label': 'Followers',
            'feeds_label': 'Circles',
        },
    ]
    context = {
        'subs': subs,
        'createform': createform,
        'invites': invites,

        'userdata': userdata,
        'graphs': graphs,
        'bars': bars,
        'socials': socials,
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
