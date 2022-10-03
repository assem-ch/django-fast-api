Django Fast API  
=================

Few hacks to speed up defining APIs based on django rest framwork, inspired from fastapi

**First version tested on: python 3.9 and django 4.0**

Features:
---------
- [x] Function based view
- [x] Easy to use decorator
- [x] Accepts validation of input and output using DRF serializers
- [x] Accept CamelCased input and group all rest input methods in same dict :`req`
- [x] Jsonify and camelcase any type of output: `str`, `dict`, `QuerySet`, `Model`
- [x] AutoSchema docs using drf-spectacular
- [x] Error handler that works with DRF
- [ ] Better way to pass the `request` object inside views
- [ ] Convert DRF serializers into a type annotation classes for better processing by IDEs

Quick start
-----------

1. Install the lib::

     `$ pip install django-fast-api`

1. Add "drf_spectacular" to your ``INSTALLED_APPS`` setting like this::
```python
    INSTALLED_APPS = [
        ...
         "drf_spectacular",
        ...
    ]
```
2. Include the swagger documentation  in your project ``urls.py`` like this::
```python
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    path('api-schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
```
3. Add open api schema class and  exception handler to "REST_FRAMEWORK" settings::
```python

    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'EXCEPTION_HANDLER': 'fast_api.error_handling.exception_handler'
    }

```
4. Examples of usage in views::
```python

    from fast_api.decorators import APIRouter

    router = APIRouter()
    from . import serializers, models

    @router.api('public/health_check')
    def health_check(req):
        return "ok"

    @router.api('sample')
    def sample_view():
        return {
            'key' : 'value'
        }
    
    @router.api('sample/error')
    def error_view():
        assert  False, "This is the error message user will get"


    # with input & output validation
    
    from rest_framework import serializers
    from test_api.models import Country


    class CreateCountryRequest(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ['name']
    
    
    class GetCountryRequest(serializers.Serializer):
        id = serializers.IntegerField()
    
    class CountryResponse(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ['name']
            
    @router.api('country/create')
    def create_company(req: serializers.CreateCountryRequest) -> serializers.CountryResponse:
        return models.Country.objects.create(**req.args)
    
    
    @router.api('country/get')
    def create_company(req: GetCountryRequest) -> CountryResponse:
        return models.Country.objects.get(id=req.args.id)   
 ```

* req is a django request
* you will find all endpoint args in req.args

Issues and  Feedback
====================

If you found an issue or you have a feedback , don't hesitate to point to it  as a github issue. 
