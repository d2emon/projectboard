from django import forms
from django.utils.translation import ugettext as _


from .models import Project

import re
import datetime


class CreateProjectForm(forms.Form):
    """
    Create a new project.
    Writes to model project
    Short name: Only alphanumeric chars allowed. Length = 20
    Name: Name of project. Length = 200
    Start_date: Start date for project. Defaults to today.
    End_date: End date ofr the project.
    """
    name = forms.CharField(
        max_length = 200,
        help_text='Name of the project.'
    )
    slug = forms.SlugField(
        max_length = 20,
        help_text = 'Shortname for your project. Determines URL. ' +
        'Can not contain spaces/sepcial chars.'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': "date"}),
    )
    end_date = forms.DateField(
        label = _("End Date"),
        widget=forms.DateInput(attrs={'type': "date"}),
        required=False,
    )

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
            slug=self.cleaned_data['slug']
        )
        project.owner = self.user
        project.start_date = self.cleaned_data['start_date']
        project.save()
        # subscribe = SubscribedUser(user = self.user, project = project, group = 'Owner')
        # subscribe.save()
        project = True
        return project

    def clean_slug(self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['slug']):
            raise forms.ValidationError("This value must contain only letters, numbers and underscores.")
        self.is_valid_slug()
        return self.cleaned_data['slug']

    def is_valid_slug(self):
        try:
            Project.objects.get(slug=self.cleaned_data['slug'])
        except Project.DoesNotExist:
            return
        raise forms.ValidationError('This project name is already taken. Please try another.')

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
