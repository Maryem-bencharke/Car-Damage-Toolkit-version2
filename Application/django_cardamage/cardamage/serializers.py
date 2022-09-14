from rest_framework import serializers

from .models import Car


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = (
                'id',
                'image',
                'iscar',
                'isdamaged',
                'location',
                'severity',
                'get_image',
                'get_absolute_url'
        )