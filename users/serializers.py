from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import UserProfile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.SerializerMethodField()
    # avatar = serializers.ReadOnlyField(source='userprofile.avatar')

    def get_profile(self, obj):
        serializer = ProfileSerializer(obj.userprofile, context=self.context)
        return serializer.data

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'profile')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
