from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Project, ProjectUser, Log, Notice, TodoList

from users.serializers import UserSerializer


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='project-detail',
        lookup_field='slug',
        read_only=True
    )
    owner = UserSerializer()

    # owner = serializers.ReadOnlyField(source='owner.username')
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
            # 'overdue',
        )


class UserStatusSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectUser
        fields = (
            'url',
            'user',
            'status',
        )


class InviteUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='invites-detail',
    )
    # accept = serializers.HyperlinkedIdentityField(
    #     view_name='invites-accept',
    # )
    # decline = serializers.HyperlinkedIdentityField(
    #     view_name='invites-decline',
    # )
    project = ProjectSerializer()
    # project = serializers.SlugRelatedField(
    #     queryset=Project.objects.all(),
    #     slug_field='slug',
    # )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = ProjectUser
        fields = (
            'url',
            # 'accept',
            # 'decline',
            'project',
            'user',
            'status',
        )
        depth = 1
        lookup_field = 'username'


class ProjectUserSerializer(serializers.HyperlinkedModelSerializer):
    users = UserStatusSerializer(many=True)
    # project = ProjectSerializer()

    class Meta:
        # model = ProjectUser
        # fields = (
        #     'url',
        #     'project',
        #     'user',
        #     'status',
        # )
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
            'users',
            # 'programming_language'
        )
        # depth = 1


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
