from __future__ import unicode_literals

from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from mainModels.models import Image, Sector
from .serializer import ImageSerializer, ImageCollectionSerializer
import json

# Create your views here.

# class CreateView(viewsets.ModelViewSet):
#     model = Image
#     parser_classes = (JSONParser)
#     serializer_class = ImageSerializer
#
#     def perform_create(self, serializer):
#         print(self.request.data)
#         print(self.request._files)
#         serializer.save()


class CreateView(generics.ListCreateAPIView):

    queryset = Image.objects.all()

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request._files)
        serializer.save()

class MultiImage(generics.ListCreateAPIView):
    queryset = Image.objects.all()

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = ImageCollectionSerializer

    def perform_create(self, serializer):
        # data_string = str(self.request.data['images']).replace("\'", "\"")
        images = self.request.POST.getlist("images")
        files = self.request._files
        for str_image in images:
            image = json.loads(str_image.replace("\'", "\""))
            photo_name = image["photo"]
            try:
                photo = files.get(photo_name)
            except Exception as e:
                raise ValidationError(str(e))

            sector = image['cameraId']
            time_taken = image['time_taken']

            data = {
                'sector': sector,
                'time_taken': time_taken,
                'photo': photo
            }
            serial = ImageSerializer(data=data)
            if serial.is_valid():
                print(serial.save())
            else:
                raise ValidationError("One or more images failed validation")


        # serializer.save()

# class CreateMultipleView():
#
#     queryset = Image.objects.all()
#
#     parser_classes = (FormParser, MultiPartParser,)
#     serializer_class = ImageSerializer
#
#     for image in request['images']:
#         # find the sector by cameraId and add image to the sector
#         sector = Sector.objects.filter(camera=image['camera']).first()
#         # create a new image based on that camera id
#         Image.create(time_taken=image['time_taken'], photo=image['photo'], sector=sector)
