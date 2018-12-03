"""parkingServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mainModels.models import Sector
from imageProcessor.models import ImageProcessor
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('inputAPI.urls')),
    url(r'^', include('outputAPI.urls')),
    url(r'^', include('webApp.urls'))
]

server = ImageProcessorServerImageAI()
imageProcessor = ImageProcessor(server)
sector = Sector.objects.get(pk=1)
image_name = "camera_pictures/image0_Tga0N1G.jpg"

imageProcessor.calibrate_sector(image_name, sector)
