from __future__ import unicode_literals

from rest_framework.exceptions import ValidationError
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from mainModels.models import Image, Sector
from .serializer import ImageSerializer, ImageCollectionSerializer, ImageResourceSerializer
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI, ImageProcessorServerExternalImageAI
from imageProcessor.models import ImageProcessor
from parkingServer.settings import IMAGE_PROCESSING_SERVER_IP
import pdb
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
    serializer_class = ImageResourceSerializer

    def perform_create(self, serializer):
        instance = serializer.create(self.request.data)
        if not IMAGE_PROCESSING_SERVER_IP:
            server = ImageProcessorServerImageAI()
        else:
            server = ImageProcessorServerExternalImageAI()
        processor = ImageProcessor(server)
        processor.update_sector_from_image(instance)


