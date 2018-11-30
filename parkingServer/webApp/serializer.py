from rest_framework import serializers
from mainModels.models import Spot, ImageCoordinates, SectorSpot, Sector, Row, LotState

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ('full', 'active')

class ImageCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCoordinates
        fields = ('left', 'right', 'top', 'bottom')

class SectorSpotSerializer(serializers.ModelSerializer):
    spot = SpotSerializer()
    image_coordinates = ImageCoordinatesSerializer()

    class Meta:
        model = SectorSpot
        fields = ('spot', 'image_coordinates')

class SectorSerializer(serializers.ModelSerializer):
    sector_spots = SectorSpotSerializer(many=True, read_only=True)

    class Meta:
        model = Sector
        fields = ('sector_spots', )

class RowSerializer(serializers.ModelSerializer):
    spots = SpotSerializer(many=True, read_only=True)

    class Meta:
        model = Row
        fields = ('spots', )
