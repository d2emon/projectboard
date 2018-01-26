from django.contrib import admin
from .models import ProgrammingLanguage


@admin.register(ProgrammingLanguage)
class ProgrammingLanguagedmin(admin.ModelAdmin):
    pass
