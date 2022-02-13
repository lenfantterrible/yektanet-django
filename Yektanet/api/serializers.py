from rest_framework import serializers
from advertiser_management.models import Advertiser, Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class AdCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ad
        exclude = ('approved', 'advertiser')

class AdvertiserSerializer(serializers.ModelSerializer):
    ads = serializers.SerializerMethodField()

    def get_ads(self, obj):
        return AdSerializer(obj.approved_ads, many=True).data

    class Meta:
        model = Advertiser
        fields = ('name', 'author', 'ads')


