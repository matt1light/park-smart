from rest_framework import serializers
from .models import Image
from mainModels.models import Camera

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('photo', 'time_taken', 'sector')

class ImageResourceSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    time_taken = serializers.DateField()
    cameraID = serializers.CharField(max_length=30)

    def create(self, validated_data):
        camera = Camera.objects.filter(cameraID = validated_data['cameraID'])[0]
        sector = camera.sector
        return Image(sector=sector, photo=validated_data['photo'], time_take=validated_data['time_taken'])

class ImageCollectionSerializer(serializers.Serializer):
    images = serializers.CharField()

    # photo1 = serializers.ImageField(required=True)
    # photo2 = serializers.ImageField(required=False)

    def create(self, validated_data):
        count = 0
        for image in validated_data.data:
            count +=1
            self.validate

