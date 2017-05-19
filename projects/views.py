from django.shortcuts import render
from .forms import UserCreationForm, LoginForm


def index(request):
    """
    If the user is not logged in, show him the login/register forms, with some
    blurb about the services. Else redirect to /dashboard/
    """
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect('/dashboard/')
    # if request.method == 'POST':
    #     return login(request)
    register_form = UserCreationForm(prefix='register')
    login_form = LoginForm()
    request.session.set_test_cookie()

    context = {
        'register_form': register_form,
        'login_form': login_form
    }
    return render(request, 'project/index.html', context)
