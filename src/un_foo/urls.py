

from .views import foo_view

try:
    from django.urls import path

    urlpatterns = [
        path('foo/', foo_view, name="api-doc"),
    ]
except:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^foo/', foo_view, name="api-doc"),
    ]
