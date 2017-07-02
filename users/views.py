from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User, Group


from rest_framework import viewsets


from .forms import LoginForm
from .serializers import UserSerializer, GroupSerializer


def login(request):
    """
    Login a user.
    Actions avialable:
    Login: Anyone

    Display and processs the login form.
    """

    no_cookies = False
    account_disabled = False
    invalid_login = False
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')

    if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            form = LoginForm(request.POST)
            if form.is_valid():
                user = auth.authenticate(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                )
                if user:
                    if user.is_active:
                        request.session[settings.PERSISTENT_SESSION_KEY] = form.cleaned_data['remember_user']
                        auth.login(request, user)
                        # login successful, redirect
                        return HttpResponseRedirect(redirect_to)
                    else:
                        account_disabled = True
                else:
                    invalid_login = True
        else:
            no_cookies = True
            form = None
    else:
        form = LoginForm()

    # cookie must be successfully set/retrieved for the form to be processed
    request.session.set_test_cookie()
    context = {
        'no_cookies': no_cookies,
        'account_disabled': account_disabled,
        'invalid_login': invalid_login,
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to
    }
    return render(
        request,
        'registration/login.html',
        context,
    )


def notify(request, filter=""):
    return HttpResponseRedirect("/")


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
