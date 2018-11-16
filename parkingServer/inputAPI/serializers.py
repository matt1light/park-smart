from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
       many = kwargs.pop('many', True)
       super(ImageSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Image
        fields = ('photo', 'time_taken', 'sector')