from django.db import models
from django.urls import reverse


class ProgrammingLanguage(models.Model):
    """
    Model for programming languages.

    slug: Shortname, can not contain spaces , special chars. Used in url
    name: Name of the language
    """
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('techs:language', kwargs={'language': self.language})
