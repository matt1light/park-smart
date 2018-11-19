from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('photo', 'time_taken', 'sector')

class ImageResourceSerializer(serializers.Serializer):
    cameraId = serializers.IntegerField(required = True)
    photo = serializers.CharField(required = True)
    time_taken = serializers.DateTimeField(required = True)

class ImageCollectionSerializer(serializers.Serializer):
    images = serializers.CharField()

    # photo1 = serializers.ImageField(required=True)
    # photo2 = serializers.ImageField(required=False)

    def create(self, validated_data):
        count = 0
        print("in create")
        for image in validated_data.data:
            count +=1
            self.validate

