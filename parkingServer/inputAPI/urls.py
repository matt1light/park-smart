from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView

urlpatterns = {
    url(r'^image/$', CreateView.as_view({'post': 'create'}), name="create"),
    # url(r'^image-collection/$', CreateMultipleView.as_view(), name="createMultiple"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
