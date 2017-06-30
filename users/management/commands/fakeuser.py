from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Factory


import random


class Command(BaseCommand):
    help = 'Adds fake user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help="Count of fake users to create."
        )

    def handle(self, *args, **options):
        count = options.get('count', 1)
        fake = Factory.create('ru_RU')
        for i in range(count):
            self.stdout.write(
                "Adding user %d of %d" % (i + 1, count),
                self.style.SUCCESS
            )
            user = User()
            user.username = fake.user_name()
            user.set_password(fake.password())

            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.email = fake.email()
            user.save()

            user.userprofile.avatar = "avatars/%d.jpg" % (random.randint(1, 6))
            user.userprofile.save()

            print(user)
            self.stdout.write(
                "User added",
                self.style.SUCCESS
            )

        # populator.addEntity(settings.AUTH_USER_MODEL, count)

        print("Add user")
        print(args)
        print(options)
        self.stdout.write(self.style.SUCCESS('Success'))
