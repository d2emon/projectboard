from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


from django.contrib.auth.models import User


from techs.models import ProgrammingLanguage


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
    git = models.CharField(max_length=100, blank=True, null=True)
    uri = models.CharField(max_length=100, blank=True, null=True)
    programming_language = models.ForeignKey(ProgrammingLanguage)

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
                'expected_start_date': datetime.today(),
                'actual_start_date': datetime.today(),
                'expected_end_date': datetime.today(),
                'actual_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
            {
                'id': 1,
                'get_absolute_url': '/',
                'name': "Task Name",
                'expected_start_date': datetime.today(),
                'actual_start_date': datetime.today(),
                'expected_end_date': datetime.today(),
                'actual_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
            {
                'id': 1,
                'get_absolute_url': '/',
                'name': "Task Name",
                'expected_start_date': datetime.today(),
                'actual_start_date': datetime.today(),
                'expected_end_date': datetime.today(),
                'actual_end_date': datetime.today(),
                'user_responsible': self.owner,
                'is_complete': True,
            },
        ]

    def get_new(self):
        return self.get_overdue()

    @property
    def users(self):
        return [user.user for user in self.projectuser_set.all()]

    def user_status(self, user):
        user_status = self.projectuser_set.get(user=user)
        return user_status.status

    @property
    def invited_users(self):
        return self.projectuser_set.filter(
            status=ProjectUser.STATUS_INVITED,
        )

    @property
    def active_users(self):
        return self.projectuser_set.filter(
            status__in=ProjectUser.ACTIVE_STATUSES
        )

    def allowed(self, user):
        if user.is_admin:
            return True
        status = self.user_status(user)
        return status in ProjectUser.ALLOWED_STATUSES

    def clone_from_git(self, cwd='sources/'):
        import subprocess
        return subprocess.Popen(
            ['git', 'clone', self.git],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        ).communicate()

    def keywords(self):
        return 'archive database flask privatisation',

    def license(self):
        return 'GPL-3.0',

    class Meta:
        ordering = ['-start_date', ]


class ProjectUser(models.Model):
    """Users who have access to a given project
    Users who have invited to a given project
    user: the user
    project: the project
    group: access rights
    ----
    rejected: has the user rejected the invitation
    """
    STATUS_INVITED = 1
    STATUS_ACCEPTED = 2
    STATUS_DECLINED = 3
    STATUSES = (
        (STATUS_INVITED, "Invited"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
    )
    ACTIVE_STATUSES = (
        STATUS_ACCEPTED,
    )
    ALLOWED_STATUSES = (
        STATUS_INVITED,
        STATUS_ACCEPTED,
    )

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    status = models.IntegerField(
        null=True,
        choices=STATUSES,
    )

    @receiver(post_save, sender=Project)
    def create_log(sender, instance, created, **kwargs):
        if created:
            owner = ProjectUser.objects.create(
                user=instance.owner,
                project=instance,
                status=ProjectUser.STATUS_ACCEPTED,
            )
            owner.save()


class Log(models.Model):
    """Log of the project.
    project: Project for which this log is written.
    text: Text of the log.
    created_on: When was this log created.
    """
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add = 1)

    @receiver(post_save, sender=Project)
    def create_project_log(sender, instance, created, **kwargs):
        if created:
            log_title = "Created"
            log_text = "Project %s created by %s" % (instance, instance.owner)
        else:
            log_title = "Changed"
            log_text = "Project %s changed" % (instance, )
        record = Log.objects.create(
            project=instance,
            title=log_title,
            description=log_text,
        )
        record.save()

    @receiver(post_save, sender=ProjectUser)
    def create_user_log(sender, instance, created, **kwargs):
        if created:
            log_title = "Invited User"
            log_text = "User %s invited" % (instance.user, )
        else:
            log_title = "Permission Changed"
            log_text = "User %s changed permission to %d" % (instance.user, instance.status)
        record = Log.objects.create(
            project=instance.project,
            title=log_title,
            description=log_text,
        )
        record.save()

    class Meta:
        ordering = ('-created_on', )


class Notice(models.Model):
    """
    number: of the notice under the current project.
    user: User who wrote this notice.
    text: text of the notice.
    created_on: When was this notice created. Auto filled.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add = 1)

    class Meta:
        ordering = ('-created_on', )


class TodoList(models.Model):
    """
    A todo list of a user of the project.
    name: name of the todo list.
    user: User for which this todo list is created.
    project: Project under which this list is created.
    is_complete_attr: Is this list complete?
    created_on: When was this list created?
    """
    name = models.CharField(max_length = 200)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    created_on = models.DateTimeField(auto_now_add = 1)

    class Meta:
        ordering = ('-created_on', )
