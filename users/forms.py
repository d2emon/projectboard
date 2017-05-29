from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


from projects.models import Project


import re


class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username
    and password.
    """
    username = forms.CharField(max_length = 30, required = True, help_text = '')
    password = forms.CharField(
        max_length=30,
        widget=forms.widgets.PasswordInput(),
        required=True,
    )
    password_verify = forms.CharField(
        max_length=30,
        widget=forms.widgets.PasswordInput(),
        required=True,
    )
    project_name = forms.CharField(max_length = 20, required = False)

    def clean_username(self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['username']):
            raise forms.ValidationError("This value must contain only letters, " +
                                        "numbers and underscores.")
        self.isValidUsername()
        return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return super(forms.Form, self).clean()

    def isValidUsername(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return
        raise forms.ValidationError(_('A user with that username already exists.'))

    def clean_project_name(self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['project_name']):
            raise forms.ValidationError("This value must contain only letters, " +
                                        "numbers and underscores.")
        self.is_valid_shortname()
        return self.cleaned_data['project_name']

    def is_valid_shortname(self):
        try:
            Project.objects.get(shortname = self.cleaned_data['project_name'])
        except Project.DoesNotExist:
            return
        raise forms.ValidationError('This project name is already taken. Please ' +
                                    'try another.')

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'], '',
                                        self.cleaned_data['password'])
        # profile = UserProfile(user = user)
        # profile.save()
        return user


class LoginForm(forms.Form):
    """Login form for users."""
    username = forms.RegexField(
        r'^[a-zA-Z0-9_]{1,30}$',
        max_length=30,
        min_length=1,
        widget=forms.widgets.TextInput(attrs={'class': 'input'}),
        error_messages={
            'min_length': 'Must be 1-30 alphanumeric characters or underscores.',
            'max_length': 'Must be 1-30 alphanumeric characters or underscores.',
        }
    )
    password = forms.CharField(
        min_length=1,
        max_length=128,
        widget=forms.widgets.PasswordInput(attrs={'class': 'input'}),
        label='Password'
    )
    remember_user = forms.BooleanField(
        required=False,
        label='Remember Me'
    )

    def clean(self):
        try:
            try:
                user = User.objects.get(username__iexact = self.cleaned_data['username'])
            except KeyError:
                raise forms.ValidationError('Please provide a username.')
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid username, please try again.')

        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError('Invalid password, please try again.')

        return self.cleaned_data
