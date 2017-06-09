import random


from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to="avatars/")

    def notifications(self):
        notifications = {
            'updates': 0,
            'messages': 0,
            'tasks': 0,
            'comments': 0,
            'payments': 0,
            'projects': 0,
        }
        for k in notifications:
            n = random.randint(-50, 100)
            if n < 0:
                notifications[k] = 0
                continue
            for d in range(100, 0, -10):
                if n > d:
                    n = str(d) + "+"
                    break
            notifications[k] = n
        return notifications

    def rand_avatar(self):
        return settings.MEDIA_URL + str(random.randint(1, 8)) + ".jpg"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return settings.MEDIA_URL
