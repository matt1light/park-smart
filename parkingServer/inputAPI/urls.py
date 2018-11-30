from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, MultiImage

urlpatterns = [
    url(r'^image/$', CreateView.as_view(), name="create"),
    url(r'^image-collection/$', MultiImage.as_view(), name="createMultiple"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
