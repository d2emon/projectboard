from rest_framework import serializers

from .models import Project, ProjectUser, Log, Notice, TodoList


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            'url',
            'name',
            'slug',
            'description',
            'owner',
            'start_date',
            'end_date',
            'is_active',
            'created_on',
            'git',
            'uri',
            # 'programming_language'
        )


class ProjectUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectUser
        fields = (
            'url',
            'project',
            'user',
            'status',
        )


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = (
            'url',
            'project',
            'title',
            'description',
            'created_on',
        )


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = (
            'url',
            'user',
            'project',
            'text',
            'created_on',
        )


class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoList
        fields = (
            'url',
            'name',
            'user',
            'project',
            'created_on',
        )
