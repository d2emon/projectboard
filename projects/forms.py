from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _


from .models import Project


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
        fields = ['name', 'slug', 'start_date', 'end_date']
        help_texts = {
            'name': "Name of the project.",
            'slug': "Shortname for your project. Determines URL. " +
            "Can not contain spaces/sepcial chars.",
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': "date"}),
            'end_date': forms.DateInput(attrs={'type': "date"}),
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
