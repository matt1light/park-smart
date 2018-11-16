from __future__ import unicode_literals

from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from mainModels.models import Image, Sector
from .serializers import ImageSerializer

# Create your views here.

class CreateView(viewsets.ModelViewSet):
    model = Image
    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request._files)
        serializer.save()


# class CreateView(generics.ListCreateAPIView):
#
#     queryset = Image.objects.all()
#
#     parser_classes = (FormParser, MultiPartParser,)
#     serializer_class = ImageSerializer
#
#     def perform_create(self, serializer):
#         print(self.request.data)
#         print(self.request._files)
#         serializer.save()


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
