from django.contrib import admin
from django.urls import include, path
from .views import AdvertiserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'advertisers', AdvertiserViewset, basename='Advertiser')

urlpatterns = [

] + router.urls