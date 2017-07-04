from django.core.management.base import BaseCommand
from projects.models import Project, TodoList
from faker import Factory


import random


class Command(BaseCommand):
    help = 'Make fake todo list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help="Count of todo lists to invite."
        )

    def handle(self, *args, **options):
        count = options.get('count', 1)
        maxlists = options.get('maxlists', 10)
        fake = Factory.create('ru_RU')
        projects = Project.objects.order_by('?')[:count]
        for i, project in enumerate(projects):
            self.stdout.write(
                "Selecting project %d of %d - %s" % (i + 1, count, project),
                self.style.SUCCESS
            )
            lists = random.randint(1, maxlists)
            for j in range(lists):
                self.stdout.write(
                    "Making todo list %d of %d to project %d of %d" % (
                        j + 1,
                        lists,
                        i + 1,
                        count,
                    ),
                    self.style.SUCCESS
                )
                user = project.users.order_by('?').first()

                todolist = TodoList()
                todolist.name = fake.company()
                todolist.project = project
                todolist.user = user.user
                todolist.save()

                self.stdout.write(
                    "Added todolist for %s" % (user.user, ),
                    self.style.SUCCESS
                )
            self.stdout.write(
                "Added todo lists to project %s" % (project, ),
                self.style.SUCCESS
            )

        self.stdout.write(self.style.SUCCESS('Success'))
