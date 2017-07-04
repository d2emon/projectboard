from django.core.management.base import BaseCommand
from projects.models import Project, Notice
from faker import Factory


import random


class Command(BaseCommand):
    help = 'Make fake notices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help="Count of projects to make notice."
        )

    def handle(self, *args, **options):
        count = options.get('count', 1)
        maxnotices = options.get('maxnotices', 10)
        fake = Factory.create('ru_RU')
        projects = Project.objects.order_by('?')[:count]
        for i, project in enumerate(projects):
            self.stdout.write(
                "Selecting project %d of %d - %s" % (i + 1, count, project),
                self.style.SUCCESS
            )
            notices = random.randint(1, maxnotices)
            for j in range(notices):
                self.stdout.write(
                    "Making notice %d of %d to project %d of %d" % (
                        j + 1,
                        notices,
                        i + 1,
                        count,
                    ),
                    self.style.SUCCESS
                )
                user = project.users.order_by('?').first()

                notice = Notice()
                notice.project = project
                notice.user = user.user
                notice.text = fake.paragraph()
                notice.save()

                self.stdout.write(
                    "User %s noticed" % (user.user, ),
                    self.style.SUCCESS
                )
            self.stdout.write(
                "Added notices to project %s" % (project, ),
                self.style.SUCCESS
            )

        self.stdout.write(self.style.SUCCESS('Success'))
