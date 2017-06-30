from django.core.management.base import BaseCommand
from users.models import UserProfile
from projects.models import Project, ProjectUser
# from faker import Factory


import random


class Command(BaseCommand):
    help = 'Make fake invitation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help="Count of projects to invite."
        )

    def handle(self, *args, **options):
        count = options.get('count', 1)
        invitations = options.get('invitations', 5)
        # fake = Factory.create('ru_RU')
        projects = Project.objects.order_by('?')[:count]
        for i, project in enumerate(projects):
            self.stdout.write(
                "Selecting project %d of %d - %s" % (i + 1, count, project),
                self.style.SUCCESS
            )
            users = UserProfile.objects.exclude(user__in=project.users).order_by('?').all()[:invitations]
            for j, user in enumerate(users):
                self.stdout.write(
                    "Inviting user %d of %d to project %d of %d - %s" % (
                        j + 1,
                        invitations,
                        i + 1,
                        count,
                        user.user
                    ),
                    self.style.SUCCESS
                )

                invite = ProjectUser()
                invite.project = project
                invite.user = user.user
                invite.status = random.choice(ProjectUser.STATUSES)[0]
                invite.save()

                self.stdout.write(
                    "User %s invited" % (user.user, ),
                    self.style.SUCCESS
                )
            self.stdout.write(
                "Added invitations to project %s" % (project, ),
                self.style.SUCCESS
            )

        self.stdout.write(self.style.SUCCESS('Success'))
