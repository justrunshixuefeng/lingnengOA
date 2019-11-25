from rest_framework import serializers
from .models import Announcement


class Announcementser(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

    def create(self, data):
        user = Announcement.objects.create(**data)
        return user
