from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _


from .models import Project, ProjectUser, Notice


import datetime


class CreateProjectForm(ModelForm):
    """
    Create a new project.
    Writes to model project
    Short name: Only alphanumeric chars allowed. Length = 20
    Name: Name of project. Length = 200
    Start_date: Start date for project. Defaults to today.
    End_date: End date ofr the project.
    """

    class Meta:
        model = Project
        fields = [
            'name',
            'slug',
            'programming_language',
            'start_date',
            'end_date',
        ]
        help_texts = {
            'name': _("Name of the project."),
            'slug': _("Shortname for your project. Determines URL. " +
            "Can not contain spaces/sepcial chars."),
        }
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': "date"},
                format="%Y-%m-%d"
            ),
            'end_date': forms.DateInput(
                attrs={'type': "date"},
                format="%Y-%m-%d"
            ),
        }
        labels = {
            'end_date': _("End Date"),
        }
        error_messages = {
            'slug': {
                'unique': _("This project name is already taken. " +
                            "Please try another."),
                'slug': _("This value must contain only letters, numbers " +
                          "and underscores."),
            },
        }

    def __init__(self, user = None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['start_date'].initial = datetime.date.today()
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self):
        project = Project(
            name=self.cleaned_data['name'],
            slug=self.cleaned_data['slug'],
            owner=self.user,
            start_date=self.cleaned_data['start_date']
        )
        project.save()

        subscribe = ProjectUser(user=self.user, project=project)
        subscribe.save()
        # subscribe = SubscribedUser(user = self.user, project = project, group = 'Owner')
        # subscribe.save()

        return project

    def as_div(self):
        return self._html_output(
            normal_row="<div class=\"form-group row\">" +
            "<div class=\"col-md-3 form-control-label\">%(label)s</div>" +
            "<div class=\"col-md-9\">%(field)s%(errors)s%(help_text)s</div>" +
            "</div>",
            error_row="<span class=\"error\">%s</span>",
            row_ender="</div>",
            help_text_html="<span class=\"help_block\">%s</span>",
            errors_on_separate_row=True,
        )


class InviteUserForm(ModelForm):
    """
    Invite a user to the project.
    Username: username of the user to invite.
    Group: The group in which to put the invited user.
    """

    class Meta:
        model = ProjectUser
        fields = ['user', ]
        help_texts = {
            'user': _("User name of the user to invite."),
            # 'group': "Permissions available to this user.",
        }

    def __init__(self, project = None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(InviteUserForm, self).__init__(*args, **kwargs)
        self.project = project
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self):
        invitation = ProjectUser(
            user=self.cleaned_data['user'],
            project=self.project,
        )
        invitation.save()
        return invitation

    def as_div(self):
        return self._html_output(
            normal_row="<div class=\"form-group row\">" +
            "<div class=\"col-md-3 form-control-label\">%(label)s</div>" +
            "<div class=\"col-md-9\">%(field)s%(errors)s%(help_text)s</div>" +
            "</div>",
            error_row="<span class=\"error\">%s</span>",
            row_ender="</div>",
            help_text_html="<span class=\"help_block\">%s</span>",
            errors_on_separate_row=True,
        )


class AddNoticeForm(ModelForm):
    """
    Add a notice to a task.
    """

    class Meta:
        model = Notice
        fields = ['text', ]

    def __init__(self, project=None, user=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AddNoticeForm, self).__init__(*args, **kwargs)
        self.project = project
        self.user = user
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self):
        notice = Notice(
            user=self.user,
            project=self.project,
            text=self.cleaned_data['text'],
        )
        notice.save()
        return notice

    def as_div(self):
        return self._html_output(
            normal_row="<div class=\"form-group row\">" +
            "<div class=\"col-md-3 form-control-label\">%(label)s</div>" +
            "<div class=\"col-md-9\">%(field)s%(errors)s%(help_text)s</div>" +
            "</div>",
            error_row="<span class=\"error\">%s</span>",
            row_ender="</div>",
            help_text_html="<span class=\"help_block\">%s</span>",
            errors_on_separate_row=True,
        )
