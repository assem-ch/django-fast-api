from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from django.urls import path

from test_api.views import router

urlpatterns = [
    *router.urls,
    path('api-schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
