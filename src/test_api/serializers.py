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

