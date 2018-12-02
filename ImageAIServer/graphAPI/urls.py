from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ImageProcessorView

urlpatterns = [
    url(r'^car_coordinates/$', ImageProcessorView.as_view(), name="process_photo"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
