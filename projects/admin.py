from django.contrib import admin
from .models import Project, ProjectUser


class ProjectUserInline(admin.StackedInline):
    model = ProjectUser


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectUserInline, ]
