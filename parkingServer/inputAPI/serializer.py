from rest_framework import serializers
from mainModels.models import Sector, Image
from rest_framework.exceptions import ValidationError

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('photo', 'time_taken', 'sector')

class ImageResourceSerializer(serializers.Serializer):

    photo = serializers.ImageField()
    time_taken = serializers.DateTimeField()
    cameraID = serializers.CharField(max_length=30)

    def create(self, validated_data):
        sector = Sector.objects.filter(cameraID = validated_data['cameraID']).first()
        if sector == None:
            raise ValidationError()
        else:
            image = Image.objects.create(sector=sector, photo=validated_data['photo'], time_taken=validated_data['time_taken'])
            return image

class ImageCollectionSerializer(serializers.Serializer):
    images = serializers.CharField()

    # photo1 = serializers.ImageField(required=True)
    # photo2 = serializers.ImageField(required=False)

    def create(self, validated_data):
        count = 0
        for image in validated_data.data:
            count +=1
            self.validate

