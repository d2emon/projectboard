from django.core.management.base import BaseCommand
from users.models import UserProfile
from projects.models import Project, ProgrammingLanguage
from faker import Factory


import random


class Command(BaseCommand):
    help = 'Adds fake project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help="Count of fake projects to create."
        )

    def handle(self, *args, **options):
        count = options.get('count', 1)
        fake = Factory.create('ru_RU')

        users = UserProfile.objects.all()
        languages = ProgrammingLanguage.objects.all()

        for i in range(count):
            self.stdout.write(
                "Adding project %d of %d" % (i + 1, count),
                self.style.SUCCESS
            )
            project = Project()
            project.name = fake.company()
            project.slug = fake.slug()
            project.description = fake.paragraph()
            project.owner = random.choice(users).user
            project.start_date = fake.date()
            project.end_date = fake.future_date()
            project.is_active = random.randint(0, 100) > 20
            # git = models.CharField(max_length=100, blank=True, null=True)
            project.uri = fake.url()
            project.programming_language = random.choice(languages)
            project.save()

            self.stdout.write(
                "Project %s added" % (project.name, ),
                self.style.SUCCESS
            )

        self.stdout.write(self.style.SUCCESS('Success'))
