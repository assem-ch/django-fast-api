from fast_api.decorators import APIRouter

router = APIRouter()
from . import serializers, models


@router.api('public/health_check')
def sample_view(req):
    return "ok"


@router.api('sample/success')
def sample_view():
    return {
        'key_name': 'value'
    }


@router.api('sample/error')
def error_view():
    assert False, "This is the error message user will get"



# with input & output validation


@router.api('country/create')
def create_company(req: serializers.CreateCountryRequest) -> serializers.CountryResponse:
    return models.Country.objects.create(**req)


@router.api('country/get')
def create_company(req: serializers.GetCountryRequest) -> serializers.CountryResponse:
    return models.Country.objects.get(id=req.id)