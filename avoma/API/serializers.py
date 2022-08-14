from rest_framework import serializers
from API.models import Test, EventItem

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields=('Id', 'Name')

class EventItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventItem
        fields=('Id', 'StartTime', 'EndTime', 'Duration','Creator')