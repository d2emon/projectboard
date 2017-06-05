from django.contrib import admin
from .models import Project, ProjectUser, Log


class ProjectUserInline(admin.StackedInline):
    model = ProjectUser


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectUserInline, ]


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
