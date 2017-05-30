from django.db import models
from django.urls import reverse


from django.contrib.auth.models import User


from datetime import datetime


class Project(models.Model):
    """
    Model for project.

    shortname: Shortname, can not contain spaces , special chars. Used in url
    name: Name of the project
    owner: The user who has all the rights for the project.
    start_date: When does this project start?
    end_date: When does this project end?
    is_active: Is this project active?
    """
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null = True)
    is_active = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add = 1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project', kwargs={'project_name': self.slug})

    def get_overdue(self):
        return [
            {
                'id': 1,
                'get_absolute_url': '/',
                'name': "Task Name",
                'expected_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
            {
                'id': 1,
                'get_absolute_url': '/',
                'name': "Task Name",
                'expected_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
            {
                'id': 1,
                'get_absolute_url': '/',
                'name': "Task Name",
                'expected_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
        ]
