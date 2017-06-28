from django.contrib import admin
from .models import Project, ProjectUser, Log, Notice, TodoList


class ProjectUserInline(admin.StackedInline):
    model = ProjectUser


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectUserInline, ]


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    pass
