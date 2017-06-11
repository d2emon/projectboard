import random


from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to="avatars/")
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
        
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

    @classmethod
    def rand_avatar(self):
        return settings.MEDIA_URL + 'avatars/' + str(random.randint(1, 8)) + ".jpg"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return UserProfile.rand_avatar()
